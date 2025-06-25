from lxml import etree
import os
import sys

XSD_NS = "http://www.w3.org/2001/XMLSchema"
NSMAP = {"xs": XSD_NS}
INCLUDE_TAG = f"{{{XSD_NS}}}include"

if len(sys.argv) != 3:
    print("Usage: python combine_schema.py <input_file> <output_file>")
    sys.exit(1)

MASTER_FILE = sys.argv[1]
OUTPUT_FILE = sys.argv[2]

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
            root.remove(include)
            continue
        print(f"Including: {included_path}")
        included_tree = etree.parse(included_path, etree.XMLParser(remove_blank_text=True))
        resolve_includes(included_tree, os.path.dirname(included_path))
        included_root = included_tree.getroot()
        for child in included_root:
            root.append(child)
        root.remove(include)
        included_files.add(included_path)

os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

parser = etree.XMLParser(remove_blank_text=True)
master_tree = etree.parse(MASTER_FILE, parser)
resolve_includes(master_tree, os.path.dirname(MASTER_FILE))

# Add project comment before root
root = master_tree.getroot()
comment = etree.Comment(
    """
  This schema file was automatically generated from modular XSD components.
  Provided by the iTop-schema project by Björn Rudner.

  Project website: https://rudnerbjoern.github.io/iTop-schema/
  GitHub repository: https://github.com/rudnerbjoern/iTop-schema

  Use this file to validate your iTop datamodels with confidence and consistency.
    """
)
root.addprevious(comment)

# Write formatted output
etree.ElementTree(root).write(
    OUTPUT_FILE,
    pretty_print=True,
    xml_declaration=True,
    encoding="UTF-8"
)

print(f"✅ Combined schema written to: {OUTPUT_FILE}")
