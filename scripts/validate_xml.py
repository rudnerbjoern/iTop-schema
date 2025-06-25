import os
import sys
import lxml.etree as ET

if len(sys.argv) != 3:
    print("Usage: python validate_xml.py <XSD_PATH> <XML_PATH>")
    sys.exit(1)

XSD_PATH = sys.argv[1]
XML_PATH = sys.argv[2]

for path in [XSD_PATH, XML_PATH]:
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Missing required file: {path}")

schema = ET.XMLSchema(file=XSD_PATH)
parser = ET.XMLParser(schema=schema)

with open(XML_PATH, "rb") as f:
    ET.parse(f, parser)

print("✅ XML is valid against schema.")
