# simple-setup.ps1
$ErrorActionPreference = 'Stop'

$username = $env:LAB_USERNAME
$subId    = $env:LAB_SUBSCRIPTION_ID
$instance = $env:LAB_INSTANCE_ID

Write-Host "=== Step 1: Azure login ==="
az login | Out-Null
az account set --subscription $subId

Write-Host "=== Step 2: Dev Tunnel login ==="
devtunnel login

Write-Host "=== Step 3: Assigning roles ==="
$subScope = "/subscriptions/$subId"
$rgScope  = "/subscriptions/$subId/resourceGroups/rg-zava-agent-wks"

az role assignment create --assignee "$username" --role "Cognitive Services User" --scope "$subScope"        2>$null
az role assignment create --assignee "$username" --role "Azure AI Developer"       --scope "$rgScope"         2>$null

Write-Host "=== Step 4: Initialize Azure Database ==="
$repoRoot = Join-Path $HOME 'aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol'
$infraDir = Join-Path $repoRoot 'infra\skillable'

Push-Location $infraDir
.\init-db-azure-action.ps1 -UniqueSuffix $instance -AzurePgPassword "SecurePassword123!"
Pop-Location

Write-Host "=== Step 5: Update Git repo ==="
Push-Location $repoRoot
git pull
Pop-Location

Write-Host "=== Step 6: Activate Python venv (if exists) ==="
$venv = Join-Path $repoRoot 'src\python\workshop\.venv\Scripts\Activate.ps1'
if (Test-Path $venv) {
    . $venv
    Write-Host "✅ Virtual environment activated"
} else {
    Write-Host "⚠️ No virtual environment found at $venv"
}

Write-Host "`n🎉 All steps completed successfully!"