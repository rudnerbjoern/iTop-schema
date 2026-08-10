# Known schema limitations

The schemas are still incomplete. The examples below document known iTop data
model constructs that are not currently represented correctly.

Please check the project's
[open issues](https://github.com/rudnerbjoern/iTop-schema/issues) before
reporting another occurrence.

## Required elements

Some elements are required only in specific scenarios, such as `_define`.
These conditional requirements are not currently validated.

## `constants/constant`

```xml
<itop_design>
    <constants>
        <constant id="id-here" xsi:type="string">content here</constant>
    </constants>
</itop_design>
```

Returns this error:

> **cvc-type.3.1.1**: Element 'constant' is a simple type, so it cannot have
> attributes. However, the attribute, 'id' was found.

## `module_designs/module_design`

```xml
<itop_design>
    <module_designs>
        <module_design id="itop-portal" xsi:type="portal"/>
    </module_designs>
</itop_design>
```

Returns this error:

> **cvc-elt.4.2**: Cannot resolve 'portal' to a type definition for element
> 'module_design'.

## `module_designs/module_design/bricks/brick`

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

> **cvc-attribute.3**: The value
> 'Combodo\iTop\Portal\Brick\ManageBrick' of attribute 'xsi:type' on element
> 'brick' is not valid with respect to its type, 'QName'.

## `branding/themes/theme/imports/import`

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

Returns these errors:

> **cvc-elt.4.3**: Type 'variables' is not validly derived from the type
> definition of element 'import'.
>
> **cvc-type.3.1.1**: Element 'import' is a simple type, so it cannot have
> attributes. However, the attribute, 'id' was found.
