from pathlib import Path

import pytest
from lxml import etree

from itop_schema.validation import validate_xml

USE_CASE_ROOT = Path(__file__).parent / "use_cases" / "3.2"
VALID_USE_CASES = sorted((USE_CASE_ROOT / "valid").glob("*.xml"))
INVALID_USE_CASES = sorted((USE_CASE_ROOT / "invalid").glob("*.xml"))
KNOWN_LIMITATIONS = [
    pytest.param(
        USE_CASE_ROOT / "known_limitations" / "portal-brick.xml",
        marks=pytest.mark.xfail(
            strict=True,
            reason="Portal brick xsi:type values are not represented by the 3.2 schema",
        ),
    ),
]


@pytest.mark.parametrize("xml_path", VALID_USE_CASES, ids=lambda path: path.stem)
def test_3_2_schema_accepts_valid_use_case(repository_root: Path, xml_path: Path) -> None:
    validate_xml(repository_root / "3.2" / "itop_design.xsd", xml_path)


@pytest.mark.parametrize("xml_path", INVALID_USE_CASES, ids=lambda path: path.stem)
def test_3_2_schema_rejects_invalid_use_case(repository_root: Path, xml_path: Path) -> None:
    with pytest.raises(etree.DocumentInvalid):
        validate_xml(repository_root / "3.2" / "itop_design.xsd", xml_path)


@pytest.mark.parametrize("xml_path", KNOWN_LIMITATIONS, ids=lambda parameter: parameter.stem)
def test_3_2_schema_known_limitation(repository_root: Path, xml_path: Path) -> None:
    validate_xml(repository_root / "3.2" / "itop_design.xsd", xml_path)


@pytest.mark.parametrize("schema_path", ["itop_design.xsd", "dist/3.2/itop_design.xsd"])
def test_3_2_public_schemas_accept_attribute_class(
    repository_root: Path,
    schema_path: str,
) -> None:
    validate_xml(repository_root / schema_path, USE_CASE_ROOT / "valid" / "attribute-class.xml")


@pytest.mark.parametrize("schema_path", ["itop_design.xsd", "dist/3.2/itop_design.xsd"])
def test_3_2_public_schemas_accept_attribute_oql(
    repository_root: Path,
    schema_path: str,
) -> None:
    validate_xml(repository_root / schema_path, USE_CASE_ROOT / "valid" / "attribute-oql.xml")


@pytest.mark.parametrize("schema_path", ["itop_design.xsd", "dist/3.2/itop_design.xsd"])
def test_3_2_public_schemas_accept_optional_transition_action_id(
    repository_root: Path,
    schema_path: str,
) -> None:
    validate_xml(
        repository_root / schema_path,
        USE_CASE_ROOT / "valid" / "transition-actions-optional-id.xml",
    )
