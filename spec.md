# Customer Search Feature

## Goal
Provide a lightweight, robust, and local HTTP REST endpoint using FastAPI to query customer entities by name or email with partial matching and input validation.

## Requirements Covered
- FR-01
- FR-02
- FR-03
- FR-04
- FR-05
- FR-06
- NFR-01
- NFR-02
- NFR-03

## Scope
- HTTP GET endpoint `/api/v1/customers/search`.
- Query parameter `q` handling with trimming and validation.
- Case-insensitive substring matching over `name` and `email`.
- Serialized JSON responses conforming to schema specifications.
- Error payloads conforming to RFC 7807 / standard FastAPI validation errors.
- Unit and integration tests using `pytest` and `TestClient`.

## Out of Scope
- Fuzzy search, phonetic search (e.g., Soundex), or Levenshtein distance matching.
- Database persistence (PostgreSQL, MySQL, SQLite) or migrations.
- Authentication, authorization, or role-based access control (RBAC).
- Customer creation, update, or deletion (CRUD mutations).

## Domain Model
```
Customer:
  - id: str (UUID or alphanumeric string, required)
  - name: str (Full name, required)
  - email: str (Valid email format, required)
  - is_active: bool (default: true)
```

## Search Rules
1. **Query Sanitization**: Leading and trailing whitespaces in parameter `q` are trimmed before evaluation.
2. **Matching Strategy**: A customer matches if:
   $$\text{lowercase}(q) \subseteq \text{lowercase}(\text{customer.name}) \quad \lor \quad \text{lowercase}(q) \subseteq \text{lowercase}(\text{customer.email})$$
3. **Empty Match**: If no records satisfy the condition, return HTTP 200 with an empty list `[]`.

## Validation Rules
1. `q` parameter is required. Omitting `q` returns HTTP 422 Unprocessable Entity.
2. `q` must contain at least 2 non-whitespace characters. Submissions with length $< 2$ or whitespace only return HTTP 400 Bad Request with error detail `"Query string must be at least 2 characters long"`.
3. `q` must not exceed 100 characters. Exceeding returns HTTP 400 Bad Request.

## Error Handling
- **HTTP 400 Bad Request**: Raised when `q` violates business constraints (e.g., blank, whitespace only, length $< 2$ or $> 100$).
- **HTTP 422 Unprocessable Entity**: Standard FastAPI response for missing required query parameter `q`.
- **HTTP 500 Internal Server Error**: Generic handler for unexpected runtime exceptions.

## Acceptance Criteria
- **AC-01 (FR-01, NFR-02)**: Requesting `GET /api/v1/customers/search?q=ana` returns HTTP 200 and a JSON array.
- **AC-02 (FR-02, FR-03)**: Searching with `q=doe` matches both "John Doe" (`name`) and "jane.doe@example.com" (`email`).
- **AC-03 (FR-03)**: Searching with uppercase `q=ALICE` returns records matching "alice" regardless of casing.
- **AC-04 (FR-04)**: Every item returned includes `id`, `name`, `email`, and `is_active`.
- **AC-05 (FR-05)**: `GET /api/v1/customers/search?q=   ` or `GET /api/v1/customers/search?q=a` returns HTTP 400.
- **AC-06 (FR-06)**: Searching for non-existent values returns HTTP 200 and `[]`.
- **AC-07 (NFR-03)**: Automated test suite passes 100% on `pytest -v`.

## Test Scenarios
- **TS-01**: Exact substring matching on customer name (case-insensitive).
- **TS-02**: Exact substring matching on customer email domain or local part.
- **TS-03**: No match found returns empty array `[]` with status 200.
- **TS-04**: Missing query parameter `q` produces 422.
- **TS-05**: Whitespace-only or single-character `q` produces 400.
- **TS-06**: Query matching multiple records returns all relevant items.

## Constraints
- Local execution only (`http://127.0.0.1:8000`).
- No external network or paid services.

## Open Questions
- N/A (All initial questions addressed in REQUIREMENTS.md assumptions).