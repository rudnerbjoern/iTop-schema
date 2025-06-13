# iTop DataModel XSD

[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat-square)](https://github.com/rudnerbjoern/iTop-schema/issues)

This project provides an **XSD schema** to validate `datamodel.xxx.xml` files used in the [iTop CMDB software](https://www.combodo.com/itop).

The goal is to catch **syntax errors** and **inconsistencies** in your iTop data models *before* importing them into iTop.

## Quickstart

Change the second line of your `datamodel.xml` to this:

```xml
<itop_design version="3.2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://rudnerbjoern.github.io/iTop-schema/itop_design.xsd">
```

This definition will always point to the latest stable version of the schema for iTop (currently version 3.2).

Your IDE will (probably) do the rest.

If you are not yet using an IDE you might try [Visual Studio Code](https://code.visualstudio.com/) by Microsoft and the [XML extension](https://marketplace.visualstudio.com/items?itemName=redhat.vscode-xml) by Red Hat.

Keep in mind that this schema definition does not guarantee that your datamodel file is fully supported by iTop.
The schema has many optional elements and attributes that might be mandatory in different use cases.

Always use the [iTop toolkit](https://github.com/Combodo/itop-toolkit-community) to fully verify your extension and ensure compatibility with iTop.

## Current Status

- Supported iTop design versions:
  - [Version 3.2](https://www.itophub.io/wiki/page?id=latest:customization:xml_reference#version_32)
- The project is in an **early stage**:
  - The XSD is still **incomplete**.
  - Many **errors and gaps** are expected.
  - More advanced validations (e.g. for attribute types and relations) are not yet fully implemented.

## How to Help

**Contributions are very welcome!**

- If you have experience with iTop data models or XSD, please help us improve this schema.
- Issues, suggestions, and pull requests are highly appreciated.
- Testing with real-world `datamodel.xml` files is extremely helpful.

## Usage

You can either:

  1. Download the latest `itop_design.xsd` file.
  2. Validate your `datamodel.xml` with your preferred XML validator.

or directly link it into your datamodel like this:

### Latest Version

This will always point to the latest available version of the schema definition:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<itop_design version="3.2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://rudnerbjoern.github.io/iTop-schema/itop_design.xsd">
```

### Specific Version

There is only one version available at the moment. This might change in the future when newer versions of iTop get released.

#### iTop 3.2

```xml
<?xml version="1.0" encoding="UTF-8"?>
<itop_design version="3.2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="https://rudnerbjoern.github.io/iTop-schema/3.2/itop_design.xsd">
```

### WARNING

When using the `xml-model` declaration the datamodel will not be processed by the iTop installer!

```xml
<?xml version="1.0" encoding="UTF-8"?>
<?xml-model href="https://rudnerbjoern.github.io/iTop-schema/3.2/itop_design.xsd"?>
<itop_design xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="3.2">
```

or use a tool like `xmllint`:

```bash
xmllint --noout --schema https://rudnerbjoern.github.io/iTop-schema/itop_design.xsd datamodel.xml
```

## Contributing

We welcome contributions of all kinds!
If you would like to contribute, please check the [issues](https://github.com/rudnerbjoern/iTop-schema/issues) or open a pull request.

## Contributors

Thanks to everyone who has contributed to this project!

Special thanks to:

- [@Hipska](https://github.com/Hipska) — for valuable additions, corrections, and improvements to the XSD.
