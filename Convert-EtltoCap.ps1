param (
    [Parameter(Mandatory=$true, Position=0)][string]$InFile,
    [Parameter(Position=1)][string]$OutFile = $(join-path (Get-Item $InFile).DirectoryName (Get-Item $InFile).BaseName ) + ".cap",
    [switch]$Overwrite = $false,
    [switch]$KeepOriginal = $false
)

$InFilePath = Convert-Path $InFile
$OutFilePath = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathfromPSPath($OutFile)
$FileExists = Test-Path $OutFilePath


if ($FileExists -And $Overwrite) {
    Remove-Item -path $OutFilePath
} elseif ($FileExists -And !$Overwrite) {
    Write-Host "OutFile already exists. Set the -Overwrite flag to delete if exists. Quitting..."
    exit
}

$s = New-PefTraceSession -Path $OutFilePath -SaveOnStop
$s | Add-PefMessageProvider -Provider $InFilePath
$s | Start-PefTraceSession

if (!$KeepOriginal) {
    Remove-Item -path $InFilePath
}