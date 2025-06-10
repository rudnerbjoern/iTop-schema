# iTop DataModel XSD

This project provides an **XSD schema** to validate `datamodel.xxx.xml` files used in the [iTop CMDB software](https://www.combodo.com/itop).

The goal is to catch **syntax errors** and **inconsistencies** in your iTop data models *before* importing them into iTop.

## Current Status

- Supported iTop design version:
  `<itop_design version="3.2">`
- The project is in an **early stage**:
  - The XSD is still **incomplete**.
  - Many **errors and gaps** are expected.
  - More advanced validations (e.g. for attribute types and relations) are not yet implemented.

## How to Help

**Contributions are very welcome!**

- If you have experience with iTop data models or XSD, please help us improve this schema.
- Issues, suggestions, and pull requests are highly appreciated.
- Testing with real-world `datamodel.xml` files is extremely helpful.

## Usage

You can either:

  1. Download the latest `datamodel.v3.2.xsd` file.
  2. Validate your `datamodel.xml` with your preferred XML validator.

or directly link it into your datamodel like this:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<?xml-model href="datamodel.v3.2.xsd"?>
<itop_design xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="3.2">
```
