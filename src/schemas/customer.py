"""Customer schemas and domain models."""

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class Customer(BaseModel):
    """Customer domain model and schema."""

    id: str = Field(..., description="Unique customer identifier")
    name: str = Field(..., min_length=1, description="Full customer name")
    email: EmailStr = Field(..., description="Valid customer email address")
    is_active: bool = Field(default=True, description="Customer active status")

    model_config = ConfigDict(from_attributes=True)


class CustomerResponse(Customer):
    """Schema representing customer response data."""

    pass


class ErrorResponse(BaseModel):
    """Schema representing error response."""

    detail: str = Field(..., description="Error message detail")
