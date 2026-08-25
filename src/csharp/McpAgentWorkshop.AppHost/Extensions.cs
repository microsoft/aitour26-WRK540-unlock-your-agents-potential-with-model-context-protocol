using System.Data.Common;
using Aspire.Hosting.Azure;
using Aspire.Hosting.DevTunnels;
using Aspire.Hosting.Python;
using McpAgentWorkshop.AppHost.Integrations;
using Microsoft.Identity.Client;

namespace Aspire.Hosting;

public static class Extensions
{
    static readonly string sourceFolder = Path.Combine(Environment.CurrentDirectory, "..", "..");
    static readonly string virtualEnvironmentPath = OperatingSystem.IsWindows() ?
        Path.Join(sourceFolder, "python", "workshop", ".venv") :
        "/usr/local";

    public static IResourceBuilder<PythonAppResource> AddFrontend(
        this IDistributedApplicationBuilder builder,
        string name)
    {
        return builder.AddPythonApp(name, Path.Combine(sourceFolder, "shared", "webapp"), "app.py")
            .WithVirtualEnvironment(virtualEnvironmentPath)
            .WithHttpEndpoint(env: "PORT")
            .WithUrlForEndpoint("http", annotations =>
            {
                annotations.DisplayText = "Workshop Frontend";
            });
    }

    public static IResourceBuilder<PostgresAccountResource> AddPostgresAccount(this IResourceBuilder<AzurePostgresFlexibleServerDatabaseResource> builder, [ResourceName] string accountName, IResourceBuilder<ParameterResource> username, IResourceBuilder<ParameterResource> password)
    {
        return builder.ApplicationBuilder.AddResource(new PostgresAccountResource(accountName, builder.Resource, username.Resource, password.Resource))
            .WithParentRelationship(builder.Resource)
            .WithInitialState(new CustomResourceSnapshot { State = KnownResourceStates.Running, ResourceType = "PostgresAccount", Properties = [] });
    }
}