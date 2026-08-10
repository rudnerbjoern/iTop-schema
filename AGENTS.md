# Agent instructions

These instructions apply to the complete repository.

## Published schema paths

Do not move or rename the published schema files or change their public URL
contract unless the user explicitly requests it. In particular, preserve:

- `/itop_design.xsd`
- `/3.2/itop_design.xsd`
- versioned schema inputs below `3.2/` and `3.3/`
- generated schema outputs below `dist/3.2/` and `dist/3.3/`

Treat `schemas.json` as the canonical registry for latest, supported, and
development versions. After changing schema inputs, regenerate distributions
through the Windows environment:

```text
cmd.exe /d /s /c "cd /d <windows-project-root> && powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\update-dist.ps1"
```

Commit generated `dist/` changes together with their inputs. Follow
`docs/releases.md` when changing the published version contract.

## Commit messages

Before generating or creating a commit, inspect only the staged changes and
follow `.github/commit-message-instructions.md`. Treat that file as the
canonical source for commit format, types, scopes, body structure, and
examples. Never include unstaged work in the generated message and never
invent verification results.

## Windows-backed checkout from WSL

The checkout is stored below `/mnt/c` and is backed by Windows. When an agent is
running inside WSL, all test and quality-check execution must use the
repository-root Windows `.venv` through `cmd.exe`. Do not run Ruff, Pyright,
PSScriptAnalyzer, or Pytest with WSL tooling. Read-only inspection may run
inside WSL, but it does not replace the Windows test result.

In the commands below, `<windows-project-root>` means the absolute Windows path
of the current repository root. Resolve and substitute this placeholder before
execution; do not pass it literally to `cmd.exe`. Invoke PowerShell explicitly
with `powershell.exe -NoProfile -ExecutionPolicy Bypass -File`. A direct script
invocation that exits with code zero but produces no runner output is
inconclusive.

Prepare the test environment:

```text
cmd.exe /d /s /c "cd /d <windows-project-root> && powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\tests\prepare-tests.ps1"
```

Run the complete quality and test suite:

```text
cmd.exe /d /s /c "cd /d <windows-project-root> && powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\tests\run-tests.ps1"
```

Run a focused test module:

```text
cmd.exe /d /s /c "cd /d <windows-project-root> && powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\tests\run-tests.ps1 tests/test_validation.py -q"
```

Run an individual test:

```text
cmd.exe /d /s /c "cd /d <windows-project-root> && powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\tests\run-tests.ps1 tests/test_combine.py::test_combined_output_is_reproducible -q"
```

`run-tests.ps1` runs Ruff, Pyright, PSScriptAnalyzer, and Pytest.
Individual quality checks may be invoked directly when needed:

```text
cmd.exe /d /s /c "cd /d <windows-project-root> && .venv\Scripts\python.exe -m ruff format --check ."
cmd.exe /d /s /c "cd /d <windows-project-root> && .venv\Scripts\python.exe -m ruff check ."
cmd.exe /d /s /c "cd /d <windows-project-root> && .venv\Scripts\python.exe -m pyright"
```

Clean test artifacts while retaining `.venv`:

```text
cmd.exe /d /s /c "cd /d <windows-project-root> && powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\tests\cleanup-tests.ps1"
```

Require visible Ruff, Pyright, PSScriptAnalyzer, Pytest collection, and final
test output before reporting the full suite as successful. If WSL reports
`UtilBindVsockAnyPort: socket failed 1`, immediately retry the exact same,
narrowly scoped `cmd.exe` command outside the WSL sandbox using the execution
tool's escalation mechanism. Do not report Windows validation as blocked until
that escalated retry also fails. Never substitute WSL tooling for the Windows
test run.

Prefer reusing an existing Python 3.14 `.venv`; only use `-Recreate` when a
clean rebuild is necessary and `python.exe` is not locked by VS Code or another
process. If an interrupted recreation leaves the interpreter intact but removes
pip, repair it with the Windows interpreter before preparing again:

```text
cmd.exe /d /s /c "cd /d <windows-project-root> && .venv\Scripts\python.exe -m ensurepip --upgrade"
```
