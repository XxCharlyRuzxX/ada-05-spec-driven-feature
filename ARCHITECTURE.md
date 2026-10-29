# Architecture

## Overview
The Customer Search service is organized as a lightweight layered architecture inside a single local FastAPI application. It separates data models, data access (repository), business logic (service), and delivery mechanism (HTTP controllers).

## Components
1. **API Layer (`src/api`)**: FastAPI route handlers defining endpoints, parsing HTTP parameters, and handling HTTP status mappings.
2. **Service Layer (`src/services`)**: Core search algorithms and business validation rules. Decoupled from HTTP specifics.
3. **Repository Layer (`src/repositories`)**: In-memory data store containing seed records and data retrieval methods.
4. **Domain/Schema Models (`src/models` & `src/schemas`)**: Pydantic models for request validation and response serialization.

## Responsibilities
- **`schemas/customer.py`**: Pydantic models (`CustomerResponse`, `ErrorResponse`).
- **`repositories/customer_repository.py`**: Holds initial in-memory dataset, supports `get_all()`.
- **`services/customer_service.py`**: Executes trimming, input length checks, and case-insensitive substring comparisons.
- **`api/v1/customers.py`**: Defines `GET /api/v1/customers/search`.
- **`main.py`**: FastAPI application entry point.

## Data Flow
```
[ Client Request: GET /api/v1/customers/search?q=john ]
                          │
                          ▼
            [ FastAPI Router: customers.py ]
                          │
                 (Validates query presence)
                          ▼
           [ Service: CustomerSearchService ]
                          │
          (Checks length >= 2, trims whitespace)
                          │
                          ▼
          [ Repository: CustomerRepository ]
                          │
               (Loads customer records)
                          │
                          ▼
          [ Service: Filters & Matches Records ]
                          │
                          ▼
           [ Router: Serializes JSON Response ]
                          │
                          ▼
              [ Client Response: 200 OK ]
```

## Interfaces
- **Endpoint**: `GET /api/v1/customers/search`
- **Query Params**: `q: str` (required)
- **Response Format**:
  ```json
  [
    {
      "id": "c7a6f23b-01d8-4be6-98ec-6e54f73801a1",
      "name": "Jane Doe",
      "email": "jane.doe@example.com",
      "is_active": true
    }
  ]
  ```

## Error Handling
- Invalid queries raise a custom domain exception `InvalidQueryException`.
- A custom FastAPI exception handler maps `InvalidQueryException` to HTTP 400 Bad Request with a clear JSON error body:
  ```json
  {
    "detail": "Query string must be at least 2 characters long"
  }
  ```

## Testing Strategy
- **Unit Tests**: Test `CustomerSearchService` in isolation with mock datasets.
- **API Integration Tests**: Use FastAPI's `TestClient` (backed by `httpx`) to verify status codes, headers, and payload schemas across all scenarios.

## Dependencies
- `fastapi`
- `uvicorn`
- `pydantic`
- `pytest`
- `httpx` (for FastAPI `TestClient`)

## Design Decisions
- **In-memory Repository**: Avoids database overhead, keeps deployment immediate, satisfies NFR-01 (< 150ms) and C-01.
- **Layered Architecture**: Keeps search logic independent of FastAPI framework, making CLI or alternate endpoints trivial to add.

## Trade-offs
- In-memory dataset resets on server restart (acceptable within ADA-05 constraints).
- Linear scan $O(N)$ matching is sufficient for typical assignment volumes (< 10,000 records) without requiring Elasticsearch or full-text indexing.