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

## Extending the Schema for Your Own Definitions

You can extend the provided base schema with your own types by creating a local `itop_design.xsd` file in your project and including the base schema.

Here is a minimal example:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">

  <!-- Include the official base schema -->
  <xs:include schemaLocation="https://raw.githubusercontent.com/rudnerbjoern/iTop-schema/refs/heads/main/3.2/itop_design.xsd"/>

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

This technique allows you to create additional schema constraints or custom attributes while still relying on the iTop structure.

Take a look at [this example by @Hipska](https://github.com/Super-Visions/sv-geolocation/blob/master/doc/itop_design.xsd) to see it in action.

## Known Issues

### constants/constant

```xml
<itop_design>
    <constants>
        <constant id="id-here" xsi:type="string" >content here</constant>
    </constants>
</itop_design>
```

has error `cvc-type.3.1.1: Element 'constant' is a simple type, so it cannot have attributes. However, the attribute, 'id' was found.`

### module_designs/module_design

```xml
<itop_design>
    <module_designs>
        <module_design id="itop-portal" xsi:type="portal" />
    </module_designs>
</itop_design>
```

has error `cvc-elt.4.2: Cannot resolve 'portal' to a type definition for element 'module_design'.`

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

has error `cvc-attribute.3: The value 'Combodo\iTop\Portal\Brick\ManageBrick' of attribute 'xsi:type' on element 'brick' is not valid with respect to its type, 'QName'.`

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

has errors

- `cvc-elt.4.3: Type 'variables' is not validly derived from the type definition of element 'import'.`
- `cvc-type.3.1.1: Element 'import' is a simple type, so it cannot have attributes. However, the attribute, 'id' was found.`

## Contributing

We welcome contributions of all kinds!
If you would like to contribute, please check the [issues](https://github.com/rudnerbjoern/iTop-schema/issues) or open a pull request.

## Contributors

Thanks to everyone who has contributed to this project!

Special thanks to:

- [@Hipska](https://github.com/Hipska) — for valuable additions, corrections, and improvements to the XSD.
