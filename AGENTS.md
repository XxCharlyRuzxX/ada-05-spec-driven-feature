# AGENTS.md

## Read First
1. REQUIREMENTS.md
2. SPEC.md
3. ARCHITECTURE.md
4. TASKS.md
5. docs/REPO_MAP.md

## Sources of Truth
- Requirements live only in REQUIREMENTS.md.
- Verifiable behavior lives in SPEC.md.
- Do not change requirements/spec merely to make tests pass.

## Repository Map
- src/ implementation
- tests/ automated tests
- docs/ architecture and operational context
- scripts/ deterministic checks
- results/ generated evidence

## Standard Commands
Install: pip install -r requirements.txt
Run: uvicorn src.main:app --reload
Test: pytest -v
Lint: ruff check .
Verify: ./scripts/verify_repo.sh

## Change Rules
- Keep changes scoped to the requested task.
- Do not weaken existing tests.
- Do not introduce new dependencies without justification.
- Do not modify secrets or generated files.
- Do not edit documentation files (README.md, ARCHITECTURE.md, REQUIREMENTS.md, SPEC.md) unless explicitly requested.

## Stop Conditions
Stop and ask for human input when:
- requirements conflict,
- a destructive action is required,
- an architecture boundary must change,
- a required external system is unavailable.

## Definition of Done
1. `./scripts/verify_repo.sh` exits 0 (all unit & integration tests pass, linter passes, and repo contract check passes).
2. All acceptance criteria relevant to the task in `SPEC.md` / `TASK_UNDER_TEST.md` are covered by automated tests.
3. No out-of-scope files, secrets, or untargeted documentation files are modified.
4. Concrete, reproducible verification evidence is reported in the final response.
