param (
    [Parameter(Mandatory=$true, Position=0)][string]$InFile,
    [Parameter(Position=1)][string]$OutFile = $(join-path (Get-Item $InFile).DirectoryName (Get-Item $InFile).BaseName ) + ".cap",
    [switch]$Overwrite = $false,
    [switch]$KeepOriginal = $false
)

$FileExists = Test-Path $OutFile

if ($FileExists -And $Overwrite) {
    Remove-Item -path $OutFile
} elseif ($FileExists -And !$Overwrite) {
    Write-Host "OutFile already exists. Set the -Overwrite flag to delete if exists. Quitting..."
    exit
}

$s = New-PefTraceSession -Path $OutFile -SaveOnStop
$s | Add-PefMessageProvider -Provider $InFile
$s | Start-PefTraceSession

if (!$KeepOriginal) {
    Remove-Item -path $InFile
}