import argparse
import os
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlparse

from lxml import etree

from .xml import parse_xml

XSD_NS = "http://www.w3.org/2001/XMLSchema"
SCHEMA_TAG = f"{{{XSD_NS}}}schema"
INCLUDE_TAG = f"{{{XSD_NS}}}include"
DOCUMENTATION_TAG = f"{{{XSD_NS}}}documentation"


def resolve_include_path(schema_location: str, base_path: Path, root_path: Path) -> Path:
    """Resolve an include and ensure that it stays inside the schema directory."""
    parsed_location = urlparse(schema_location)
    if parsed_location.scheme or parsed_location.netloc:
        raise ValueError(f"Only local schema includes are supported: {schema_location}")

    included_path = (base_path / schema_location).resolve()
    if not included_path.is_relative_to(root_path):
        raise ValueError(
            f"Schema include leaves the allowed directory {root_path}: {schema_location}"
        )
    if not included_path.is_file():
        raise FileNotFoundError(f"Included schema does not exist: {included_path}")
    return included_path


def parse_schema(path: Path) -> etree._ElementTree:
    tree = parse_xml(path, remove_blank_text=True)
    if tree.getroot().tag != SCHEMA_TAG:
        raise ValueError(f"Expected an XML Schema root element in {path}")
    return tree


def merge_namespace_declarations(
    tree: etree._ElementTree,
    additional_namespaces: dict[str | None, str],
) -> etree._Element:
    """Copy namespace prefixes needed by QName-valued schema attributes."""
    root = tree.getroot()
    namespaces = dict(root.nsmap)

    for prefix, namespace in additional_namespaces.items():
        existing_namespace = namespaces.get(prefix)
        if existing_namespace is not None and existing_namespace != namespace:
            raise ValueError(
                f"Conflicting namespace declaration for prefix {prefix!r}: "
                f"{existing_namespace!r} and {namespace!r}"
            )
        namespaces[prefix] = namespace

    if namespaces == root.nsmap:
        return root

    replacement = etree.Element(root.tag, attrib=root.attrib, nsmap=namespaces)
    replacement.text = root.text
    replacement.tail = root.tail
    for child in list(root):
        replacement.append(child)
    tree._setroot(replacement)
    return replacement


def resolve_includes(
    tree: etree._ElementTree,
    source_path: Path,
    root_path: Path,
    processing: list[Path],
    processed: set[Path],
) -> None:
    """Replace local xs:include elements recursively with their declarations."""
    root = tree.getroot()

    for include in list(root.findall(INCLUDE_TAG)):
        schema_location = include.get("schemaLocation")
        if not schema_location:
            raise ValueError(f"xs:include without schemaLocation in {source_path}")

        included_path = resolve_include_path(
            schema_location,
            source_path.parent,
            root_path,
        )
        if included_path in processing:
            chain = " -> ".join(str(path) for path in [*processing, included_path])
            raise ValueError(f"Cyclic schema include detected: {chain}")
        if included_path in processed:
            root.remove(include)
            continue

        included_tree = parse_schema(included_path)
        processing.append(included_path)
        try:
            resolve_includes(
                included_tree,
                included_path,
                root_path,
                processing,
                processed,
            )
        finally:
            processing.pop()

        root = merge_namespace_declarations(tree, included_tree.getroot().nsmap)
        for child in list(included_tree.getroot()):
            root.insert(root.index(include), child)
        root.remove(include)
        processed.add(included_path)


def add_generation_comment(tree: etree._ElementTree) -> None:
    comment = etree.Comment(
        """
  This schema file was automatically generated from modular XSD components.
  Provided by the iTop-schema project by Björn Rudner.

  Project website: https://rudnerbjoern.github.io/iTop-schema/
  GitHub repository: https://github.com/rudnerbjoern/iTop-schema

  Use this file to validate your iTop datamodels with confidence and consistency.
    """
    )
    tree.getroot().addprevious(comment)


def normalize_documentation(tree: etree._ElementTree) -> None:
    """Normalize whitespace in schema documentation deterministically."""
    for documentation in tree.getroot().iter(DOCUMENTATION_TAG):
        documentation.text = " ".join("".join(documentation.itertext()).split())
        for child in list(documentation):
            documentation.remove(child)


def write_atomically(tree: etree._ElementTree, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            dir=output_path.parent,
            prefix=f".{output_path.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)
            tree.write(
                temporary_file,
                pretty_print=True,
                xml_declaration=True,
                encoding="UTF-8",
            )
        os.replace(temporary_path, output_path)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def combine_schema(input_path: Path, output_path: Path) -> None:
    """Flatten local XSD includes and atomically write a compiled schema."""
    input_path = input_path.resolve()
    output_path = output_path.resolve()
    if not input_path.is_file():
        raise FileNotFoundError(f"Input schema does not exist: {input_path}")

    master_tree = parse_schema(input_path)
    resolve_includes(
        master_tree,
        input_path,
        input_path.parent,
        processing=[input_path],
        processed=set(),
    )

    etree.XMLSchema(master_tree)
    normalize_documentation(master_tree)
    add_generation_comment(master_tree)
    write_atomically(master_tree, output_path)


def create_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Combine local xs:include declarations into one XML Schema file."
    )
    parser.add_argument("input_file", type=Path, help="Master XSD file")
    parser.add_argument("output_file", type=Path, help="Combined XSD output file")
    return parser


def main(arguments: list[str] | None = None) -> int:
    parsed_arguments = create_argument_parser().parse_args(arguments)
    try:
        combine_schema(parsed_arguments.input_file, parsed_arguments.output_file)
    except (OSError, ValueError, etree.LxmlError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(f"✅ Combined schema written to: {parsed_arguments.output_file.resolve()}")
    return 0
