from pathlib import Path

import pytest
from lxml import etree

from itop_schema.combine import (
    DOCUMENTATION_TAG,
    INCLUDE_TAG,
    combine_schema,
    main,
)
from itop_schema.validation import validate_xml


def test_repository_schema_can_be_combined_and_validated(
    repository_root: Path,
    tmp_path: Path,
    version: str,
) -> None:
    output = tmp_path / version / "itop_design.xsd"

    combine_schema(repository_root / version / "itop_design.xsd", output)

    validate_xml(
        output,
        repository_root / "tests" / "fixtures" / version / "datamodel.must-validate.xml",
    )
    assert not etree.parse(str(output)).getroot().findall(INCLUDE_TAG)


def test_combined_output_is_reproducible(repository_root: Path, tmp_path: Path) -> None:
    first_output = tmp_path / "first.xsd"
    second_output = tmp_path / "second.xsd"

    combine_schema(repository_root / "3.3" / "itop_design.xsd", first_output)
    combine_schema(repository_root / "3.3" / "itop_design.xsd", second_output)

    assert first_output.read_bytes() == second_output.read_bytes()


def test_committed_distribution_is_current(
    repository_root: Path,
    tmp_path: Path,
    version: str,
) -> None:
    generated_output = tmp_path / version / "itop_design.xsd"

    combine_schema(repository_root / version / "itop_design.xsd", generated_output)

    assert (
        generated_output.read_bytes()
        == (repository_root / "dist" / version / "itop_design.xsd").read_bytes()
    )


def test_documentation_whitespace_is_normalized(tmp_path: Path) -> None:
    input_schema = tmp_path / "input.xsd"
    output_schema = tmp_path / "output.xsd"
    input_schema.write_text(
        """\
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:annotation>
    <xs:documentation>
      Several   words
      on multiple lines.
    </xs:documentation>
  </xs:annotation>
</xs:schema>
""",
        encoding="utf-8",
    )

    combine_schema(input_schema, output_schema)

    documentation = etree.parse(str(output_schema)).getroot().find(f".//{DOCUMENTATION_TAG}")
    assert documentation is not None
    assert documentation.text == "Several words on multiple lines."


def test_documentation_markup_is_flattened(tmp_path: Path) -> None:
    input_schema = tmp_path / "input.xsd"
    output_schema = tmp_path / "output.xsd"
    input_schema.write_text(
        """\
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:annotation>
    <xs:documentation>Text with <em>inline markup</em>.</xs:documentation>
  </xs:annotation>
</xs:schema>
""",
        encoding="utf-8",
    )

    combine_schema(input_schema, output_schema)

    documentation = etree.parse(str(output_schema)).getroot().find(f".//{DOCUMENTATION_TAG}")
    assert documentation is not None
    assert documentation.text == "Text with inline markup."
    assert len(documentation) == 0


def test_cyclic_includes_are_rejected(tmp_path: Path) -> None:
    first_schema = tmp_path / "a.xsd"
    second_schema = tmp_path / "b.xsd"
    first_schema.write_text(_schema_with_include("b.xsd"), encoding="utf-8")
    second_schema.write_text(_schema_with_include("a.xsd"), encoding="utf-8")

    with pytest.raises(ValueError, match="Cyclic schema include detected"):
        combine_schema(first_schema, tmp_path / "combined.xsd")


def test_include_may_not_leave_schema_directory(tmp_path: Path) -> None:
    schema_directory = tmp_path / "schemas"
    schema_directory.mkdir()
    master_schema = schema_directory / "master.xsd"
    external_schema = tmp_path / "external.xsd"
    master_schema.write_text(_schema_with_include("../external.xsd"), encoding="utf-8")
    external_schema.write_text(_empty_schema(), encoding="utf-8")

    with pytest.raises(ValueError, match="leaves the allowed directory"):
        combine_schema(master_schema, tmp_path / "combined.xsd")


