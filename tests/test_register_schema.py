#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("register_schema", ROOT / "tools/register_schema.py")
assert SPEC and SPEC.loader
REGISTER_SCHEMA = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(REGISTER_SCHEMA)


class RegisterSchemaTests(unittest.TestCase):
    def setUp(self) -> None:
        self.schema = REGISTER_SCHEMA.load_schema()
        self.by_id = {item["id"]: item for item in self.schema["registers"]}

    def write_register(self, root: Path, register_id: str, rows: list[list[str]]) -> None:
        register = self.by_id[register_id]
        path = root / register["project_path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        lines = ["\t".join(register["columns"])] + ["\t".join(row) for row in rows]
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    def test_rejects_invalid_enum_and_duplicate_key(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            register = self.by_id["SOURCE_REGISTER"]
            base = {column: "" for column in register["columns"]}
            base.update(
                SOURCE_ID="S0001",
                TITLE="資料",
                ACQUISITION_PATH="図書館",
                DISCOVERY_METHOD="書誌",
                MEDIUM="PAPER",
                HUMAN_AUTHORSHIP_STATUS="INVALID",
                GENAI_STATUS="UNKNOWN",
                PERMITTED_USE="FACT",
                REVIEWER="R01",
                REVIEW_DATE="2026-07-17",
                RECORD_STATUS="ACTIVE",
            )
            row = [base[column] for column in register["columns"]]
            self.write_register(root, "SOURCE_REGISTER", [row, row])
            errors = REGISTER_SCHEMA.validate_root(self.schema, root)
            self.assertTrue(any("invalid enum" in error for error in errors))
            self.assertTrue(any("duplicate primary key" in error for error in errors))

    def test_rejects_missing_foreign_key(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            register = self.by_id["SESSION_REGISTER"]
            data = {column: "" for column in register["columns"]}
            data.update(
                SESSION_ID="SESSION-0001",
                START_AT="2026-07-17T01:00:00Z",
                END_AT="2026-07-17T02:00:00Z",
                CHAPTER_OR_SCENE="001",
                SOURCE_IDS="S9999",
                DEVICE_ID="DEVICE-01",
                ENVIRONMENT_ID="ENV-01",
                DICTIONARY_ID="DIC-01",
                EXCEPTION_STATUS="NONE",
                OPERATOR="AUTHOR",
                RECORD_STATUS="ACTIVE",
            )
            self.write_register(root, "SESSION_REGISTER", [[data[column] for column in register["columns"]]])
            errors = REGISTER_SCHEMA.validate_root(self.schema, root)
            self.assertTrue(any("missing active SOURCE_REGISTER" in error for error in errors))

    def test_accepts_header_only_templates(self) -> None:
        self.assertEqual([], REGISTER_SCHEMA.check_generated(self.schema))


if __name__ == "__main__":
    unittest.main()
