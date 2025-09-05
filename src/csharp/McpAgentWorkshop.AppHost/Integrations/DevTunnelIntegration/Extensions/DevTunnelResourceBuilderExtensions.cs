using AspireDevTunnels.AppHost.HealthChecks;
using AspireDevTunnels.AppHost.Resources;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Diagnostics.HealthChecks;
using Microsoft.Identity.Client;

namespace AspireDevTunnels.AppHost.Extensions;

public static class DevTunnelResourceBuilderExtensions
{
    public static IResourceBuilder<DevTunnelResource> AddDevTunnel(
        this IDistributedApplicationBuilder builder,
        string name)
    {
        DevTunnelResource devTunnelResource = new(name);

        IResourceBuilder<DevTunnelResource> devTunnelResourceBuilder =
            builder
                .AddResource(devTunnelResource)
                .WithArgs(["host"]);

        // Startup events
        builder.Eventing.Subscribe<BeforeResourceStartedEvent>(
            devTunnelResource,
            async (context, cancellationToken) =>
            {
                if (devTunnelResource.VerifyShouldInitialize())
                {
                    await InitializeTunnelAsync(devTunnelResource, cancellationToken);
                    await InitializePortsAsync(devTunnelResource, cancellationToken);

                    devTunnelResource.IsInitialized = true;
                }
                else
                {
                    devTunnelResource.SkippedInitializationForExplicitStart = true;
                }
            });

        // Dashboard Actions
        devTunnelResourceBuilder
            .WithCommand("allow-anonymous-access", "Make Endpoint Public", async (context) =>
             {
                 await devTunnelResource.AllowAnonymousAccessAsync(context.CancellationToken);

                 devTunnelResource.IsPublic = true;

                 return new ExecuteCommandResult { Success = true };

             }, commandOptions: new CommandOptions
             {
                 ConfirmationMessage = "Are you sure you want to make the dev tunnel publicly available?",
                 IconName = "LockOpen",
                 UpdateState = (updateState) =>
                 {
                     return updateState.ResourceSnapshot.State?.Text != "Running" ? ResourceCommandState.Disabled : ResourceCommandState.Enabled;
                 },
             });

        devTunnelResourceBuilder
            .WithCommand("get-tunnel-urls", "Get URLs", async (context) =>
            {
                DevTunnel devTunnel =
                    await devTunnelResource.GetTunnelDetailsAsync(context.CancellationToken);

                Console.WriteLine($"Tunnel {devTunnelResource.Name} URLs:");

                foreach (DevTunnelActivePort port in devTunnel.Tunnel.Ports)
                {
                    Console.WriteLine($"Port {port.PortNumber}: {port.PortUri}");
                }

                return new ExecuteCommandResult { Success = true };

            }, commandOptions: new CommandOptions
            {
                IconName = "LinkMultiple",
                UpdateState = (updateState) =>
                {
                    return updateState.ResourceSnapshot.State?.Text != "Running" ? ResourceCommandState.Disabled : ResourceCommandState.Enabled;
                },
            });

        devTunnelResourceBuilder
           .WithCommand("get-access-token", "Get Access Token", async (context) =>
           {
               DevTunnelAccessInfo devTunnelAccessInfo =
                   await devTunnelResource.GetAuthTokenAsync(context.CancellationToken);

               Console.WriteLine($"{devTunnelResource.Name} Token (and header):");

               Console.WriteLine($"X-Tunnel-Authorization: tunnel {devTunnelAccessInfo.Token}");

               return new ExecuteCommandResult { Success = true };

           }, commandOptions: new CommandOptions
           {
               IconName = "Key",
               UpdateState = (updateState) =>
               {
                   return updateState.ResourceSnapshot.State?.Text != "Running" ? ResourceCommandState.Disabled : ResourceCommandState.Enabled;
               },
           });

        // Establish Health Checks
        string healthCheckKey = $"DevTunnelHealth_{name}";

        builder.Services.AddHealthChecks()
            .Add(new HealthCheckRegistration(
              healthCheckKey,
              sp => sp.GetRequiredKeyedService<DevTunnelHealthCheck>(healthCheckKey),
              failureStatus: default,
              tags: default,
              timeout: TimeSpan.FromMinutes(2)));

        builder.Services.AddKeyedSingleton(healthCheckKey, new DevTunnelHealthCheck(name));

        devTunnelResourceBuilder.WithHealthCheck(healthCheckKey);

        return devTunnelResourceBuilder;
    }

