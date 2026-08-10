from pathlib import Path
from typing import cast

import pytest
from lxml import etree

from itop_schema import validation
from itop_schema.validation import main, validate_xml


def test_latest_public_schema_targets_configured_release(
    repository_root: Path,
    schema_config: dict[str, object],
) -> None:
    latest_version = cast(str, schema_config["latest"])
    supported_versions = cast(list[str], schema_config["supported"])
    schema_tree = etree.parse(str(repository_root / "itop_design.xsd"))

    etree.XMLSchema(schema_tree)

    assert latest_version in supported_versions
    assert schema_tree.getroot().get("version") == latest_version
    assert schema_tree.xpath(
        "/xs:schema/xs:include/@schemaLocation",
        namespaces={"xs": "http://www.w3.org/2001/XMLSchema"},
    ) == [f"{latest_version}/itop_design.xsd"]


def test_versioned_public_schema_compiles(
    repository_root: Path,
    supported_version: str,
) -> None:
    etree.XMLSchema(etree.parse(str(repository_root / supported_version / "itop_design.xsd")))


def test_repository_datamodel_is_valid(repository_root: Path, version: str) -> None:
    validate_xml(
        repository_root / version / "itop_design.xsd",
        repository_root / "tests" / "fixtures" / version / "datamodel.must-validate.xml",
    )


def test_invalid_document_is_rejected(repository_root: Path, tmp_path: Path) -> None:
    invalid_xml = tmp_path / "invalid.xml"
    invalid_xml.write_text("<not_itop_design/>", encoding="utf-8")

    with pytest.raises(etree.DocumentInvalid):
        validate_xml(repository_root / "3.2" / "itop_design.xsd", invalid_xml)


def test_doctype_is_rejected(repository_root: Path, tmp_path: Path) -> None:
    xml_with_doctype = tmp_path / "doctype.xml"
    xml_with_doctype.write_text(
        """\
<!DOCTYPE itop_design [
  <!ENTITY local-file SYSTEM "file:///etc/passwd">
]>
<itop_design>&local-file;</itop_design>
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="DOCTYPE declarations are not allowed"):
        validate_xml(repository_root / "3.2" / "itop_design.xsd", xml_with_doctype)


def test_missing_file_is_reported(repository_root: Path, tmp_path: Path) -> None:
    missing_xml = tmp_path / "missing.xml"

    with pytest.raises(FileNotFoundError, match="Required file does not exist"):
        validate_xml(repository_root / "3.2" / "itop_design.xsd", missing_xml)


def test_cli_reports_validation_error(
    repository_root: Path,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    invalid_xml = tmp_path / "invalid.xml"
    invalid_xml.write_text("<not_itop_design/>", encoding="utf-8")

    exit_code = main([str(repository_root / "3.2" / "itop_design.xsd"), str(invalid_xml)])

    assert exit_code == 1
    assert "XML validation failed" in capsys.readouterr().err


def test_cli_reports_invalid_schema(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    invalid_schema = tmp_path / "invalid.xsd"
    xml_file = tmp_path / "document.xml"
    invalid_schema.write_text("<not-a-schema/>", encoding="utf-8")
    xml_file.write_text("<document/>", encoding="utf-8")

    exit_code = main([str(invalid_schema), str(xml_file)])

    assert exit_code == 1
    assert "XML Schema is invalid" in capsys.readouterr().err


def test_cli_reports_xml_syntax_error(
    repository_root: Path,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    malformed_xml = tmp_path / "malformed.xml"
    malformed_xml.write_text("<itop_design>", encoding="utf-8")

    exit_code = main([str(repository_root / "3.2" / "itop_design.xsd"), str(malformed_xml)])

    assert exit_code == 1
    assert "XML syntax error" in capsys.readouterr().err


def test_cli_reports_missing_file(
    repository_root: Path,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    missing_xml = tmp_path / "missing.xml"

    exit_code = main([str(repository_root / "3.2" / "itop_design.xsd"), str(missing_xml)])

    assert exit_code == 1
    assert "Required file does not exist" in capsys.readouterr().err


def test_cli_reports_generic_lxml_error(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def raise_lxml_error(_xsd_path: Path, _xml_path: Path) -> None:
        raise etree.LxmlError("processing failed")

    monkeypatch.setattr(validation, "validate_xml", raise_lxml_error)

    exit_code = main([str(tmp_path / "schema.xsd"), str(tmp_path / "document.xml")])

    assert exit_code == 1
    assert "XML processing failed: processing failed" in capsys.readouterr().err


def test_cli_reports_success(
    repository_root: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    exit_code = main(
        [
            str(repository_root / "3.2" / "itop_design.xsd"),
            str(repository_root / "tests/fixtures/3.2/datamodel.must-validate.xml"),
        ]
    )

    assert exit_code == 0
    assert "XML is valid against schema" in capsys.readouterr().out
