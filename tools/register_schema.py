#!/usr/bin/env python3
"""Generate and validate the normative register templates."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO_ROOT / "schemas/registers.schema.json"
DOC_PATH = REPO_ROOT / "docs/REGISTER_SCHEMA.md"


def load_schema() -> dict[str, Any]:
    with SCHEMA_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def enum_text(register: dict[str, Any], column: str) -> str:
    values = register.get("enums", {}).get(column)
    return " / ".join(values) if values else ""


def foreign_text(register: dict[str, Any], column: str) -> str:
    for foreign_key in register.get("foreign_keys", []):
        if foreign_key["column"] == column:
            suffix = " (複数)" if foreign_key.get("multiple") else ""
            return f"{foreign_key['register']}.{foreign_key['target']}{suffix}"
    for foreign_key in register.get("conditional_foreign_keys", []):
        if foreign_key["column"] == column:
            return (
                f"{foreign_key['register']}.{foreign_key['target']} "
                f"if {foreign_key['when_column']}={foreign_key['when_value']}"
            )
    self_reference = register.get("self_reference")
    if self_reference and self_reference["column"] == column:
        return f"self.{self_reference['target']}"
    return ""


def render_document(schema: dict[str, Any]) -> str:
    lines = [
        "<!-- GENERATED FILE: tools/register_schema.py --write -->",
        "# 台帳スキーマおよび入力規則",
        "",
        "この文書と `templates/*.tsv` のヘッダーは、規範的な機械可読定義 "
        "[`schemas/registers.schema.json`](../schemas/registers.schema.json) から生成される。直接編集せず、スキーマ変更後に "
        "`python3 tools/register_schema.py --write` を実行する。",
        "",
        "## 共通入力規則",
        "",
        f"- 文字コードは `{schema['encoding']}`、改行は `{schema['line_ending']}`、区切りはタブとする。",
        "- 1行目は対応テンプレートと完全一致するヘッダーとし、列の追加、削除、改名または並べ替えを行ってはならない。",
        "- 値にタブ、CRまたはLFを含めてはならない。引用符によるエスケープは定義しない。複数行情報は別ファイルへ保存し、そのIDまたはハッシュを記録する。",
        f"- 複数IDは空白を含めず `{schema['multiple_value_separator']}` で区切る。順序に意味がある場合は元資料へ明記する。",
        f"- 必須値の来歴が不明な場合は空欄ではなく `{schema['unknown_value']}` を使用する。ただし、列の形式または列挙値が `UNKNOWN` を許可しない場合、その記録は不適合とする。",
        f"- `{schema['none_value']}` は、確認の結果対象が存在しないことを表す。空欄は任意列の未入力、`UNKNOWN` は未確認、`NONE` は確認済み不存在であり、相互に置換してはならない。",
        "- `date` は `YYYY-MM-DD`、`utc_datetime` は秒までの `YYYY-MM-DDThh:mm:ssZ` とし、ローカル時刻を記録してはならない。",
        "- SHA-256は小文字16進64桁とする。IDは台帳内で一意でなければならず、外部キーは同じ検証スナップショット内の有効な行を参照する。",
        "- 台帳を凍結した後は行を削除または上書きしない。訂正行へ新しいIDを付け、旧行を `SUPERSEDED`、新行を `ACTIVE` とし、新行の `SUPERSEDES_ID` から旧IDを参照する。誤登録を無効化する場合は `VOID` とし理由を `NOTES` に記録する。",
        "- 台帳スナップショット全体のSHA-256と検証日時を適合記録へ固定する。",
        "",
        "## 台帳一覧",
        "",
        "| ID | 配布テンプレート | プロジェクト内の標準パス | 状態 |",
        "|---|---|---|---|",
    ]
    for register in schema["registers"]:
        state = "移行専用" if register.get("legacy") else "規範"
        project_path = register.get("project_path", "—")
        lines.append(
            f"| `{register['id']}` | `{register['template']}` | `{project_path}` | {state} |"
        )

    for register in schema["registers"]:
        lines.extend(
            [
                "",
                f"## {register['id']}",
                "",
                register["description"],
                "",
            ]
        )
        if register.get("legacy"):
            lines.extend(
                [
                    "> [!WARNING]",
                    "> この台帳は版1.1.0からの移行入力専用であり、新規プロジェクトの適合証拠には使用できない。正規化P4-H台帳へ移記し、検証した後に使用する。",
                    "",
                ]
            )
        lines.extend(
            [
                "| 列 | 必須 | 形式 | 列挙値 | 参照先 |",
                "|---|:---:|---|---|---|",
            ]
        )
        required = set(register.get("required", []))
        for column in register["columns"]:
            lines.append(
                "| `{}` | {} | `{}` | {} | {} |".format(
                    column,
                    "必須" if column in required else "任意",
                    register.get("formats", {}).get(column, "text"),
                    enum_text(register, column) or "—",
                    foreign_text(register, column) or "—",
                )
            )
    lines.append("")
    return "\n".join(lines)


def expected_template(register: dict[str, Any]) -> str:
    return "\t".join(register["columns"]) + "\n"


def write_generated(schema: dict[str, Any]) -> None:
    for register in schema["registers"]:
        path = REPO_ROOT / register["template"]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(expected_template(register), encoding="utf-8", newline="\n")
    DOC_PATH.write_text(render_document(schema), encoding="utf-8", newline="\n")


def check_generated(schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for register in schema["registers"]:
        path = REPO_ROOT / register["template"]
        if not path.is_file():
            errors.append(f"missing template: {path.relative_to(REPO_ROOT)}")
            continue
        actual = path.read_text(encoding="utf-8")
        if actual != expected_template(register):
            errors.append(f"template differs from schema: {path.relative_to(REPO_ROOT)}")
    if not DOC_PATH.is_file():
        errors.append(f"missing generated document: {DOC_PATH.relative_to(REPO_ROOT)}")
    elif DOC_PATH.read_text(encoding="utf-8") != render_document(schema):
        errors.append(f"generated document is stale: {DOC_PATH.relative_to(REPO_ROOT)}")
    for template in schema.get("markdown_templates", []):
        path = REPO_ROOT / template["path"]
        if not path.is_file():
            errors.append(f"missing Markdown template: {template['path']}")
            continue
        content = path.read_text(encoding="utf-8")
        for literal in template["required_literals"]:
            if literal not in content:
                errors.append(f"{template['path']}: missing required text: {literal}")
    return errors


def valid_date(value: str) -> bool:
    try:
        dt.datetime.strptime(value, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def valid_utc_datetime(value: str) -> bool:
    try:
        dt.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
        return True
    except ValueError:
        return False


def format_valid(name: str, value: str, separator: str) -> bool:
    if value == "" and name.endswith("_or_empty"):
        return True
    if value == "NONE" and name.endswith("_or_none"):
        return True
    if value == "UNKNOWN" and name.endswith("_or_unknown"):
        return True
    base = re.sub(r"_(or_empty|or_none|or_unknown)$", "", name)
    if base == "date":
        return valid_date(value)
    if base == "date_or_partial":
        return bool(re.fullmatch(r"(?:[0-9]{4}|[0-9]{4}-[0-9]{2}|[0-9]{4}-[0-9]{2}-[0-9]{2}|UNKNOWN)", value))
    if base == "utc_datetime":
        return valid_utc_datetime(value)
    if base == "sha256":
        return bool(re.fullmatch(r"[0-9a-f]{64}", value))
    patterns = {
        "source_id": r"S[0-9]{4,}",
        "idea_id": r"I[0-9]{4,}",
        "session_id": r"SESSION-[0-9]{4,}",
        "exception_id": r"EX-[0-9]{4,}",
        "source_id_list": rf"S[0-9]{{4,}}(?:{re.escape(separator)}S[0-9]{{4,}})*",
        "idea_id_list": rf"I[0-9]{{4,}}(?:{re.escape(separator)}I[0-9]{{4,}})*",
        "exception_id_list": rf"EX-[0-9]{{4,}}(?:{re.escape(separator)}EX-[0-9]{{4,}})*",
        "evidence_id_list": rf"[A-Za-z0-9][A-Za-z0-9._-]*(?:{re.escape(separator)}[A-Za-z0-9][A-Za-z0-9._-]*)*",
    }
    return bool(re.fullmatch(patterns.get(base, r".*"), value))


def read_register(path: Path, register: dict[str, Any], separator: str) -> tuple[list[dict[str, str]], list[str]]:
    errors: list[str] = []
    try:
        raw = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return [], [f"{path}: not valid UTF-8"]
    if "\r" in raw:
        errors.append(f"{path}: CR is prohibited; use LF")
    lines = raw.splitlines()
    if not lines:
        return [], [f"{path}: empty file"]
    expected = register["columns"]
    header = lines[0].split("\t")
    if header != expected:
        errors.append(f"{path}: header does not match {register['id']}")
        return [], errors
    rows: list[dict[str, str]] = []
    for line_number, line in enumerate(lines[1:], 2):
        if line == "":
            errors.append(f"{path}:{line_number}: blank rows are prohibited")
            continue
        values = line.split("\t")
        if len(values) != len(expected):
            errors.append(f"{path}:{line_number}: expected {len(expected)} columns, found {len(values)}")
            continue
        row = dict(zip(expected, values))
        for column in register.get("required", []):
            if row[column] == "":
                errors.append(f"{path}:{line_number}:{column}: required value is empty")
        for column, allowed in register.get("enums", {}).items():
            value = row[column]
            if value and value not in allowed:
                errors.append(f"{path}:{line_number}:{column}: invalid enum value {value!r}")
        for column, format_name in register.get("formats", {}).items():
            value = row[column]
            if value and not format_valid(format_name, value, separator):
                errors.append(f"{path}:{line_number}:{column}: invalid {format_name}: {value!r}")
        rows.append(row)
    keys: set[tuple[str, ...]] = set()
    for row_number, row in enumerate(rows, 2):
        key = tuple(row[column] for column in register.get("primary_key", []))
        if key and key in keys:
            errors.append(f"{path}:{row_number}: duplicate primary key {key}")
        keys.add(key)
    return rows, errors


def validate_root(schema: dict[str, Any], project_root: Path) -> list[str]:
    errors: list[str] = []
    if not project_root.is_dir():
        return [f"project root does not exist or is not a directory: {project_root}"]
    loaded: dict[str, list[dict[str, str]]] = {}
    definitions = {register["id"]: register for register in schema["registers"]}
    separator = schema["multiple_value_separator"]
    for register in schema["registers"]:
        project_path = register.get("project_path")
        if not project_path or register.get("legacy"):
            continue
        path = project_root / project_path
        if not path.exists():
            continue
        rows, row_errors = read_register(path, register, separator)
        loaded[register["id"]] = rows
        errors.extend(row_errors)
    if not loaded:
        errors.append(f"no recognized register files found below {project_root}")
    for register_id, rows in loaded.items():
        register = definitions[register_id]
        for foreign_key in register.get("foreign_keys", []):
            values = {
                row[foreign_key["target"]]
                for row in loaded.get(foreign_key["register"], [])
                if row.get("RECORD_STATUS", "ACTIVE") == "ACTIVE"
            }
            for row_number, row in enumerate(rows, 2):
                raw_value = row[foreign_key["column"]]
                if raw_value in ("", "NONE", "UNKNOWN"):
                    continue
                references = raw_value.split(separator) if foreign_key.get("multiple") else [raw_value]
                for reference in references:
                    if reference not in values:
                        errors.append(
                            f"{register['project_path']}:{row_number}:{foreign_key['column']}: "
                            f"missing active {foreign_key['register']}.{foreign_key['target']}={reference}"
                        )
        for foreign_key in register.get("conditional_foreign_keys", []):
            values = {
                row[foreign_key["target"]]
                for row in loaded.get(foreign_key["register"], [])
                if row.get("RECORD_STATUS", "ACTIVE") == "ACTIVE"
            }
            for row_number, row in enumerate(rows, 2):
                if row[foreign_key["when_column"]] != foreign_key["when_value"]:
                    continue
                reference = row[foreign_key["column"]]
                if not reference:
                    errors.append(
                        f"{register['project_path']}:{row_number}:{foreign_key['column']}: "
                        f"required when {foreign_key['when_column']}={foreign_key['when_value']}"
                    )
                elif reference not in values:
                    errors.append(
                        f"{register['project_path']}:{row_number}:{foreign_key['column']}: "
                        f"missing active {foreign_key['register']}.{foreign_key['target']}={reference}"
                    )
        self_reference = register.get("self_reference")
        if self_reference:
            target = self_reference["target"]
            column = self_reference["column"]
            row_by_id = {row[target]: row for row in rows}
            superseded_targets: set[str] = set()
            for row_number, row in enumerate(rows, 2):
                reference = row[column]
                if not reference:
                    continue
                if reference == row[target]:
                    errors.append(f"{register['project_path']}:{row_number}:{column}: self-reference is prohibited")
                elif reference not in row_by_id:
                    errors.append(f"{register['project_path']}:{row_number}:{column}: missing record {reference}")
                else:
                    superseded_targets.add(reference)
                    if row_by_id[reference].get("RECORD_STATUS") != "SUPERSEDED":
                        errors.append(f"{register['project_path']}:{row_number}:{column}: target {reference} is not SUPERSEDED")
            for row_number, row in enumerate(rows, 2):
                if row.get("RECORD_STATUS") == "SUPERSEDED" and row[target] not in superseded_targets:
                    errors.append(f"{register['project_path']}:{row_number}: SUPERSEDED row has no replacement")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="regenerate TSV headers and the schema document")
    parser.add_argument("--check", action="store_true", help="check generated files and Markdown templates")
    parser.add_argument("--validate-root", type=Path, help="validate registers found below a project root")
    args = parser.parse_args()
    if not (args.write or args.check or args.validate_root):
        parser.error("select --write, --check, or --validate-root")
    schema = load_schema()
    if args.write:
        write_generated(schema)
    errors: list[str] = []
    if args.check:
        errors.extend(check_generated(schema))
    if args.validate_root:
        errors.extend(validate_root(schema, args.validate_root.resolve()))
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("REGISTER_SCHEMA=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
