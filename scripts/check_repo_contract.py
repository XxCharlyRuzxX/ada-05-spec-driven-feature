#!/usr/bin/env python3
"""Repository contract and readiness validation guardrail."""

from pathlib import Path
import subprocess
import sys

REQUIRED_FILES = [
    "AGENTS.md",
    "README.md",
    "REQUIREMENTS.md",
    "SPEC.md",
    "ARCHITECTURE.md",
    "TASKS.md",
    "docs/REPO_MAP.md",
    ".gitignore",
    "scripts/verify_repo.sh",
]

SENSITIVE_PATTERNS = [".env", ".env.local", ".env.production", "*.key", "*.pem", "*.pfx"]


def check_required_files() -> list[str]:
    """Verify that all core contract and documentation files exist."""
    missing = [path for path in REQUIRED_FILES if not Path(path).exists()]
    return [f"Missing required file: {p}" for p in missing]


def check_spec_references() -> list[str]:
    """Verify that SPEC.md contains references to requirements (FR-) and acceptance criteria (AC-)."""
    spec_path = Path("SPEC.md")
    if not spec_path.exists():
        return ["SPEC.md does not exist to check references"]

    content = spec_path.read_text(encoding="utf-8")
    errors = []
    if "FR-" not in content:
        errors.append("SPEC.md lacks references to functional requirements (FR-)")
    if "AC-" not in content:
        errors.append("SPEC.md lacks references to acceptance criteria (AC-)")
    return errors


def check_agents_commands() -> list[str]:
    """Verify that AGENTS.md defines required standard commands and stop conditions."""
    agents_path = Path("AGENTS.md")
    if not agents_path.exists():
        return ["AGENTS.md does not exist to check commands"]

    content = agents_path.read_text(encoding="utf-8")
    errors = []
    for expected in ["verify_repo.sh", "pytest", "ruff"]:
        if expected not in content:
            errors.append(f"AGENTS.md missing standard command reference: '{expected}'")
    if "Stop Conditions" not in content:
        errors.append("AGENTS.md missing 'Stop Conditions' section")
    return errors


def check_results_directory() -> list[str]:
    """Verify that results directory exists for output artifacts."""
    results_dir = Path("results")
    if not results_dir.exists() or not results_dir.is_dir():
        return ["Directory 'results/' does not exist"]
    return []


def check_no_tracked_cache_or_secrets() -> list[str]:
    """Verify that no pycache, .pyc, or sensitive files are tracked in git."""
    errors = []
    try:
        tracked_files = (
            subprocess.check_output(["git", "ls-files"], text=True)
            .strip()
            .splitlines()
        )
        for f in tracked_files:
            if f.endswith(".pyc") or "__pycache__" in f:
                errors.append(f"Bytecode file tracked in git: {f}")
            if any(Path(f).match(pat) for pat in SENSITIVE_PATTERNS):
                errors.append(f"Sensitive file tracked in git: {f}")
    except Exception as e:
        errors.append(f"Failed to check git tracked files: {e}")
    return errors


def main() -> int:
    """Run all readiness contract checks."""
    all_errors: list[str] = []
    all_errors.extend(check_required_files())
    all_errors.extend(check_spec_references())
    all_errors.extend(check_agents_commands())
    all_errors.extend(check_results_directory())
    all_errors.extend(check_no_tracked_cache_or_secrets())

    if all_errors:
        print("REPO_CONTRACT: FAIL")
        for err in all_errors:
            print(f"  - {err}")
        return 1

    print("REPO_CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
