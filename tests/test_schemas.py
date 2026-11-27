"""Schema and example integrity tests for the Creduent specification repository."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMAS_DIR = ROOT / "schemas"
EXAMPLES_DIR = ROOT / "examples"


def test_schema_files_are_valid_json():
    """Verify every JSON schema file parses cleanly and defines a schema."""
    schema_files = sorted(SCHEMAS_DIR.glob("*.json"))
    assert schema_files, "Expected at least one JSON schema in schemas/"
    for path in schema_files:
        data = json.loads(path.read_text(encoding="utf-8"))
        assert isinstance(data, dict), f"{path.name} must be a JSON object"
        assert "$schema" in data or "type" in data, f"{path.name} missing schema metadata"


def test_example_files_are_valid_json():
    """Verify every example JSON document parses cleanly."""
    example_files = sorted(EXAMPLES_DIR.glob("*.json"))
    assert example_files, "Expected at least one JSON file in examples/"
    for path in example_files:
        data = json.loads(path.read_text(encoding="utf-8"))
        assert isinstance(data, (dict, list)), f"{path.name} must be a valid JSON object or array"

