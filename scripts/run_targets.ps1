Param(
  [string]$TargetsFile = "scans/targets.txt",
  [string]$Python = "python",
  [switch]$NoSubfinder,
  [string]$ArtifactDir = "artifacts"
)

if (-not (Test-Path $TargetsFile)) {
  Write-Error "Targets file not found: $TargetsFile"
  exit 1
}

$lines = Get-Content $TargetsFile | ForEach-Object { $_.Trim() } | Where-Object { $_ -and -not $_.StartsWith('#') }

foreach ($t in $lines) {
  Write-Host "[targets] $t"
  $args = @('--target', $t, '--artifact-dir', $ArtifactDir)
  if ($NoSubfinder) { $args += '--no-subfinder' }
  & $Python @args
  if ($LASTEXITCODE -ne 0) { Write-Warning "target $t returned exit code $LASTEXITCODE" }
}
