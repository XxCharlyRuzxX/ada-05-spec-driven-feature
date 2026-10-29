"""Unit tests for Customer schemas, repository, and search service."""

import pytest
from pydantic import ValidationError

from src.schemas.customer import Customer, CustomerResponse, ErrorResponse
from src.repositories.customer_repository import CustomerRepository
from src.exceptions import InvalidQueryException
from src.services.customer_service import CustomerSearchService


class TestCustomerSchema:
    """Tests for Customer schema validation."""

    def test_customer_creation_valid(self):
        customer = Customer(
            id="cust-001",
            name="John Doe",
            email="john.doe@example.com",
            is_active=True,
        )
        assert customer.id == "cust-001"
        assert customer.name == "John Doe"
        assert customer.email == "john.doe@example.com"
        assert customer.is_active is True

    def test_customer_default_is_active(self):
        customer = Customer(
            id="cust-002",
            name="Jane Doe",
            email="jane.doe@example.com",
        )
        assert customer.is_active is True

    def test_customer_invalid_email(self):
        with pytest.raises(ValidationError):
            Customer(
                id="cust-003",
                name="Invalid Email",
                email="not-an-email",
            )

    def test_customer_missing_required_fields(self):
        with pytest.raises(ValidationError):
            Customer(name="Missing ID and Email")

    def test_customer_empty_name(self):
        with pytest.raises(ValidationError):
            Customer(
                id="cust-004",
                name="",
                email="valid@example.com",
            )

    def test_customer_response_inherits_customer(self):
        res = CustomerResponse(
            id="cust-005",
            name="Alice",
            email="alice@example.com",
            is_active=False,
        )
        assert res.id == "cust-005"
        assert res.is_active is False

    def test_error_response_schema(self):
        err = ErrorResponse(detail="Invalid query")
        assert err.detail == "Invalid query"


class TestCustomerRepository:
    """Tests for CustomerRepository."""

    def test_repository_get_all_default_seeds(self):
        repo = CustomerRepository()
        customers = repo.get_all()
        assert len(customers) >= 5
        # Ensure instances are Customer objects
        for c in customers:
            assert isinstance(c, Customer)
            assert c.id
            assert c.name
            assert c.email

    def test_repository_custom_data(self):
        custom_customers = [
            Customer(
                id="custom-1",
                name="Custom Person",
                email="custom@example.com",
                is_active=True,
            )
        ]
        repo = CustomerRepository(customers=custom_customers)
        assert repo.get_all() == custom_customers


