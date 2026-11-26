# Checks that each file is signed as a download from us would be (desktop.yml, windows-sign): a chain Windows trusts, the
# publisher Salesflare BV, and a timestamp, so the signature outlives the short-lived certificate.
param([Parameter(Mandatory, ValueFromRemainingArguments)][string[]]$Files)
$ErrorActionPreference = 'Stop'
$signtool = (Get-ChildItem 'C:\Program Files (x86)\Windows Kits\10\bin\*\x64\signtool.exe' | Sort-Object { [version]$_.Directory.Parent.Name } | Select-Object -Last 1).FullName
foreach ($file in $Files) {
  & $signtool verify /pa /tw $file
  if ($LASTEXITCODE) { exit $LASTEXITCODE }
  $signature = Get-AuthenticodeSignature $file
  $subject = $signature.SignerCertificate.Subject
  Write-Host "$file`: $($signature.Status), $subject, timestamped by $($signature.TimeStamperCertificate.Subject)"
  if ($signature.Status -ne 'Valid') { throw "$file is not validly signed: $($signature.StatusMessage)" }
  if ($subject -notmatch '(^|, )O=Salesflare BV(,|$)') { throw "$file is signed by someone else: $subject" }
  if (-not $signature.TimeStamperCertificate) { throw "$file has no timestamp" }
}
