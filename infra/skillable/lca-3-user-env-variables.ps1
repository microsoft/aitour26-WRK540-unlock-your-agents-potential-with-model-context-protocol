# LCA Metadata
# Delay: 15 seconds

[Environment]::SetEnvironmentVariable("LAB_SUBSCRIPTION_ID", "@lab.CloudSubscription.Id", "User")
[Environment]::SetEnvironmentVariable("LAB_TENANT_ID", "@lab.CloudSubscription.TenantId", "User")
[Environment]::SetEnvironmentVariable("LAB_USERNAME", "@lab.CloudPortalCredential(User1).Username", "User")
[Environment]::SetEnvironmentVariable("LAB_INSTANCE_ID", "@lab.LabInstance.Id", "User")
[Environment]::SetEnvironmentVariable("LAB_RESOURCE_GROUP", "@lab.CloudResourceGroup(rg-zava-agent-wks).Name", "User")
[Environment]::SetEnvironmentVariable("LAB_APP_SECRET", "@lab.CloudSubscription.AppSecret", "User")
[Environment]::SetEnvironmentVariable("LAB_APP_ID", "@lab.CloudSubscription.AppId", "User")
[Environment]::SetEnvironmentVariable("LAB_AZURE_PASSWORD", "@lab.CloudResourceTemplate(WRK540-AITour2026).Parameters[postgresAdminPassword]", "User")
[Environment]::SetEnvironmentVariable("AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED", "true", "User")
