# Agent Instructions

## Project Rules
- Read `REQUIREMENTS.md` before implementing.
- Read `SPEC.md` before implementing.
- Read `ARCHITECTURE.md` before architectural changes.
- Follow `TASKS.md` strictly in sequential order (T-01 to T-06).
- Prefer small, focused, and incremental changes.
- Do not invent business requirements or add extra features not requested.
- Do not modify `REQUIREMENTS.md` or `SPEC.md` to make tests pass.
- Do not delete or weaken tests.
- Do not add external dependencies without technical justification.
- The web framework is FastAPI; do not swap it with Flask or Django.

## Validation
- Run `pytest -v` before and after changes.
- Add tests for every new behavior or validation rule introduced.
- Report changed files and test results after completing each task.
- Stop and ask for clarification if requirements conflict or appear ambiguous.

## Definition of Done
- All relevant unit and integration tests pass.
- Acceptance criteria defined in `SPEC.md` are covered and verified.
- No unrelated files are created or modified.
- Documentation and comments reflect the final implemented behavior.