# LCA Metadata
# Delay: 20 seconds
# Blocking: true
# Retries: 1

# =========================
# VM Life Cycle Action (PowerShell)
# Tear down resources created for the lab by deleting the resource group
# =========================

# --- Skillable tokens / lab values ---
$TenantId = "@lab.CloudSubscription.TenantId"
$AppId = "@lab.CloudSubscription.AppId"
$Secret = "@lab.CloudSubscription.AppSecret"
$SubId = "@lab.CloudSubscription.Id"

# Resource group where your template deployed (via alias rg-zava-agent-wks)
$ResourceGroup = "@lab.CloudResourceGroup(rg-zava-agent-wks).Name"

# --- Azure login (service principal) ---
$sec = ConvertTo-SecureString $Secret -AsPlainText -Force
$cred = [pscredential]::new($AppId, $sec)
Connect-AzAccount -ServicePrincipal -Tenant $TenantId -Credential $cred -Subscription $SubId | Out-Null

Write-Host "Skillable LCA: Deleting resource group '$ResourceGroup' and all contained resources..." -ForegroundColor Yellow

# Check if resource group exists and delete it
try {
    $resourceGroup = Get-AzResourceGroup -Name $ResourceGroup -ErrorAction SilentlyContinue
    if (-not $resourceGroup) {
        Write-Host "Resource group '$ResourceGroup' not found. Nothing to delete." -ForegroundColor Yellow
        exit 0
    }

    Write-Host "Deleting resource group '$ResourceGroup'..." -ForegroundColor Red
    Remove-AzResourceGroup -Name $ResourceGroup -Force

    Write-Host "Resource group '$ResourceGroup' and all contained resources have been successfully deleted!" -ForegroundColor Green
}
catch {
    Write-Error "Failed to delete resource group: $($_.Exception.Message)"
    exit 1
}