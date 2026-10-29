# Implicit Knowledge Found

## IK-01
What:
How to execute the comprehensive verification pipeline (tests + lint + repository contract check) in a single reproducible command.
How was it discovered:
By inspecting `pyproject.toml`, running `pytest -v`, and attempting `ruff check .` (which failed due to unconfigured rules).
Should this remain implicit?
NO
Where should it become explicit?
`AGENTS.md` (Standard Commands) and `scripts/verify_repo.sh`.

## IK-02
What:
Which files and paths must NOT be edited directly (e.g., `README.md`, `architecture.md`, `requirements.md`, `spec.md`, production/seed data, compiled caches, secrets).
How was it discovered:
Not documented. The agent modified `README.md`, `architecture.md`, and default seed data because no boundaries or protected paths were declared.
Risk:
The agent causes scope creep, mutates documentation inappropriately, or alters shared baseline data without authorization.
Should this remain implicit?
NO
Where should it become explicit?
`AGENTS.md` (Change Rules & Stop Conditions) and `docs/REPO_MAP.md` (Do Not Edit Directly).

## IK-03
What:
Where the code entry points, architectural boundaries, and tests are located without having to scan every single file in `src/`.
How was it discovered:
By running `find src tests -type f` and reading every `.py` file one by one.
Should this remain implicit?
NO
Where should it become explicit?
`docs/REPO_MAP.md` (Entry Points, Tests, and Change Guide).

## IK-04
What:
Repository cleanliness standards and file ignore rules (ignoring `.pyc`, `__pycache__`, `.DS_Store`, `.env`).
How was it discovered:
Inspecting `git status` after running pytest revealed dozens of tracked `.pyc` and `.DS_Store` files because no `.gitignore` existed.
Risk:
Polluting version control with binary artifacts, bytecode, and potential local secrets.
Should this remain implicit?
NO
Where should it become explicit?
`.gitignore` and `scripts/check_repo_contract.py`.
