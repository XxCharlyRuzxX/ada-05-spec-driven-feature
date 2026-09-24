"""In-memory customer repository with seed data."""

from typing import List, Optional
from src.schemas.customer import Customer

SEED_CUSTOMERS: List[Customer] = [
    Customer(
        id="c7a6f23b-01d8-4be6-98ec-6e54f73801a1",
        name="Jane Doe",
        email="jane.doe@example.com",
        is_active=True,
    ),
    Customer(
        id="d1e2f3a4-b5c6-7d8e-9f0a-1b2c3d4e5f6a",
        name="John Doe",
        email="john.smith@example.net",
        is_active=True,
    ),
    Customer(
        id="b2c3d4e5-f6a7-8b9c-0d1e-2f3a4b5c6d7e",
        name="Robert Miller",
        email="rmiller.doe@example.org",
        is_active=True,
    ),
    Customer(
        id="a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d",
        name="Alice Smith",
        email="alice.smith@example.com",
        is_active=True,
    ),
    Customer(
        id="f4e3d2c1-b0a9-8f7e-6d5c-4b3a210fedcb",
        name="Ana Garcia",
        email="ana.garcia@example.com",
        is_active=False,
    ),
    Customer(
        id="98765432-10ab-cdef-0123-456789abcdef",
        name="Carlos Rodriguez",
        email="carlos.r@example.com",
        is_active=True,
    ),
]


class CustomerRepository:
    """In-memory repository for accessing customer records."""

    def __init__(self, customers: Optional[List[Customer]] = None):
        """Initialize repository with provided customers or default seed data."""
        self._customers: List[Customer] = (
            list(customers) if customers is not None else list(SEED_CUSTOMERS)
        )

    def get_all(self) -> List[Customer]:
        """Retrieve all customers in repository."""
        return list(self._customers)
