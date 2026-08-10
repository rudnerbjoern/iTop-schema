# Combined XSD Schemas for iTop

This directory contains **automatically generated** XSD files for the
[iTop CMDB system](https://www.combodo.com/itop).

## ⚠️ Do not edit manually

All files in this folder are generated from the versioned schema sources.
Do not edit them manually; use `scripts/update-dist.ps1` and commit the generated
changes together with their inputs. CI verifies that both remain synchronized.

## 📦 Purpose

These files are intended for **external use**:

- You can download and include them in your own iTop-related projects
- Each file is self-contained – all referenced definitions via `xs:include` are
  already merged
- They are validated and formatted as part of the CI pipeline

## ℹ️ Learn more

For details, visit the project homepage:
👉 [https://rudnerbjoern.github.io/iTop-schema/](https://rudnerbjoern.github.io/iTop-schema/)
