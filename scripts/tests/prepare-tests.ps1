[CmdletBinding()]
param(
    [string]$PythonCommand = "python",
    [switch]$Recreate,
    [switch]$SkipPowerShellAnalyzer
)

$ErrorActionPreference = "Stop"

$repositoryRoot = (Resolve-Path (Join-Path $PSScriptRoot "../..")).Path
$virtualEnvironment = Join-Path $repositoryRoot ".venv"
$requirementsFile = Join-Path $repositoryRoot "scripts/requirements-dev.txt"
$toolVersionsFile = Join-Path $repositoryRoot "scripts/tool-versions.psd1"
$toolVersions = Import-PowerShellDataFile -Path $toolVersionsFile
$powerShellAnalyzerVersion = $toolVersions.PSScriptAnalyzer

function Invoke-CheckedCommand {
    param(
        [Parameter(Mandatory)]
        [scriptblock]$Command,
        [Parameter(Mandatory)]
        [string]$Description
    )

    & $Command
    if ($LASTEXITCODE -ne 0) {
        throw "$Description failed with exit code $LASTEXITCODE."
    }
}

function Get-VirtualEnvironmentPython {
    $windowsPython = Join-Path $virtualEnvironment "Scripts/python.exe"
    $posixPython = Join-Path $virtualEnvironment "bin/python"

    if (Test-Path -LiteralPath $windowsPython -PathType Leaf) {
        return $windowsPython
    }
    if (Test-Path -LiteralPath $posixPython -PathType Leaf) {
        return $posixPython
    }
    throw "Python was not found in the virtual environment: $virtualEnvironment"
}

if (-not (Get-Command $PythonCommand -ErrorAction SilentlyContinue)) {
    throw "Python command '$PythonCommand' was not found. Use -PythonCommand to select it."
}
if ($Recreate -and (Test-Path -LiteralPath $virtualEnvironment)) {
    Write-Host "Removing existing virtual environment: $virtualEnvironment"
    Remove-Item -LiteralPath $virtualEnvironment -Recurse -Force
}

if (-not (Test-Path -LiteralPath $virtualEnvironment -PathType Container)) {
    Write-Host "Creating virtual environment: $virtualEnvironment"
    Invoke-CheckedCommand -Description "Creating the virtual environment" -Command {
        & $PythonCommand -m venv $virtualEnvironment
    }
}
else {
    Write-Host "Using existing virtual environment: $virtualEnvironment"
}

$virtualEnvironmentPython = Get-VirtualEnvironmentPython

Push-Location $repositoryRoot
try {
    Write-Host "Installing test dependencies from: $requirementsFile"
    Invoke-CheckedCommand -Description "Installing test dependencies" -Command {
        & $virtualEnvironmentPython -m pip install -r $requirementsFile
    }
}
finally {
    Pop-Location
}

if (-not $SkipPowerShellAnalyzer) {
    $requiredAnalyzer = Get-Module -ListAvailable -Name PSScriptAnalyzer |
        Where-Object Version -EQ $powerShellAnalyzerVersion
    if (-not $requiredAnalyzer) {
        Write-Host "Installing PSScriptAnalyzer $powerShellAnalyzerVersion for the current user."
        $moduleParameters = @{
            Name = "PSScriptAnalyzer"
            RequiredVersion = $powerShellAnalyzerVersion
            Scope = "CurrentUser"
            Repository = "PSGallery"
            Force = $true
        }
        Install-Module @moduleParameters
    }
    else {
        Write-Host "Using PSScriptAnalyzer $powerShellAnalyzerVersion."
    }
}

Write-Host "Test environment is ready."
