# Requirements Customer Search

## User Story
As a user,
I want to search customers by name or email,
so that I can quickly find the customer record I need.

## Functional Requirements
- **FR-01**: The system must provide a search endpoint that accepts a query string (`q`) to filter customers.
- **FR-02**: The search must match against customer name and customer email.
- **FR-03**: The search must support case-insensitive, partial matching (substring matching).
- **FR-04**: The system must return a list of matching customer records containing at least ID, full name, email, and active status.
- **FR-05**: The system must reject empty or whitespace-only search queries with an appropriate client error response.
- **FR-06**: The system must return an empty list with a successful status code if no customers match the search criteria.

## Non-Functional Requirements
- **NFR-01**: **Performance & Latency**: The search endpoint must respond in under 150ms for datasets under 1,000 in-memory/local records.
- **NFR-02**: **Interface Protocol**: The service must expose a local HTTP REST API using FastAPI.
- **NFR-03**: **Testability**: All business logic and HTTP endpoints must achieve 100% automated test coverage with `pytest` and `httpx`.

## Open Questions
- **Q-01**: Should inactive customers be excluded from search results by default? *(Assumed: No, inactive customers are returned with their status indicated, unless explicitly filtered).*
- **Q-02**: Should search queries enforce a minimum character length? *(Assumed: Yes, minimum 2 non-whitespace characters to prevent unbounded result sets).*

## Constraints / Assumptions
- **C-01**: The application must run locally without external paid APIs, cloud services, or dedicated database servers.
- **C-02**: Built using Python 3.11+ and FastAPI.
- **A-01**: Initial customer data can be seeded from an in-memory collection or a local static JSON file.