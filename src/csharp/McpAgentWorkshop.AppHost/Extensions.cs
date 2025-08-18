using Aspire.Hosting.Python;
using AspireDevTunnels.AppHost.Extensions;
using AspireDevTunnels.AppHost.Resources;

namespace Aspire.Hosting;

public static class Extensions
{
    static readonly string sourceFolder = Path.Combine(Environment.CurrentDirectory, "..", "..");
    static readonly string virtualEnvironmentPath = "/usr/local/python/current";

    public static IResourceBuilder<PythonAppResource> WithPostgres(this IResourceBuilder<PythonAppResource> builder, IResourceBuilder<PostgresDatabaseResource> db)
    {
        builder.WithEnvironment("POSTGRES_URL", () => $"postgresql://{db.Resource.Parent.UserNameParameter?.ToString() ?? "postgres"}:{db.Resource.Parent.PasswordParameter.Value}@{db.Resource.Parent.PrimaryEndpoint.Host}:{db.Resource.Parent.PrimaryEndpoint.Port}/{db.Resource.Name}")
               .WaitFor(db);

        return builder;
    }

    public static IDistributedApplicationBuilder AddPythonWorkshop(
        this IDistributedApplicationBuilder builder,
        IResourceBuilder<PostgresDatabaseResource> zava,
        IResourceBuilder<DevTunnelResource> devtunnel,
        IResourceBuilder<IResourceWithConnectionString> appInsights,
        IResourceBuilder<ParameterResource> foundryEndpoint,
        IResourceBuilder<ParameterResource> chatDeployment,
        IResourceBuilder<ParameterResource> embeddingDeployment,
        IResourceBuilder<ParameterResource> aoai)
    {


        var mcpServer = builder.AddPythonApp("python-mcp-server", Path.Combine(sourceFolder, "python", "mcp_server", "sales_analysis"), "sales_analysis.py", virtualEnvironmentPath: virtualEnvironmentPath)
            .WithPostgres(zava)
            .WithHttpEndpoint(env: "PORT")
            .WithOtlpExporter()
            .WithEnvironment("OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED", "true")
            .WithEnvironment("APPLICATIONINSIGHTS_CONNECTION_STRING", appInsights)
            .WithDevTunnel(devtunnel);

        var agentApp = builder.AddPythonApp("python-agent-app", Path.Combine(sourceFolder, "python", "workshop"), "app.py", virtualEnvironmentPath: virtualEnvironmentPath)
            .WithHttpEndpoint(env: "PORT")
            .WithHttpHealthCheck("/health")
            .WithEnvironment("PROJECT_ENDPOINT", foundryEndpoint)
            .WithEnvironment("MODEL_DEPLOYMENT_NAME", chatDeployment)
            .WithEnvironment("EMBEDDING_MODEL_DEPLOYMENT_NAME", embeddingDeployment)
            .WithEnvironment("AZURE_OPENAI_ENDPOINT", aoai)
            .WithEnvironment("APPLICATIONINSIGHTS_CONNECTION_STRING", appInsights)
            .WithEnvironment("AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED", "true")
            .WithPostgres(zava)
            .WithEnvironment("MAP_MCP_FUNCTIONS", "false")
            .WithReference(mcpServer)
            .WaitFor(mcpServer)
            .WaitFor(devtunnel)
            .WithOtlpExporter()
            .WithEnvironment("OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED", "true")
            .WithDevTunnelEnvironmentVariable(devtunnel, mcpServer);

        builder.AddFrontend("python-chat-frontend")
            .WithReference(agentApp)
            .WaitFor(agentApp);

        return builder;
    }

    public static IResourceBuilder<PythonAppResource> AddFrontend(
        this IDistributedApplicationBuilder builder,
        string name)
    {
        return builder.AddPythonApp(name, Path.Combine(sourceFolder, "shared", "webapp"), "app.py", virtualEnvironmentPath: virtualEnvironmentPath)
            .WithHttpEndpoint(env: "PORT")
            .WithOtlpExporter()
            .WithEnvironment("OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED", "true");
    }

    public static IResourceBuilder<T> WithDevTunnelEnvironmentVariable<T>(
        this IResourceBuilder<T> builder,
        IResourceBuilder<DevTunnelResource> devtunnel,
        IResourceBuilder<IResourceWithEndpoints> mcpServer,
        string variableName = "DEV_TUNNEL_URL")
        where T : IResourceWithEnvironment
    {
        return builder.WithEnvironment(async (ctx) =>
        {
            var devTunnelInfo = await devtunnel.Resource.GetTunnelDetailsAsync();

            if (devTunnelInfo is null) return;

            if (!mcpServer.Resource.TryGetEndpoints(out var endpoints)) return;

            var endpoint = endpoints.FirstOrDefault(e => e.Transport == "http") ?? throw new InvalidOperationException("MCP Server HTTP endpoint not found.");
            var activePort = devTunnelInfo.Tunnel.Ports.FirstOrDefault(p => p.PortNumber == endpoint.Port) ?? throw new InvalidOperationException($"No active port found for MCP Server on port {endpoint.Port}.");

            if (activePort.PortUri is not null)
                ctx.EnvironmentVariables[variableName] = activePort.PortUri;
        });
    }
}
