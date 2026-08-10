@{
    IncludeDefaultRules = $true
    Severity = @(
        "Error"
        "Warning"
    )
    ExcludeRules = @(
        "PSAvoidUsingWriteHost"
    )
    Rules = @{
        PSUseConsistentIndentation = @{
            Enable = $true
            Kind = "space"
            IndentationSize = 4
            PipelineIndentation = "IncreaseIndentationForFirstPipeline"
        }
        PSUseConsistentWhitespace = @{
            Enable = $true
            CheckInnerBrace = $true
            CheckOpenBrace = $true
            CheckOpenParen = $true
            CheckOperator = $true
            CheckPipe = $true
            CheckSeparator = $true
        }
    }
}
