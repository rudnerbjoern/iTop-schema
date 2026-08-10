import json
from pathlib import Path
from typing import cast

import pytest

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
RAW_SCHEMA_CONFIG: object = json.loads(
    (REPOSITORY_ROOT / "schemas.json").read_text(encoding="utf-8")
)
SCHEMA_CONFIG = cast(dict[str, object], RAW_SCHEMA_CONFIG)
SUPPORTED_VERSIONS = cast(list[str], SCHEMA_CONFIG["supported"])
DEVELOPMENT_VERSIONS = cast(list[str], SCHEMA_CONFIG["development"])


@pytest.fixture(scope="session")
def repository_root() -> Path:
    return REPOSITORY_ROOT


@pytest.fixture(params=[*SUPPORTED_VERSIONS, *DEVELOPMENT_VERSIONS])
def version(request: pytest.FixtureRequest) -> str:
    return cast(str, request.param)


@pytest.fixture(params=SUPPORTED_VERSIONS)
def supported_version(request: pytest.FixtureRequest) -> str:
    return cast(str, request.param)


@pytest.fixture(scope="session")
def schema_config() -> dict[str, object]:
    return SCHEMA_CONFIG
