# Repository Map

## Entry Points
- `src/main.py` - application bootstrap, CORS, exception handlers, and FastAPI app setup
- `src/api/v1/customers.py` - API route definitions and HTTP query parameter bindings
- `src/services/customer_service.py` - core search algorithms, query sanitation, and business validations
- `src/repositories/customer_repository.py` - in-memory data store with seed customer instances
- `src/schemas/customer.py` - Pydantic customer domain and response models
- `src/exceptions.py` - application-specific domain exceptions (e.g., `InvalidQueryException`)

## Tests
- `tests/test_api.py` - integration tests using FastAPI `TestClient` (status codes, query validation, latency)
- `tests/test_customer_service.py` - unit tests for schemas, customer repository, and search service

## Change Guide
If changing API search behavior or query parameters:
1. Check `REQUIREMENTS.md` and `SPEC.md` for existing contracts and acceptance criteria.
2. Update `src/schemas/customer.py` if request/response contracts change.
3. Update `src/services/customer_service.py` for business logic, filtering, or input validation.
4. Update `src/api/v1/customers.py` route definitions to expose new query parameters.
5. Add or update unit tests in `tests/test_customer_service.py` and integration tests in `tests/test_api.py`.
6. Run `./scripts/verify_repo.sh` to ensure all tests, linting, and repo contracts pass cleanly.

## Do Not Edit Directly
- `.env*` - local environment configuration and credentials.
- `REQUIREMENTS.md` / `SPEC.md` / `ARCHITECTURE.md` - sources of truth; do not modify to make tests pass.
- `SEED_CUSTOMERS` in `src/repositories/customer_repository.py` - baseline seed data; use mock repository instances in tests rather than mutating global seed values.
- `.git/` - version control internal files.
