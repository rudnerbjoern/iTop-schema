from pathlib import Path

from lxml import etree


def create_xml_parser(*, remove_blank_text: bool = False) -> etree.XMLParser:
    """Create an XML parser without DTD, entity, or network resolution."""
    return etree.XMLParser(
        load_dtd=False,
        no_network=True,
        remove_blank_text=remove_blank_text,
        resolve_entities=False,
    )


def parse_xml(path: Path, *, remove_blank_text: bool = False) -> etree._ElementTree:
    if not path.is_file():
        raise FileNotFoundError(f"Required file does not exist: {path}")

    document = etree.parse(
        str(path),
        create_xml_parser(remove_blank_text=remove_blank_text),
    )
    if document.docinfo.doctype:
        raise ValueError(f"DOCTYPE declarations are not allowed: {path}")
    return document
