"""Schema tests.

Test Fixtures live in `tests/fixtures/<schema_name>/{valid,invalid}/*.json`
New files discovered automatically.

"""

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, ValidationError

from slink.schemas import available_schemas, load_schema, validate

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def _fixture_cases(kind: str) -> list:
    return [
        pytest.param(schema, path, id=f"{schema}/{path.name}")
        for schema in available_schemas()
        for path in sorted((FIXTURES_DIR / schema / kind).glob("*.json"))
    ]


def test_schemas_are_bundled():
    assert available_schemas(), "no *.schema.json files found in slink.schemas"


@pytest.mark.parametrize("name", available_schemas())
def test_schema_is_valid(name):
    Draft202012Validator.check_schema(load_schema(name))


@pytest.mark.parametrize(("schema", "path"), _fixture_cases("valid"))
def test_valid_fixture_passes(schema, path):
    validate(json.loads(path.read_text()), schema)


@pytest.mark.parametrize(("schema", "path"), _fixture_cases("invalid"))
def test_invalid_fixture_fails(schema, path):
    with pytest.raises(ValidationError):
        validate(json.loads(path.read_text()), schema)
