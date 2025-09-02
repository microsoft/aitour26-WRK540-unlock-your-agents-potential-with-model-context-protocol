# LCA Metadata
# Delay: 20 seconds

# =========================
# VM Life Cycle Action (PowerShell)
# Pull outputs from ARM/Bicep deployment and write .env
# =========================

# --- logging to both Skillable log + file ---
$logDir = "C:\logs"
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir | Out-Null }
$logFile = Join-Path $logDir "vm-init-pg-firewall-$(Get-Date -Format 'yyyyMMdd_HHmmss').log"
"[$(Get-Date -Format s)] VM LCA start" | Tee-Object -FilePath $logFile

function Log { param([string]$m) $ts = "[$(Get-Date -Format s)] $m"; $ts | Tee-Object -FilePath $logFile -Append }

# --- Skillable tokens / lab values ---
$UniqueSuffix = "@lab.LabInstance.Id"
$TenantId = "@lab.CloudSubscription.TenantId"
$AppId = "@lab.CloudSubscription.AppId"
$Secret = "@lab.CloudSubscription.AppSecret"
$SubId = "@lab.CloudSubscription.Id"

# Resource group where your template deployed (via alias rg-zava-agent-wks)
$ResourceGroup = "@lab.CloudResourceGroup(rg-zava-agent-wks).Name"

# Template PARAMETER (✅ supported by Skillable token macros)
$AzurePgPassword = "@lab.CloudResourceTemplate(WRK540-AITour2026).Parameters[postgresAdminPassword]"

# --- Azure login (service principal) ---
Log "Authenticating to Azure tenant $TenantId, subscription $SubId"
$sec = ConvertTo-SecureString $Secret -AsPlainText -Force
$cred = [pscredential]::new($AppId, $sec)
Connect-AzAccount -ServicePrincipal -Tenant $TenantId -Credential $cred -Subscription $SubId | Out-Null
$ctx = Get-AzContext
Log "Logged in as: $($ctx.Account) | Sub: $($ctx.Subscription.Name) ($($ctx.Subscription.Id))"

$PostgresServerName = "pg-zava-agent-wks-$UniqueSuffix"
$ResourceGroup = "@lab.CloudResourceGroup(rg-zava-agent-wks).Name"

# Set IP range 103.177.0.0 to 103.177.255.255
$StartIP = "103.177.0.0"
$EndIP = "103.177.255.255"
$RuleName = "allow-range-103-177-0-0-to-103-177-255-255"
Log "Adding firewall rule for IP range: $StartIP to $EndIP"
New-AzPostgreSqlFlexibleServerFirewallRule `
  -Name $RuleName `
  -ResourceGroupName $ResourceGroup `
  -ServerName $PostgresServerName `
  -StartIPAddress $StartIP `
  -EndIPAddress   $EndIP | Out-Null