    public static IResourceBuilder<T> WithDevTunnel<T>(
        this IResourceBuilder<T> resourceBuilder,
        IResourceBuilder<DevTunnelResource> devTunnelResourceBuilder)
            where T : IResourceWithEndpoints
    {
        // TODO: Check port limits (how many ports per tunnel allowed)
        devTunnelResourceBuilder
            .WithParentRelationship(resourceBuilder.Resource)
            .WaitFor((IResourceBuilder<IResource>)resourceBuilder);
        return resourceBuilder;
    }

    private static async Task InitializeTunnelAsync(
        DevTunnelResource devTunnelResource,
        CancellationToken cancellationToken)
    {
        await devTunnelResource.VerifyDevTunnelCliInstalledAsync(cancellationToken);
        await devTunnelResource.VerifyUserLoggedInAsync(cancellationToken);

        // Check if tunnel already exists
        DevTunnel devTunnel = await devTunnelResource.GetTunnelDetailsAsync(cancellationToken);

        if (devTunnel is null)
        {
            await devTunnelResource.CreateTunnelAsync(cancellationToken);

            if (devTunnelResource.IsPublic)
            {
                await devTunnelResource.AllowAnonymousAccessAsync(cancellationToken);
            }
        }
        else
        {
            Console.WriteLine($"Tunnel {devTunnelResource.Name} already exists. Skipping creation");
        }
    }

    private static async Task InitializePortsAsync(
        DevTunnelResource devTunnelResource,
        CancellationToken cancellationToken)
    {
        var parentResources =
                    devTunnelResource.Annotations.OfType<ResourceRelationshipAnnotation>()
                        .Where(resourceRelationship => resourceRelationship.Type == "Parent")
                        .Select(resourceRelationship => resourceRelationship.Resource)
                        .ToList();

        foreach (IResource parentResource in parentResources)
        {

            if (!parentResource.TryGetEndpoints(out IEnumerable<EndpointAnnotation>? parentEndpoints))
            {
                continue;
            }

            var endpoints = parentEndpoints.ToList();

            foreach (EndpointAnnotation endpoint in endpoints)
            {
                if (endpoint.AllocatedEndpoint?.Port is null)
                {
                    Console.WriteLine($"No eligible port found for {endpoint.Name}.");

                    continue;
                }

                // Check if port already exists
                DevTunnelPort devTunnelPort =
                    await devTunnelResource.GetPortDetailsAsync(endpoint.AllocatedEndpoint.Port, cancellationToken);

                if (devTunnelPort is not null)
                {
                    Console.WriteLine($"Port {endpoint.AllocatedEndpoint.Port} already exists for tunnel {devTunnelResource.Name}");
                    continue;
                }
                else
                {
                    // Add port to tunnel
                    DevTunnelPort devTunnelActivePort =
                        await devTunnelResource.AddPortAsync(
                            endpoint.AllocatedEndpoint.Port,
                            endpoint.UriScheme,
                            cancellationToken);
                }
            }
        }
    }

    public static IResourceBuilder<DevTunnelResource> WithPublicAccess(this IResourceBuilder<DevTunnelResource> devTunnelResourceBuilder)
    {
        devTunnelResourceBuilder.Resource.IsPublic = true;
        return devTunnelResourceBuilder;
    }
}
