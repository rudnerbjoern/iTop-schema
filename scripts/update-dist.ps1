[CmdletBinding()]
param(
    [string]$PythonPath
)

$ErrorActionPreference = "Stop"

$repositoryRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
if (-not $PythonPath) {
    $PythonPath = Join-Path $repositoryRoot ".venv/Scripts/python.exe"
}
if (-not (Test-Path -LiteralPath $PythonPath -PathType Leaf)) {
    throw "Python was not found at: $PythonPath. Run scripts/tests/prepare-tests.ps1 first."
}

Push-Location $repositoryRoot
try {
    & $PythonPath scripts/update_dist.py --repository-root $repositoryRoot
    if ($LASTEXITCODE -ne 0) {
        throw "Distribution generation failed with exit code $LASTEXITCODE."
    }
}
finally {
    Pop-Location
}
