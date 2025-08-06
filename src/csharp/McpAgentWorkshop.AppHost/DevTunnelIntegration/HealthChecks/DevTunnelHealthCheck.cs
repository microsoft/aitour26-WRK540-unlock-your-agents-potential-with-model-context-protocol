using AspireDevTunnels.AppHost.Commands;
using AspireDevTunnels.AppHost.Resources;
using Microsoft.Extensions.Diagnostics.HealthChecks;

namespace AspireDevTunnels.AppHost.HealthChecks;

internal class DevTunnelHealthCheck(string name) : IHealthCheck
{
    public async Task<HealthCheckResult> CheckHealthAsync(HealthCheckContext context, CancellationToken cancellationToken = default)
    {
        Console.WriteLine($"Running health check for {name}...");

        List<string> commandLineArgs = DevTunnelCommandArgs.GetTunnelDetailsArguments(name);

        DevTunnelCommandResult<DevTunnel> devTunnelCommandResult =
            await DevTunnelCommands.TryRunProcessAsync<DevTunnel>(commandLineArgs, cancellationToken);

        if (devTunnelCommandResult.IsSuccess && devTunnelCommandResult.Value is not null)
        {
            DevTunnel devTunnel = devTunnelCommandResult.Value;

            Console.WriteLine($"Tunnel {devTunnel.Tunnel.TunnelId} is healthy.");

            return HealthCheckResult.Healthy(
                $"Tunnel {devTunnel.Tunnel.TunnelId} is healthy. Hosting {devTunnel.Tunnel.Ports.Count} Ports.");
        }

        return HealthCheckResult.Unhealthy(
            $"Tunnel {name} is unhealthy. Error: {devTunnelCommandResult.Error}; ExitCode: {devTunnelCommandResult.ExitCode}; Output: {devTunnelCommandResult.Output}");
    }
}
