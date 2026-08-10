# Testing

The test suite covers schema combination, XML validation, error handling, and
the supported iTop schema versions. Test data models are stored below
`tests/fixtures/`.

The quality checks use Ruff for Python linting and formatting, Pyright for
static type checking, and PSScriptAnalyzer for PowerShell analysis.

## Prerequisites

- Python 3.14
- A Python installation with virtual environment support

## Prepare the test environment

Create a virtual environment and install the project with its test dependencies:

```bash
python -m venv .venv
.venv/bin/python -m pip install -r scripts/requirements-dev.txt
```

Direct project dependencies are pinned for reproducible setup in
`scripts/constraints.txt`. Dependabot keeps these versions current.

On Windows without WSL, use `.venv/Scripts/python.exe` instead of
`.venv/bin/python`.

## Run the tests

Run the complete suite with coverage:

```bash
.venv/bin/python -m pytest \
  --cov=itop_schema \
  --cov-report=term-missing
```

Pytest configuration, test discovery, and coverage source paths are defined in
`pyproject.toml`. The same file enforces the project-wide minimum coverage of
95 percent.

## Run the quality checks

Run Python linting, formatting validation, and static type checking directly:

```bash
.venv/bin/python -m ruff check .
.venv/bin/python -m ruff format --check .
.venv/bin/python -m pyright
```

The PowerShell lifecycle described below runs these checks and Pytest together.

## PowerShell test lifecycle

PowerShell users can prepare, run, and clean up the test environment through
the repository scripts:

```powershell
./scripts/tests/prepare-tests.ps1
./scripts/tests/run-tests.ps1
./scripts/tests/cleanup-tests.ps1
```

Recreate an existing virtual environment during preparation:

```powershell
./scripts/tests/prepare-tests.ps1 -Recreate
```

Preparation installs the project's pinned PSScriptAnalyzer version for the
current user when it is missing. PowerShell tool versions are maintained in
`scripts/tool-versions.psd1`.
Use `-SkipPowerShellAnalyzer` when only the Python environment is required.

Pass additional arguments to Pytest:

```powershell
./scripts/tests/run-tests.ps1 -AdditionalPytestArguments @("-k", "validation")
```

Preview cleanup without removing anything:

```powershell
./scripts/tests/cleanup-tests.ps1 -WhatIf
```

The cleanup script retains `.venv` by default. Remove it explicitly when
needed:

```powershell
./scripts/tests/cleanup-tests.ps1 -IncludeVirtualEnvironment
```

## VS Code Test Explorer

The workspace enables Pytest discovery in `.vscode/settings.json`. After
preparing the environment:

1. Select the Python interpreter from `.venv`.
2. Open the Testing view in VS Code.
3. Discover, run, or debug the tests individually or as a suite.

The recommended Microsoft Python extension is declared in
`.vscode/extensions.json`.

## Versioned schema use cases

Focused integration fixtures below `tests/use_cases/<version>/` validate the
actual modular `<version>/itop_design.xsd` entry points:

- `valid/` contains data model constructs the schema must accept.
- `invalid/` contains constructs the schema must reject.
- `known_limitations/` contains valid iTop constructs represented as strict
  `xfail` tests until the schema supports them.

Run only these contracts through the PowerShell lifecycle:

```powershell
./scripts/tests/run-tests.ps1 tests/test_use_cases_3_2.py -q --no-cov
./scripts/tests/run-tests.ps1 tests/test_use_cases_3_3.py -q --no-cov
```

Use small fixtures that exercise one behavior each. Add larger anonymized real
data models only as complementary end-to-end cases. Never commit original
customer or installation data; derive minimal fixtures with synthetic class,
field, module, query, and label values instead.

## Update generated schemas

`schemas.json` is the canonical list of supported and development schema
versions. After changing a schema input, regenerate every configured file:

```powershell
./scripts/update-dist.ps1
```

Alternatively, invoke the Python entry point directly:

```bash
.venv/bin/python scripts/update_dist.py
```

Commit the resulting changes below `dist/` together with their schema inputs.
The manual combine workflow repeats the generation and fails when the committed
distribution files differ.
