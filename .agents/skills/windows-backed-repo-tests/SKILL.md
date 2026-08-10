---
name: windows-backed-repo-tests
description: Run repository tests and quality checks through Windows executables from a WSL-based Codex session. Use when this checkout is accessed below /mnt/c, AGENTS.md requires the Windows .venv, cmd.exe or powershell.exe reports UtilBindVsockAnyPort, or the user asks for authoritative local validation of this Windows-backed repository.
---

# Windows-backed repository tests

Treat the Windows toolchain as authoritative for this checkout. Never
substitute WSL test results.

## Execute validation

1. Read the repository `AGENTS.md` and use its exact preparation, focused test,
   full-suite, and cleanup commands.
2. Resolve `<windows-project-root>` to the repository's absolute Windows path.
   Never pass the placeholder literally.
3. Prefer the existing Windows environment. Check its interpreter version
   before recreating it.
4. Invoke Windows through `cmd.exe`; invoke PowerShell scripts with
   `powershell.exe -NoProfile -ExecutionPolicy Bypass -File`.
5. Run the smallest requested scope. For completion claims, run the full suite
   required by `AGENTS.md` and retain visible runner output.

## Cross the sandbox boundary

Start with the normal narrowly scoped Windows command. If it fails with
`UtilBindVsockAnyPort: socket failed 1`, immediately retry the exact command
using the execution tool's sandbox-escalation mechanism. Use a narrow reusable
prefix such as `cmd.exe /d /s /c` when approval prefixes are supported.

Do not report Windows interop as blocked until the escalated retry also fails.
Do not run Ruff, Pyright, PSScriptAnalyzer, or Pytest under WSL as a fallback.

## Recover the Windows environment safely

Avoid `-Recreate` when the existing environment uses Python 3.14. If recreation
fails because `.venv\Scripts\python.exe` is locked, do not terminate processes
without user authorization. Reuse the environment when possible or ask the
user to close the locking application.

If a failed recreation leaves `python.exe` intact but removes pip, repair it:

```text
cmd.exe /d /s /c "cd /d <windows-project-root> && .venv\Scripts\python.exe -m ensurepip --upgrade"
```

Then prepare without `-Recreate` and run the required suite.

## Report evidence

Report the Windows Python version, Ruff, Pyright, PSScriptAnalyzer, collected
and passed Pytest counts, and coverage. Treat exit code zero without visible
runner output as inconclusive.
