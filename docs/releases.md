# Schema releases

`schemas.json` is the canonical registry for schema versions:

- `latest` identifies the version referenced by `/itop_design.xsd`.
- `supported` lists stable versioned public schemas.
- `development` lists schemas that are maintained but not yet stable.

## Release checklist

1. Move the release version from `development` to `supported` in
   `schemas.json`.
2. Set `latest` to the newest released iTop version.
3. Update `/itop_design.xsd` so its schema version and `xs:include` target the
   configured latest release.
4. Regenerate distributions with `scripts/update-dist.ps1`.
5. Update the supported-version links in `README.md`.
6. Run `scripts/tests/run-tests.ps1` and review all generated changes.

The stable paths `/itop_design.xsd` and `/<version>/itop_design.xsd` are a
public compatibility contract. Never move or remove them as part of routine
cleanup.
