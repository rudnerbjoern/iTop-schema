import argparse
import sys
from pathlib import Path

from lxml import etree

from .xml import parse_xml


def validate_xml(xsd_path: Path, xml_path: Path) -> None:
    """Raise an lxml validation exception if XML does not match the schema."""
    schema_document = parse_xml(xsd_path)
    schema = etree.XMLSchema(schema_document)
    xml_document = parse_xml(xml_path)
    schema.assertValid(xml_document)


def format_error_log(error_log: etree._ListErrorLog) -> str:
    return "\n".join(
        f"{entry.filename or '<unknown>'}:{entry.line}:{entry.column}: {entry.message}"
        for entry in error_log
    )


def create_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate an XML document against an XML Schema.")
    parser.add_argument("xsd_path", type=Path, help="XSD schema file")
    parser.add_argument("xml_path", type=Path, help="XML document to validate")
    return parser


def main(arguments: list[str] | None = None) -> int:
    parsed_arguments = create_argument_parser().parse_args(arguments)
    try:
        validate_xml(parsed_arguments.xsd_path, parsed_arguments.xml_path)
    except etree.DocumentInvalid as error:
        details = format_error_log(error.error_log)
        print(f"XML validation failed:\n{details or error}", file=sys.stderr)
        return 1
    except etree.XMLSchemaParseError as error:
        details = format_error_log(error.error_log)
        print(f"XML Schema is invalid:\n{details or error}", file=sys.stderr)
        return 1
    except etree.XMLSyntaxError as error:
        details = format_error_log(error.error_log)
        print(f"XML syntax error:\n{details or error}", file=sys.stderr)
        return 1
    except etree.LxmlError as error:
        print(f"XML processing failed: {error}", file=sys.stderr)
        return 1
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print("✅ XML is valid against schema.")
    return 0
