#!/usr/bin/env python3
"""Check repository-local targets in Markdown links without network access."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parent.parent
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")


def local_target(raw: str) -> str | None:
    target = raw.strip()
    if target.startswith("<") and ">" in target:
        target = target[1 : target.index(">")]
    else:
        target = target.split(maxsplit=1)[0]
    if target.startswith(("https://", "http://", "mailto:", "#")):
        return None
    return unquote(target.split("#", 1)[0]) or None


def main() -> int:
    errors: list[str] = []
    for markdown in sorted(ROOT.rglob("*.md")):
        if ".git" in markdown.parts:
            continue
        content = markdown.read_text(encoding="utf-8")
        for line_number, line in enumerate(content.splitlines(), 1):
            for match in LINK.finditer(line):
                target = local_target(match.group(1))
                if target is None:
                    continue
                resolved = (markdown.parent / target).resolve()
                try:
                    resolved.relative_to(ROOT)
                except ValueError:
                    errors.append(f"{markdown.relative_to(ROOT)}:{line_number}: link escapes repository: {target}")
                    continue
                if not resolved.exists():
                    errors.append(f"{markdown.relative_to(ROOT)}:{line_number}: missing link target: {target}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("MARKDOWN_LINKS=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
