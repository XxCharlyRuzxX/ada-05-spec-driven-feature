# Task Under Test

Change ID: CR-01

## Goal
Add an optional `is_active` boolean filter to the customer search endpoint and service, allowing clients to filter matching customers by their active status (`true` or `false`) while preserving the default behavior (returning both active and inactive customers) when omitted.

## Requirements Covered
- FR-01
- FR-04
- AC-01
- AC-04

## Verification
Describe the observable evidence that will prove the change works:
- Requesting `GET /api/v1/customers/search?q=doe&is_active=true` returns only active customers matching query 'doe'.
- Requesting `GET /api/v1/customers/search?q=doe&is_active=false` returns only inactive customers matching query 'doe'.
- Requesting `GET /api/v1/customers/search?q=doe` (omitting `is_active`) returns both active and inactive customers matching query 'doe' (ensuring full backwards compatibility).
- Requesting `GET /api/v1/customers/search?q=doe&is_active=invalid` returns HTTP 422 Unprocessable Entity.
- Automated unit tests in `tests/test_customer_service.py` and integration tests in `tests/test_api.py` verify all filter scenarios and pass 100%.

## Constraints
- Use REQUIREMENTS.md and SPEC.md as the source of truth.
- Keep changes scoped to this task.
- Do not redefine requirements in this file.
