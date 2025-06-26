from lxml import etree
from datetime import datetime
import os
import sys
import tempfile
import shutil

XSD_NS = "http://www.w3.org/2001/XMLSchema"
NSMAP = {"xs": XSD_NS}
INCLUDE_TAG = f"{{{XSD_NS}}}include"

included_files = set()

def resolve_includes(tree, base_path):
    root = tree.getroot()
    includes = root.findall(INCLUDE_TAG)
    for include in includes:
        href = include.attrib.get("schemaLocation")
        if not href:
            continue
        included_path = os.path.normpath(os.path.join(base_path, href))
        if included_path in included_files:
            print(f"Already included: {included_path}")
            root.remove(include)
            continue
        print(f"Parsing and including: {included_path}")
        included_tree = etree.parse(included_path, etree.XMLParser(remove_blank_text=True))
        resolve_includes(included_tree, os.path.dirname(included_path))
        included_root = included_tree.getroot()
        for child in included_root:
            if child.tag != INCLUDE_TAG:
                root.append(child)
        root.remove(include)
        included_files.add(included_path)

def main():
    if len(sys.argv) != 3:
        print("Usage: python combine_schema.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    print(f"Input file: {input_file}")
    print(f"Output file: {output_file}")

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    parser = etree.XMLParser(remove_blank_text=True)
    print("Parsing master schema...")
    master_tree = etree.parse(input_file, parser)
    resolve_includes(master_tree, os.path.dirname(input_file))

    root = master_tree.getroot()
    comment = etree.Comment(
    f"""
  This schema file was automatically generated from modular XSD components.
  Provided by the iTop-schema project by Björn Rudner.

  Project website: https://rudnerbjoern.github.io/iTop-schema/
  GitHub repository: https://github.com/rudnerbjoern/iTop-schema

  Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC

  Use this file to validate your iTop datamodels with confidence and consistency.
    """
    )
    root.addprevious(comment)

    # Write to a temporary file first
    with tempfile.NamedTemporaryFile("wb", delete=False) as tmp:
        temp_path = tmp.name
        print(f"Writing combined schema to temporary file: {temp_path}")
        master_tree.write(
            tmp,
            pretty_print=True,
            xml_declaration=True,
            encoding="UTF-8"
        )

    print(f"Moving temporary file to final destination: {output_file}")
    shutil.move(temp_path, output_file)
    print(f"✅ Combined schema written to: {output_file}")

if __name__ == "__main__":
    main()
