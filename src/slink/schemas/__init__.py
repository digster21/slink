"""JSON schemas bundled with slink, plus helpers to load them and validate against them."""

import json
from functools import cache
from importlib.resources import files
from typing import Any

from jsonschema import Draft202012Validator

SCHEMA_SUFFIX = ".schema.json"


def available_schemas() -> list[str]:
    """Return the names of all bundled schemas (filename without the suffix)."""
    return sorted(
        p.name.removesuffix(SCHEMA_SUFFIX)
        for p in files(__package__).iterdir()
        if p.name.endswith(SCHEMA_SUFFIX)
    )


@cache
def load_schema(name: str) -> dict[str, Any]:
    """Load a bundled schema by name, e.g. ``load_schema("config")``."""
    return json.loads(files(__package__).joinpath(f"{name}{SCHEMA_SUFFIX}").read_text())


def validate(instance: Any, name: str) -> None:
    """Validate ``instance`` against a bundled schema.

    Raises ``jsonschema.ValidationError`` if the instance is invalid.
    """
    Draft202012Validator(load_schema(name)).validate(instance)
