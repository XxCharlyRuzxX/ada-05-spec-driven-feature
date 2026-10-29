# Tasks

## T-01 Project setup
- **Goal**: Initialize Python project structure, dependency files (`pyproject.toml` or `requirements.txt`), and test environment.
- **Files**:
  - `requirements.txt`
  - `src/__init__.py`
  - `tests/__init__.py`
- **Acceptance**: Virtual environment installs dependencies without errors; `pytest` runs and discovers test directory.
- **Verification**: Run `pytest` returning 0 collected tests without errors.

## T-02 Domain model and schemas
- **Goal**: Define customer entity model and response schemas using Pydantic.
- **Files**:
  - `src/schemas/__init__.py`
  - `src/schemas/customer.py`
- **Acceptance**: `Customer` schema validates fields `id`, `name`, `email`, and `is_active`.
- **Verification**: Unit test validating schema instantiation with valid and invalid customer attributes.

## T-03 Repository and seed data
- **Goal**: Implement in-memory customer repository pre-loaded with realistic test customer data.
- **Files**:
  - `src/repositories/__init__.py`
  - `src/repositories/customer_repository.py`
- **Acceptance**: `CustomerRepository.get_all()` returns the list of seed customer instances.
- **Verification**: Unit test verifying repository returns seeded customers correctly.

## T-04 Search logic and business validations
- **Goal**: Implement `CustomerSearchService` with query sanitation, length validations, and case-insensitive substring search.
- **Files**:
  - `src/services/__init__.py`
  - `src/services/customer_service.py`
  - `src/exceptions.py`
- **Acceptance**: Search logic satisfies AC-02, AC-03, AC-05, and AC-06.
- **Verification**: Unit tests covering partial match on name, email, casing variants, whitespace, and short query errors.

## T-05 FastAPI HTTP API and endpoints
- **Goal**: Expose the search feature via FastAPI HTTP GET endpoint with appropriate error handlers.
- **Files**:
  - `src/api/__init__.py`
  - `src/api/v1/__init__.py`
  - `src/api/v1/customers.py`
  - `src/main.py`
- **Acceptance**: `GET /api/v1/customers/search?q={query}` responds as specified in SPEC.md and AC-01 through AC-06.
- **Verification**: Integration tests using `TestClient(app)` confirming HTTP 200, 400, and 422 responses.

## T-06 Automated testing and traceability verification
- **Goal**: Finalize end-to-end test suite and verify complete coverage of all functional and non-functional requirements.
- **Files**:
  - `tests/test_customer_service.py`
  - `tests/test_api.py`
- **Acceptance**: All tests pass (`pytest -v`) with no warnings or failures.
- **Verification**: Execution of `pytest -v` outputting 100% passing tests.