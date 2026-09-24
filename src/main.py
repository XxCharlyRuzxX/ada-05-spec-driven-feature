"""Main FastAPI application entrypoint."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.api.v1.customers import router as customers_v1_router
from src.exceptions import InvalidQueryException

app = FastAPI(
    title="Customer Search API",
    version="1.0.0",
    description="Local HTTP REST API for searching customer records",
)


@app.exception_handler(InvalidQueryException)
async def invalid_query_exception_handler(
    request: Request, exc: InvalidQueryException
) -> JSONResponse:
    """Handle InvalidQueryException by returning HTTP 400 with detail."""
    return JSONResponse(
        status_code=400,
        content={"detail": exc.detail},
    )


app.include_router(customers_v1_router, prefix="/api/v1")
