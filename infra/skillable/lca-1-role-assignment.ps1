# LCA Metadata
# Delay: 15 seconds
# Blocking: yes

$subId   = "@lab.CloudSubscription.Id"
$username = "@lab.CloudPortalCredential(User1).Username"

# Print subid and username
Write-Host "Subscription ID: $subId"
Write-Host "Username: $username"

function Invoke-WithRetry {
    param (
        [scriptblock]$Command,
        [int]$MaxRetries = 5,
        [int]$DelaySeconds = 10
    )

    for ($i = 1; $i -le $MaxRetries; $i++) {
        try {
            & $Command
            Write-Host "Success on attempt $i"
            return
        }
        catch {
            Write-Warning "Attempt $i failed: $($_.Exception.Message)"
            if ($i -lt $MaxRetries) {
                Write-Host "Retrying in $DelaySeconds seconds..."
                Start-Sleep -Seconds $DelaySeconds
            }
            else {
                throw "Command failed after $MaxRetries attempts."
            }
        }
    }
}

# Assign roles with retries
Invoke-WithRetry { 
    New-AzRoleAssignment -SignInName $username -RoleDefinitionName "Azure AI Developer" -Scope "/subscriptions/$subId/resourceGroups/rg-zava-agent-wks"
    Write-Host "Assigned 'Azure AI Developer' role to resource group."
}

Invoke-WithRetry { 
    New-AzRoleAssignment -SignInName $username -RoleDefinitionName "Cognitive Services User" -Scope "/subscriptions/$subId"
    Write-Host "Assigned 'Cognitive Services User' role to subscription."
}