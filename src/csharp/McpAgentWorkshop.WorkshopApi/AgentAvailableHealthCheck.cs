using McpAgentWorkshop.WorkshopApi.Services;
using Microsoft.Extensions.Diagnostics.HealthChecks;

internal class AgentAvailableHealthCheck(AgentService agentService) : IHealthCheck
{
    public Task<HealthCheckResult> CheckHealthAsync(HealthCheckContext context, CancellationToken cancellationToken = default)
    {
        if (!agentService.IsAgentAvailable)
        {
            return Task.FromResult(HealthCheckResult.Unhealthy("Agent is not available"));
        }

        return Task.FromResult(HealthCheckResult.Healthy("Agent is available"));
    }
}