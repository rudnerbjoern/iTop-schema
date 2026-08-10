[CmdletBinding(SupportsShouldProcess)]
param(
    [switch]$IncludeVirtualEnvironment
)

$ErrorActionPreference = "Stop"

$repositoryRoot = (Resolve-Path (Join-Path $PSScriptRoot "../..")).Path
$virtualEnvironment = Join-Path $repositoryRoot ".venv"

function Remove-TestArtifact {
    [CmdletBinding(SupportsShouldProcess)]
    param(
        [Parameter(Mandatory)]
        [string]$Path
    )

    if ((Test-Path -LiteralPath $Path) -and $PSCmdlet.ShouldProcess($Path, "Remove test artifact")) {
        Remove-Item -LiteralPath $Path -Recurse -Force
    }
}

$fixedArtifacts = @(
    (Join-Path $repositoryRoot ".pytest_cache"),
    (Join-Path $repositoryRoot ".coverage"),
    (Join-Path $repositoryRoot "htmlcov")
)

foreach ($artifact in $fixedArtifacts) {
    Remove-TestArtifact -Path $artifact
}

$childItemParameters = @{
    LiteralPath = $repositoryRoot
    Directory = $true
    Recurse = $true
    Force = $true
    ErrorAction = "SilentlyContinue"
}

$generatedDirectories = Get-ChildItem @childItemParameters |
    Where-Object {
        -not $_.FullName.StartsWith($virtualEnvironment, [System.StringComparison]::OrdinalIgnoreCase) -and
        ($_.Name -eq "__pycache__" -or $_.Name -like "*.egg-info")
    }

foreach ($directory in $generatedDirectories) {
    Remove-TestArtifact -Path $directory.FullName
}

if ($IncludeVirtualEnvironment) {
    Remove-TestArtifact -Path $virtualEnvironment
}
Write-Host "Test cleanup completed."