class TestCustomerSearchService:
    """Unit tests for CustomerSearchService."""

    def test_search_partial_name_match(self):
        service = CustomerSearchService()
        results = service.search("Jane")
        assert len(results) >= 1
        assert any(c.name == "Jane Doe" for c in results)

    def test_search_partial_email_match(self):
        service = CustomerSearchService()
        results = service.search("example.net")
        assert len(results) >= 1
        assert any(c.name == "John Doe" for c in results)

    def test_search_matches_both_name_and_email(self):
        service = CustomerSearchService()
        results = service.search("doe")
        # Matches Jane Doe (name & email), John Doe (name), Robert Miller (email rmiller.doe@example.org)
        names = [c.name for c in results]
        assert "Jane Doe" in names
        assert "John Doe" in names
        assert "Robert Miller" in names

    def test_search_case_insensitivity(self):
        service = CustomerSearchService()
        results_lower = service.search("alice")
        results_upper = service.search("ALICE")
        results_mixed = service.search("AlIcE")
        assert len(results_lower) == len(results_upper) == len(results_mixed)
        assert results_lower[0].name == "Alice Smith"

    def test_search_query_whitespace_trimming(self):
        service = CustomerSearchService()
        results_trimmed = service.search("alice")
        results_with_spaces = service.search("   alice   ")
        assert results_trimmed == results_with_spaces

    def test_search_empty_match_returns_empty_list(self):
        service = CustomerSearchService()
        results = service.search("nonexistentqueryxyz")
        assert results == []

    def test_search_includes_inactive_customers(self):
        service = CustomerSearchService()
        results = service.search("Ana")
        assert len(results) >= 1
        ana = next(c for c in results if c.name == "Ana Garcia")
        assert ana.is_active is False

    @pytest.mark.parametrize(
        "invalid_query",
        [
            "",
            "a",
            "   ",
            " a ",
            None,
        ],
    )
    def test_search_short_or_whitespace_query_raises_exception(self, invalid_query):
        service = CustomerSearchService()
        with pytest.raises(InvalidQueryException) as exc_info:
            service.search(invalid_query)
        assert exc_info.value.detail == "Query string must be at least 2 characters long"

    def test_search_query_exceeding_max_length_raises_exception(self):
        service = CustomerSearchService()
        with pytest.raises(InvalidQueryException) as exc_info:
            service.search("a" * 101)
        assert exc_info.value.detail == "Query string must not exceed 100 characters"

    def test_search_with_mock_repository(self):
        mock_customers = [
            Customer(
                id="mock-1",
                name="Test User",
                email="test.user@company.com",
                is_active=True,
            ),
            Customer(
                id="mock-2",
                name="Another Person",
                email="another@different.org",
                is_active=False,
            ),
        ]
        repo = CustomerRepository(customers=mock_customers)
        service = CustomerSearchService(repository=repo)

        results = service.search("company")
        assert len(results) == 1
        assert results[0].id == "mock-1"

    def test_search_filter_is_active_true(self):
        service = CustomerSearchService()
        results = service.search("doe", is_active=True)
        assert len(results) >= 1
        for c in results:
            assert c.is_active is True
        # Ana Garcia is inactive, so searching ana with is_active=True returns empty
        assert service.search("ana", is_active=True) == []

    def test_search_filter_is_active_false(self):
        service = CustomerSearchService()
        # In seed data, Ana Garcia is inactive
        results = service.search("ana", is_active=False)
        assert len(results) >= 1
        assert any(c.name == "Ana Garcia" for c in results)
        for c in results:
            assert c.is_active is False
        # In seed data, all Does are active, so is_active=False returns empty
        assert service.search("doe", is_active=False) == []

    def test_search_filter_is_active_none_returns_both(self):
        service = CustomerSearchService()
        results_omitted = service.search("doe")
        results_none = service.search("doe", is_active=None)
        assert results_omitted == results_none

    def test_search_filter_is_active_with_mixed_mock_repository(self):
        mock_customers = [
            Customer(
                id="mock-active",
                name="John Doe",
                email="john.doe@example.com",
                is_active=True,
            ),
            Customer(
                id="mock-inactive",
                name="Janet Doe",
                email="janet.doe@example.com",
                is_active=False,
            ),
            Customer(
                id="mock-other",
                name="Someone Else",
                email="someone@example.com",
                is_active=True,
            ),
        ]
        repo = CustomerRepository(customers=mock_customers)
        service = CustomerSearchService(repository=repo)

        # Filter active
        active_results = service.search("doe", is_active=True)
        assert len(active_results) == 1
        assert active_results[0].id == "mock-active"
        assert active_results[0].is_active is True

        # Filter inactive
        inactive_results = service.search("doe", is_active=False)
        assert len(inactive_results) == 1
        assert inactive_results[0].id == "mock-inactive"
        assert inactive_results[0].is_active is False

        # Omit / None returns both
        all_doe_results = service.search("doe", is_active=None)
        assert len(all_doe_results) == 2
        ids = {c.id for c in all_doe_results}
        assert ids == {"mock-active", "mock-inactive"}

        omitted_results = service.search("doe")
        assert len(omitted_results) == 2
        assert {c.id for c in omitted_results} == {"mock-active", "mock-inactive"}
