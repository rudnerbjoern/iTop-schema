from pathlib import Path

import pytest
from lxml import etree

from itop_schema.validation import validate_xml

USE_CASE_ROOT = Path(__file__).parent / "use_cases" / "extension"
VALID_USE_CASES = sorted((USE_CASE_ROOT / "valid").glob("*.xml"))
INVALID_USE_CASES = sorted((USE_CASE_ROOT / "invalid").glob("*.xml"))


@pytest.mark.parametrize("xml_path", VALID_USE_CASES, ids=lambda path: path.stem)
def test_extension_schema_accepts_valid_use_case(repository_root: Path, xml_path: Path) -> None:
    validate_xml(repository_root / "extension.xsd", xml_path)


@pytest.mark.parametrize("xml_path", INVALID_USE_CASES, ids=lambda path: path.stem)
def test_extension_schema_rejects_invalid_use_case(repository_root: Path, xml_path: Path) -> None:
    with pytest.raises(etree.DocumentInvalid):
        validate_xml(repository_root / "extension.xsd", xml_path)
