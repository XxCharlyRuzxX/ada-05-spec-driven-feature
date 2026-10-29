"""Customer routes for API v1."""

from typing import List, Optional
from fastapi import APIRouter, Depends, Query

from src.schemas.customer import CustomerResponse, ErrorResponse
from src.services.customer_service import CustomerSearchService

router = APIRouter(prefix="/customers", tags=["customers"])


def get_customer_search_service() -> CustomerSearchService:
    """Dependency provider for CustomerSearchService."""
    return CustomerSearchService()


@router.get(
    "/search",
    response_model=List[CustomerResponse],
    responses={
        200: {"description": "Matching customer records", "model": List[CustomerResponse]},
        400: {"description": "Invalid query parameters", "model": ErrorResponse},
        422: {"description": "Validation error (missing query parameter or invalid filter)"},
    },
)
def search_customers(
    q: str = Query(..., description="Query string to search by name or email"),
    is_active: Optional[bool] = Query(None, description="Optional filter by active status"),
    service: CustomerSearchService = Depends(get_customer_search_service),
) -> List[CustomerResponse]:
    """Search customers by name or email with optional active status filter."""
    return service.search(query=q, is_active=is_active)
