[CmdletBinding()]
param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$AdditionalPytestArguments = @()
)

$ErrorActionPreference = "Stop"

$repositoryRoot = (Resolve-Path (Join-Path $PSScriptRoot "../..")).Path
$virtualEnvironment = Join-Path $repositoryRoot ".venv"
$windowsPython = Join-Path $virtualEnvironment "Scripts/python.exe"
$posixPython = Join-Path $virtualEnvironment "bin/python"
$powerShellAnalyzerSettings = Join-Path $repositoryRoot "PSScriptAnalyzerSettings.psd1"
$powerShellScripts = Join-Path $repositoryRoot "scripts/tests"
$toolVersionsFile = Join-Path $repositoryRoot "scripts/tool-versions.psd1"
$toolVersions = Import-PowerShellDataFile -Path $toolVersionsFile
$powerShellAnalyzerVersion = $toolVersions.PSScriptAnalyzer

if (Test-Path -LiteralPath $windowsPython -PathType Leaf) {
    $python = $windowsPython
}
elseif (Test-Path -LiteralPath $posixPython -PathType Leaf) {
    $python = $posixPython
}
else {
    throw "Test environment not found. Run scripts/tests/prepare-tests.ps1 first."
}
function Invoke-PythonCommand {
    param(
        [Parameter(Mandatory)]
        [string[]]$Arguments,
        [Parameter(Mandatory)]
        [string]$Description
    )

    & $python @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "$Description failed with exit code $LASTEXITCODE."
    }
}

Push-Location $repositoryRoot
try {
    Invoke-PythonCommand -Description "Ruff linting" -Arguments @(
        "-m", "ruff", "check", "."
    )
    Invoke-PythonCommand -Description "Ruff format check" -Arguments @(
        "-m", "ruff", "format", "--check", "."
    )
    Invoke-PythonCommand -Description "Pyright type checking" -Arguments @(
        "-m", "pyright"
    )

    $requiredAnalyzer = Get-Module -ListAvailable -Name PSScriptAnalyzer |
        Where-Object Version -EQ $powerShellAnalyzerVersion
    if (-not $requiredAnalyzer) {
        throw "PSScriptAnalyzer $powerShellAnalyzerVersion is not installed. Run prepare-tests.ps1 first."
    }
    Import-Module PSScriptAnalyzer -RequiredVersion $powerShellAnalyzerVersion

    $analysisResults = @(
        Invoke-ScriptAnalyzer -Path $powerShellScripts -Recurse -Settings $powerShellAnalyzerSettings
    )
    if ($analysisResults.Count -gt 0) {
        $analysisResults | Format-Table -AutoSize | Out-Host
        throw "PSScriptAnalyzer reported $($analysisResults.Count) issue(s)."
    }

    $pytestArguments = @(
        "-m", "pytest",
        "--cov=itop_schema",
        "--cov-report=term-missing"
    ) + $AdditionalPytestArguments
    Invoke-PythonCommand -Description "Pytest" -Arguments $pytestArguments
}
finally {
    Pop-Location
}

Write-Host "All lint, type, and test checks passed."
