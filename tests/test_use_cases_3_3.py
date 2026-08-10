from pathlib import Path

import pytest
from lxml import etree

from itop_schema.validation import validate_xml

USE_CASE_ROOT = Path(__file__).parent / "use_cases" / "3.3"
VALID_USE_CASES = sorted((USE_CASE_ROOT / "valid").glob("*.xml"))
INVALID_USE_CASES = sorted((USE_CASE_ROOT / "invalid").glob("*.xml"))
KNOWN_LIMITATIONS = [
    pytest.param(
        USE_CASE_ROOT / "known_limitations" / "portal-brick.xml",
        marks=pytest.mark.xfail(
            strict=True,
            reason="Portal brick xsi:type values are not represented by the 3.3 schema",
        ),
    ),
]


@pytest.mark.parametrize("xml_path", VALID_USE_CASES, ids=lambda path: path.stem)
def test_3_3_schema_accepts_valid_use_case(repository_root: Path, xml_path: Path) -> None:
    validate_xml(repository_root / "3.3" / "itop_design.xsd", xml_path)


@pytest.mark.parametrize("xml_path", INVALID_USE_CASES, ids=lambda path: path.stem)
def test_3_3_schema_rejects_invalid_use_case(repository_root: Path, xml_path: Path) -> None:
    with pytest.raises(etree.DocumentInvalid):
        validate_xml(repository_root / "3.3" / "itop_design.xsd", xml_path)


@pytest.mark.parametrize("xml_path", KNOWN_LIMITATIONS, ids=lambda parameter: parameter.stem)
def test_3_3_schema_known_limitation(repository_root: Path, xml_path: Path) -> None:
    validate_xml(repository_root / "3.3" / "itop_design.xsd", xml_path)
