"""Validate git commit messages follow Conventional Commits."""

import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

CONVENTIONAL_COMMITS_PATTERN = re.compile(
    r"^(feat|fix|chore|docs|style|refactor|perf|test|build|ci|revert)" r"(\([\w.-]+\))?: .{1,72}$"
)

ALLOWED_TYPES = [
    "feat",
    "fix",
    "chore",
    "docs",
    "style",
    "refactor",
    "perf",
    "test",
    "build",
    "ci",
    "revert",
]


def get_commit_message() -> str:
    commit_msg_file = Path(sys.argv[1])
    raw = commit_msg_file.read_text(encoding="utf-8-sig")
    return raw.strip()


def validate(message: str) -> tuple[bool, str]:
    lines = message.split("\n")
    first_line = lines[0]

    if not first_line:
        return False, "Commit message is empty"

    if not CONVENTIONAL_COMMITS_PATTERN.match(first_line):
        return False, (
            f"Invalid commit format.\n\n"
            f"Expected: tipo(alcance): descripción\n"
            f"Got:      {first_line}\n\n"
            f"Tipos permitidos: {', '.join(ALLOWED_TYPES)}\n"
            f"Ejemplo: feat(auth): add login endpoint\n"
            f"         fix(tareas): resolve date parsing error\n"
            f"         docs: update README"
        )

    scope_match = re.search(r"\(([\w.-]+)\)", first_line)
    if scope_match:
        scope = scope_match.group(1)
        if not scope.islower():
            return False, f"Scope '{scope}' must be lowercase"

    if len(lines) > 1 and lines[1] != "":
        if not lines[1].strip():
            pass
        elif not lines[1].startswith("\n") and first_line.endswith("."):
            return False, "First line must not end with a period"

    return True, ""


def main():
    message = get_commit_message()
    is_valid, error_msg = validate(message)

    if not is_valid:
        print(error_msg)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