def test_remote_include_is_rejected(tmp_path: Path) -> None:
    master_schema = tmp_path / "master.xsd"
    master_schema.write_text(
        _schema_with_include("https://example.com/schema.xsd"),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Only local schema includes are supported"):
        combine_schema(master_schema, tmp_path / "combined.xsd")


def test_missing_include_is_reported(tmp_path: Path) -> None:
    master_schema = tmp_path / "master.xsd"
    master_schema.write_text(_schema_with_include("missing.xsd"), encoding="utf-8")

    with pytest.raises(FileNotFoundError, match="Included schema does not exist"):
        combine_schema(master_schema, tmp_path / "combined.xsd")


def test_non_schema_root_is_rejected(tmp_path: Path) -> None:
    input_file = tmp_path / "not-a-schema.xml"
    input_file.write_text("<root/>", encoding="utf-8")

    with pytest.raises(ValueError, match="Expected an XML Schema root element"):
        combine_schema(input_file, tmp_path / "combined.xsd")


def test_include_without_location_is_rejected(tmp_path: Path) -> None:
    input_file = tmp_path / "master.xsd"
    input_file.write_text(
        '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"><xs:include/></xs:schema>',
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="xs:include without schemaLocation"):
        combine_schema(input_file, tmp_path / "combined.xsd")


def test_duplicate_include_is_merged_once(tmp_path: Path) -> None:
    included_schema = tmp_path / "included.xsd"
    master_schema = tmp_path / "master.xsd"
    included_schema.write_text(
        """\
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:simpleType name="identifier"><xs:restriction base="xs:string"/></xs:simpleType>
</xs:schema>
""",
        encoding="utf-8",
    )
    master_schema.write_text(
        """\
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:include schemaLocation="included.xsd"/>
  <xs:include schemaLocation="included.xsd"/>
</xs:schema>
""",
        encoding="utf-8",
    )

    output = tmp_path / "combined.xsd"
    combine_schema(master_schema, output)

    tree = etree.parse(str(output))
    assert (
        len(
            tree.xpath(
                "//xs:simpleType[@name='identifier']",
                namespaces={"xs": "http://www.w3.org/2001/XMLSchema"},
            )
        )
        == 1
    )


def test_conflicting_include_namespace_is_rejected(tmp_path: Path) -> None:
    included_schema = tmp_path / "included.xsd"
    master_schema = tmp_path / "master.xsd"
    included_schema.write_text(
        '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:custom="urn:two"/>',
        encoding="utf-8",
    )
    master_schema.write_text(
        """\
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:custom="urn:one">
  <xs:include schemaLocation="included.xsd"/>
</xs:schema>
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Conflicting namespace declaration"):
        combine_schema(master_schema, tmp_path / "combined.xsd")


def test_invalid_result_does_not_replace_existing_output(tmp_path: Path) -> None:
    invalid_schema = tmp_path / "invalid.xsd"
    output = tmp_path / "combined.xsd"
    invalid_schema.write_text(
        """\
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="invalid" type="missing-type"/>
</xs:schema>
""",
        encoding="utf-8",
    )
    output.write_text("existing output", encoding="utf-8")

    with pytest.raises(etree.XMLSchemaParseError):
        combine_schema(invalid_schema, output)

    assert output.read_text(encoding="utf-8") == "existing output"


def test_cli_returns_failure_for_missing_input(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    exit_code = main([str(tmp_path / "missing.xsd"), str(tmp_path / "output.xsd")])

    assert exit_code == 1
    assert "Input schema does not exist" in capsys.readouterr().err


def test_cli_reports_success(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    input_schema = tmp_path / "input.xsd"
    output_schema = tmp_path / "output.xsd"
    input_schema.write_text(_empty_schema(), encoding="utf-8")

    exit_code = main([str(input_schema), str(output_schema)])

    assert exit_code == 0
    assert output_schema.is_file()
    assert "Combined schema written" in capsys.readouterr().out


def _schema_with_include(schema_location: str) -> str:
    return f"""\
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:include schemaLocation="{schema_location}"/>
</xs:schema>
"""


def _empty_schema() -> str:
    return '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"/>\n'
