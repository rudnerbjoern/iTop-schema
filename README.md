# iTop DataModel XSD

[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?logo=git&style=flat)](https://github.com/rudnerbjoern/iTop-schema/issues)
[![Validate XSD Schema v3.2](https://github.com/rudnerbjoern/iTop-schema/actions/workflows/validate-xml.v3.2.yml/badge.svg)](https://github.com/rudnerbjoern/iTop-schema/actions/workflows/validate-xml.v3.2.yml)
[![Combine XSD Schema v3.2](https://github.com/rudnerbjoern/iTop-schema/actions/workflows/combine-schema.v3.2.yml/badge.svg)](https://github.com/rudnerbjoern/iTop-schema/actions/workflows/combine-schema.v3.2.yml)

This project provides an **XSD schema** to validate `datamodel.my-module.xml`
files used in the [iTop CMDB software](https://www.itophub.io).

The goal is to catch **syntax errors** and **inconsistencies** in your datamodel
files *before* importing them into iTop.

Keep in mind that this schema definition does not guarantee that your datamodel
file is fully supported by iTop.
Always use the [iTop toolkit](https://github.com/Combodo/itop-toolkit-community/releases)
to fully verify your extension and ensure compatibility with iTop.

## Current status

Supported iTop design versions and URL to use to reference the schema:

- [Latest](https://rudnerbjoern.github.io/iTop-schema/itop_design.xsd):
  This will always point to the datamodel reference version from the latest
  release (STS or LTS) of iTop.
- [Version 3.2](https://rudnerbjoern.github.io/iTop-schema/3.2/itop_design.xsd):
  This version is released with iTop 3.2 LTS in August 2024, see also the
  [schema changes](https://www.itophub.io/wiki/page?id=latest:customization:xml_reference#version_32).

The project is in an **early stage**:

- The XSD is still **incomplete**.
- Many **errors and gaps** are [expected](#known-issues).

## Usage

You can either:

  1. Use the schema [offline](#offline).
  2. Feed it directly into a [validator tool](#validator-tool).
  3. Update your [datamodel](#datamodel) to reference the schema.

### Offline

  1. Download the latest `itop_design.xsd` file from [dist](dist/) for the
     version you want to validate against.
  2. Validate your `datamodel.xml` with your preferred XML validator or directly
     include it in your project.

### Validator tool

#### xmllint

```bash
xmllint --noout --schema https://rudnerbjoern.github.io/iTop-schema/itop_design.xsd datamodel.my-module.xml
```

### Datamodel

Change the top of your `datamodel.my-module.xml` to this:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<itop_design version="3.2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:noNamespaceSchemaLocation="https://rudnerbjoern.github.io/iTop-schema/itop_design.xsd">
```

Your IDE will (probably) do the rest.

If you are not yet using an IDE, you might try [Visual Studio Code](https://code.visualstudio.com)
by Microsoft and the [XML extension](https://marketplace.visualstudio.com/items?itemName=redhat.vscode-xml)
by Red Hat.

> [!WARNING]
> When using the `xml-model` declaration, the datamodel will probably not be
> processed by the iTop installer!
>
> ```xml
> <?xml version="1.0" encoding="UTF-8"?>
> <?xml-model href="https://rudnerbjoern.github.io/iTop-schema/itop_design.xsd"?>
> <itop_design xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="3.2">
> ```

## Extending the schema for your own definitions

You can extend the provided base schema with your own types by creating a local
`itop_design.xsd` file in your project and include the base schema.

Here is a minimal example:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">

  <!-- Include the official base schema -->
  <xs:include schemaLocation="https://rudnerbjoern.github.io/iTop-schema/3.2/itop_design.xsd"/>

  <!-- Add your custom type definition -->
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

This technique allows you to create additional schema constraints or custom
attributes while still relying on the iTop structure.

Take a look at [this example](https://github.com/Super-Visions/sv-geolocation/blob/master/doc/itop_design.xsd)
to see it in action.

## Known issues

<!-- TOD: Convert these to GitHub Issues -->

### Required elements

Some elements are required in different scenario's such as `_define`.
This is currently not checked against.

### constants/constant

```xml
<itop_design>
    <constants>
        <constant id="id-here" xsi:type="string" >content here</constant>
    </constants>
</itop_design>
```

Returns this error:

> **cvc-type.3.1.1**: Element 'constant' is a simple type, so it cannot have
  attributes. However, the attribute, 'id' was found.

### module_designs/module_design

```xml
<itop_design>
    <module_designs>
        <module_design id="itop-portal" xsi:type="portal" />
    </module_designs>
</itop_design>
```

Returns this error:

> **cvc-elt.4.2**: Cannot resolve 'portal' to a type definition for element 'module_design'.

### module_designs/module_design/bricks/brick

```xml
<itop_design>
    <module_designs>
        <module_design id="some-id">
            <bricks>
                <brick id="cis-for-portal-user" xsi:type="Combodo\iTop\Portal\Brick\ManageBrick">
                    <!-- brick content -->
                </brick>
            </bricks>
        </module_design>
    </module_designs>
</itop_design>
```

Returns this error:

> **cvc-attribute.3**: The value 'Combodo\iTop\Portal\Brick\ManageBrick' of
  attribute 'xsi:type' on element 'brick' is not valid with respect to its type,
  'QName'.

### branding/themes/theme/imports/import

```xml
<itop_design>
    <branding>
        <themes>
            <theme id="theme-id">
                <imports>
                    <import id="import-id" xsi:type="variables">import-file</import>
                </imports>
            </theme>
        </themes>
    </branding>
</itop_design>
```

Returns the following errors:

> **cvc-elt.4.3**: Type 'variables' is not validly derived from the type
  definition of element 'import'.
>
> **cvc-type.3.1.1**: Element 'import' is a simple type, so it cannot have
  attributes. However, the attribute, 'id' was found.

## How to help

**Contributions are very welcome!**

- If you have experience with iTop data models or XSD, please help us improve
  this schema.
- Issues, suggestions and pull requests are highly appreciated.
- Testing with real-world `datamodel.xml` files is extremely helpful.

If you would like to contribute, please check the [issues](https://github.com/rudnerbjoern/iTop-schema/issues)
or open a pull request.

## Contributors

Thanks to everyone who has contributed to this project!

Special thanks to:

- [@Hipska](https://github.com/Hipska) — for valuable additions, corrections,
  and improvements to the XSD.
