#!/usr/bin/env python3
"""Validate version identifiers across release documents."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SEMVER = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)


def main() -> int:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if not SEMVER.fullmatch(version):
        print(f"ERROR: VERSION is not strict SemVer: {version!r}", file=sys.stderr)
        return 1
    tag = f"sop-v{version}"
    required = {
        "docs/SOP.md": [
            f'version: "{version}"',
            f"| 版 | {version} |",
            f"| {version} |",
        ],
        "CHANGELOG.md": [f"## [{version}]"],
        "README.md": [f"- SOP version: `{version}`", f"- Git tag: `{tag}`"],
        "VERSIONING.md": [f"SOP_VERSION={version}", f"SOP_TAG={tag}"],
        "PROVENANCE.md": [f"## 版{version}"],
        "PUBLISHING.md": [f"git push origin {tag}", f"git ls-remote --tags origin {tag}"],
    }
    errors: list[str] = []
    for relative, literals in required.items():
        path = ROOT / relative
        content = path.read_text(encoding="utf-8")
        for literal in literals:
            if literal not in content:
                errors.append(f"{relative}: missing current release identifier: {literal}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"RELEASE_METADATA=PASS ({version})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
