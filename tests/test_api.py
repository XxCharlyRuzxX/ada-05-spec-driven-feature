"""Integration tests for Customer Search HTTP API."""

import time
import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.schemas.customer import Customer
from src.repositories.customer_repository import CustomerRepository
from src.services.customer_service import CustomerSearchService
from src.api.v1.customers import get_customer_search_service

client = TestClient(app)


class TestCustomerSearchAPI:
    """Integration test suite for /api/v1/customers/search."""

    def test_search_success_ac01(self):
        """AC-01: GET /api/v1/customers/search?q=ana returns HTTP 200 and JSON array."""
        response = client.get("/api/v1/customers/search?q=ana")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert any(item["name"] == "Ana Garcia" for item in data)

    def test_search_matches_name_and_email_ac02(self):
        """AC-02: Searching with q=doe matches both customer name and email."""
        response = client.get("/api/v1/customers/search?q=doe")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2
        names = [item["name"] for item in data]
        emails = [item["email"] for item in data]
        assert "John Doe" in names
        assert "jane.doe@example.com" in emails

    def test_search_case_insensitive_ac03(self):
        """AC-03: Searching with uppercase q=ALICE returns matching records."""
        response = client.get("/api/v1/customers/search?q=ALICE")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert any(item["name"] == "Alice Smith" for item in data)

    def test_search_item_fields_ac04(self):
        """AC-04: Every item returned includes id, name, email, and is_active."""
        response = client.get("/api/v1/customers/search?q=doe")
        assert response.status_code == 200
        data = response.json()
        for item in data:
            assert "id" in item and isinstance(item["id"], str)
            assert "name" in item and isinstance(item["name"], str)
            assert "email" in item and isinstance(item["email"], str)
            assert "is_active" in item and isinstance(item["is_active"], bool)

    @pytest.mark.parametrize(
        "invalid_q",
        [
            "",
            "   ",
            "a",
            " a ",
        ],
    )
    def test_search_short_or_blank_query_ac05(self, invalid_q):
        """AC-05: Blank, whitespace-only, or single-character q returns HTTP 400."""
        response = client.get("/api/v1/customers/search", params={"q": invalid_q})
        assert response.status_code == 400
        data = response.json()
        assert data.get("detail") == "Query string must be at least 2 characters long"

    def test_search_non_existent_returns_empty_list_ac06(self):
        """AC-06: Searching for non-existent values returns HTTP 200 and []."""
        response = client.get("/api/v1/customers/search?q=nonexistentqueryxyz")
        assert response.status_code == 200
        assert response.json() == []

    def test_search_missing_q_parameter_ts04(self):
        """TS-04: Missing query parameter q produces HTTP 422."""
        response = client.get("/api/v1/customers/search")
        assert response.status_code == 422

    def test_search_query_exceeding_max_length(self):
        """Query parameter exceeding 100 characters returns HTTP 400."""
        response = client.get("/api/v1/customers/search", params={"q": "a" * 101})
        assert response.status_code == 400
        data = response.json()
        assert data.get("detail") == "Query string must not exceed 100 characters"

    def test_search_response_latency_nfr01(self):
        """NFR-01: Search endpoint must respond in under 150ms."""
        start = time.perf_counter()
        response = client.get("/api/v1/customers/search?q=doe")
        duration_ms = (time.perf_counter() - start) * 1000
        assert response.status_code == 200
        assert duration_ms < 150, f"Response took {duration_ms:.2f}ms which exceeds 150ms limit"

    def test_search_filter_is_active_true(self):
        """Requesting GET /api/v1/customers/search?q=doe&is_active=true returns only active customers matching 'doe'."""
        response = client.get("/api/v1/customers/search?q=doe&is_active=true")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        for item in data:
            assert item["is_active"] is True
            assert "doe" in item["name"].lower() or "doe" in item["email"].lower()

    def test_search_filter_is_active_false(self):
        """GET /api/v1/customers/search?q=doe&is_active=false returns only inactive customers matching 'doe'."""
        response = client.get("/api/v1/customers/search?q=doe&is_active=false")
        assert response.status_code == 200
        assert response.json() == []

        # In seed data, Ana Garcia is inactive
        res_ana = client.get("/api/v1/customers/search?q=ana&is_active=false")
        assert res_ana.status_code == 200
        ana_data = res_ana.json()
        assert len(ana_data) >= 1
        for item in ana_data:
            assert item["is_active"] is False

    def test_search_filter_is_active_omitted_returns_both(self):
        """Requesting GET /api/v1/customers/search?q=doe (omitting is_active) returns backwards-compatible results."""
        response = client.get("/api/v1/customers/search?q=doe")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2
        names = [item["name"] for item in data]
        assert "Jane Doe" in names
        assert "John Doe" in names

    def test_search_filter_is_active_invalid_returns_422(self):
        """Requesting GET /api/v1/customers/search?q=doe&is_active=invalid returns HTTP 422 Unprocessable Entity."""
        response = client.get("/api/v1/customers/search?q=doe&is_active=invalid")
        assert response.status_code == 422

    def test_search_filter_is_active_with_mixed_dataset(self):
        """Verify active, inactive, and omitted filtering on a dataset with both active and inactive matches."""
        mock_customers = [
            Customer(
                id="mock-doe-active",
                name="John Doe",
                email="john.doe@example.com",
                is_active=True,
            ),
            Customer(
                id="mock-doe-inactive",
                name="Janet Doe",
                email="janet.doe@example.com",
                is_active=False,
            ),
        ]
        repo = CustomerRepository(customers=mock_customers)
        mock_service = CustomerSearchService(repository=repo)

        app.dependency_overrides[get_customer_search_service] = lambda: mock_service
        try:
            # is_active=true
            res_true = client.get("/api/v1/customers/search?q=doe&is_active=true")
            assert res_true.status_code == 200
            data_true = res_true.json()
            assert len(data_true) == 1
            assert data_true[0]["id"] == "mock-doe-active"
            assert data_true[0]["is_active"] is True

            # is_active=false
            res_false = client.get("/api/v1/customers/search?q=doe&is_active=false")
            assert res_false.status_code == 200
            data_false = res_false.json()
            assert len(data_false) == 1
            assert data_false[0]["id"] == "mock-doe-inactive"
            assert data_false[0]["is_active"] is False

            # is_active omitted
            res_all = client.get("/api/v1/customers/search?q=doe")
            assert res_all.status_code == 200
            data_all = res_all.json()
            assert len(data_all) == 2
            ids = {item["id"] for item in data_all}
            assert ids == {"mock-doe-active", "mock-doe-inactive"}
        finally:
            app.dependency_overrides.clear()
