# Signs one file with Azure Artifact Signing, as the installer is made (desktop.yml, windows-sign). Off where SIGN_DLIB
# (Azure.CodeSigning.Dlib.dll) and SIGN_METADATA (its metadata.json) aren't set. A certificate in a cloud HSM would go in here
# instead: signtool's /sha1, with the HSM's key storage provider installed.
param([Parameter(Mandatory)][string]$File)
$ErrorActionPreference = 'Stop'
if (-not $env:SIGN_DLIB) { Write-Host "not signed: $File"; exit 0 }
$signtool = (Get-ChildItem 'C:\Program Files (x86)\Windows Kits\10\bin\*\x64\signtool.exe' | Sort-Object { [version]$_.Directory.Parent.Name } | Select-Object -Last 1).FullName
& $signtool sign /v /fd SHA256 /tr http://timestamp.acs.microsoft.com /td SHA256 /dlib $env:SIGN_DLIB /dmdf $env:SIGN_METADATA $File
if ($LASTEXITCODE) { exit $LASTEXITCODE }
& $signtool verify /pa /v $File
exit $LASTEXITCODE
