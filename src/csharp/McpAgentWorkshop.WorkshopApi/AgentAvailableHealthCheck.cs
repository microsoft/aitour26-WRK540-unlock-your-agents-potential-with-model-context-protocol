using Azure.AI.Agents.Persistent;
using Microsoft.Extensions.Diagnostics.HealthChecks;

internal class AgentAvailableHealthCheck(PersistentAgent? agent) : IHealthCheck
{
    public Task<HealthCheckResult> CheckHealthAsync(HealthCheckContext context, CancellationToken cancellationToken = default)
    {
        if (agent is null)
        {
            return Task.FromResult(HealthCheckResult.Unhealthy("Agent is not available"));
        }

        return Task.FromResult(HealthCheckResult.Healthy("Agent is available"));
    }
}