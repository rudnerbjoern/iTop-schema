# iTop DataModel XSD

[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?logo=git&style=flat)](https://github.com/rudnerbjoern/iTop-schema/issues)
[![Validate XSD Schemas](https://github.com/rudnerbjoern/iTop-schema/actions/workflows/validate-xml.yml/badge.svg)](https://github.com/rudnerbjoern/iTop-schema/actions/workflows/validate-xml.yml)
[![Combine XSD Schemas](https://github.com/rudnerbjoern/iTop-schema/actions/workflows/combine-schema.yml/badge.svg)](https://github.com/rudnerbjoern/iTop-schema/actions/workflows/combine-schema.yml)

This project provides a community-maintained **XSD schema** for validating
`datamodel.my-module.xml` files used by the
[iTop CMDB software](https://www.itophub.io).

It helps detect syntax errors and structural inconsistencies before a data
model is imported into iTop.

> [!IMPORTANT]
> Successful schema validation does not guarantee that a data model is fully
> compatible with iTop. Always verify extensions with the
> [iTop toolkit](https://github.com/Combodo/itop-toolkit-community/releases)
> before deployment.

## Quick start

Validate an iTop 3.2 data model with `xmllint`:

```bash
xmllint --noout \
  --schema https://rudnerbjoern.github.io/iTop-schema/3.2/itop_design.xsd \
  datamodel.my-module.xml
```

For IDE validation, reference the same versioned schema in the data model:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<itop_design version="3.2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:noNamespaceSchemaLocation="https://rudnerbjoern.github.io/iTop-schema/3.2/itop_design.xsd">
```

## Supported versions

| Version | Status                  | Schema                             |
| ------- | ----------------------- | ---------------------------------- |
| Latest  | Currently points to 3.2 | [Latest endpoint][latest-schema]   |
| 3.2     | Supported               | [Version 3.2 endpoint][schema-3-2] |
| 3.3     | In development          | Not published                      |

The `Latest` endpoint follows the release configured by this project and may
change to a newer iTop STS or LTS version. Use a versioned URL when validation
must remain reproducible across future releases.

iTop 3.2 LTS was released in August 2024. See the corresponding
[schema changes](https://www.itophub.io/wiki/page?id=latest:customization:xml_reference#version_32)
in the iTop documentation.

The project remains at an early stage. The schemas are incomplete, and some
iTop data model constructs are not represented correctly yet. See the
[known limitations](docs/known-issues.md) for examples.

## Usage

### Reference a schema from a data model

For stable validation, reference the schema matching the targeted iTop
version:

```xml
xsi:noNamespaceSchemaLocation="https://rudnerbjoern.github.io/iTop-schema/3.2/itop_design.xsd"
```

Use the following endpoint only when automatically following this project's
latest supported version is intentional:

```xml
xsi:noNamespaceSchemaLocation="https://rudnerbjoern.github.io/iTop-schema/itop_design.xsd"
```

Visual Studio Code users can use the
[XML extension by Red Hat](https://marketplace.visualstudio.com/items?itemName=redhat.vscode-xml)
for schema-based validation and completion.

### Validate from the command line

Any XML validator with XSD support can use the published schema. For example:

```bash
xmllint --noout \
  --schema https://rudnerbjoern.github.io/iTop-schema/3.2/itop_design.xsd \
  datamodel.my-module.xml
```

### Validate offline

The versioned files such as `3.2/itop_design.xsd` are the published schema
entry points and can reference additional XSD files from the same version
directory.

The generated files below [`dist/`](dist/) are self-contained: all local
`xs:include` references have already been merged. Download
[`dist/3.2/itop_design.xsd`](dist/3.2/itop_design.xsd) when validation must work
without network access or accompanying schema files.

> [!WARNING]
> A data model containing an `xml-model` processing instruction may not be
> accepted by the iTop installer. Prefer `xsi:noNamespaceSchemaLocation` for
> editor integration.
>
> ```xml
> <?xml version="1.0" encoding="UTF-8"?>
> <?xml-model href="https://rudnerbjoern.github.io/iTop-schema/3.2/itop_design.xsd"?>
> <itop_design xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="3.2">
> ```

## Extend the schema for custom definitions

Create a local `itop_design.xsd` when a module requires additional types or
constraints. Include the community-maintained versioned schema and add custom
definitions locally:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">

  <!-- Include the community-maintained base schema -->
  <xs:include schemaLocation="https://rudnerbjoern.github.io/iTop-schema/3.2/itop_design.xsd"/>

  <xs:complexType name="AttributeMyOwnDefinition">
    <xs:complexContent>
      <xs:extension base="AttributeDefinition">
        <xs:sequence>
          <xs:element name="sql" type="xs:string"/>
          <xs:element name="default_value" type="xs:string"/>
          <xs:element name="is_null_allowed" type="xs:boolean"/>
          <xs:element name="own_value" type="xs:nonNegativeInteger" minOccurs="0" default="150"/>
          <xs:element name="other_value" type="xs:string" minOccurs="0"/>
        </xs:sequence>
      </xs:extension>
    </xs:complexContent>
  </xs:complexType>

</xs:schema>
```

This keeps project-specific definitions separate while retaining the shared
iTop data model structure. See the
[sv-geolocation example](https://github.com/Super-Visions/sv-geolocation/blob/master/doc/itop_design.xsd)
for a real-world implementation.

## Development and testing

See the [testing guide](docs/testing.md) for local setup, Pytest, coverage,
VS Code Test Explorer, and the PowerShell test lifecycle.

Maintainers should follow the [release guide](docs/releases.md) when publishing
or changing supported schema versions.

## Contributing

Contributions are welcome, particularly:

- corrections and additions to the schemas;
- test cases based on real-world iTop data models;
- reports for unsupported or incorrectly validated constructs.

Review the [known limitations](docs/known-issues.md) and
[open issues](https://github.com/rudnerbjoern/iTop-schema/issues), or submit a
pull request.

## Contributors

Thanks to everyone who has contributed to this project.

Special thanks to:

- [@Hipska](https://github.com/Hipska) — for valuable additions, corrections,
  and improvements to the XSD.

[latest-schema]: https://rudnerbjoern.github.io/iTop-schema/itop_design.xsd
[schema-3-2]: https://rudnerbjoern.github.io/iTop-schema/3.2/itop_design.xsd
