using AspireDevTunnels.AppHost.Extensions;

var builder = DistributedApplication.CreateBuilder(args);

var foundry = builder.AddParameter("FoundryEndpoint");
var chatDeployment = builder.AddParameter("ChatModelDeploymentName");
var embeddingDeployment = builder.AddParameter("EmbeddingModelDeploymentName");
var aoai = builder.AddParameter("AzureOpenAIEndpoint");
var appInsights = builder.AddConnectionString("ApplicationInsights", "APPLICATIONINSIGHTS_CONNECTION_STRING");

var pg = builder.AddPostgres("pg")
    .WithPgAdmin()
    .WithInitFiles(Path.Combine(Environment.CurrentDirectory, "..", "..", "..", "scripts"))
    // Use the pgvector image for PostgreSQL with pgvector extension
    .WithImage("pgvector/pgvector", "pg17")
    .WithLifetime(ContainerLifetime.Persistent)
    ;

var zava = pg.AddDatabase("zava");

var sourceFolder = Path.Combine(Environment.CurrentDirectory, "..", "..");

string virtualEnvironmentPath = "/usr/local/python/current";

var devtunnel = builder.AddDevTunnel("mcp-devtunnel");

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
    .WithEnvironment("PROJECT_ENDPOINT", foundry)
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
    .WithEnvironment("DEV_TUNNEL_URL", () =>
    {
        var endpoint = mcpServer.GetEndpoint("http") ?? throw new InvalidOperationException("MCP Server HTTP endpoint not found.");

        var devTunnelInfo = devtunnel.Resource.GetTunnelDetailsAsync();
        devTunnelInfo.Wait();

        var result = devTunnelInfo.Result;

        var activePort = result.Tunnel.Ports.FirstOrDefault(p => p.PortNumber == endpoint.Port) ?? throw new InvalidOperationException($"No active port found for MCP Server on port {endpoint.Port}.");

        return activePort.PortUri;
    });

builder.AddPythonApp("python-chat-frontend", Path.Combine(sourceFolder, "shared", "webapp"), "app.py", virtualEnvironmentPath: virtualEnvironmentPath)
    .WithReference(agentApp)
    .WaitFor(agentApp)
    .WithHttpEndpoint(env: "PORT")
    .WithOtlpExporter()
    .WithEnvironment("OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED", "true");

builder.AddMcpInspector("mcp-inspector")
    .WithReference(mcpServer);

var dotnetMcpServer = builder.AddProject<Projects.McpAgentWorkshop_McpServer>("dotnet-mcp-server")
    .WithReference(zava)
    .WaitFor(zava)
    .WithDevTunnel(devtunnel)
    .WithReference(appInsights);

var dotnetAgentApp = builder.AddProject<Projects.McpAgentWorkshop_WorkshopApi>("dotnet-agent-app")
    .WithReference(zava)
    .WithEnvironment("MAP_MCP_FUNCTIONS", "false")
    .WithReference(dotnetMcpServer)
    .WaitFor(dotnetMcpServer)
    .WaitFor(devtunnel)
    .WithEnvironment("DEV_TUNNEL_URL", () =>
    {
        var endpoint = dotnetMcpServer.GetEndpoint("http") ?? throw new InvalidOperationException("MCP Server HTTP endpoint not found.");

        var devTunnelInfo = devtunnel.Resource.GetTunnelDetailsAsync();
        devTunnelInfo.Wait();

        var result = devTunnelInfo.Result;

        var activePort = result.Tunnel.Ports.FirstOrDefault(p => p.PortNumber == endpoint.Port) ?? throw new InvalidOperationException($"No active port found for MCP Server on port {endpoint.Port}.");

        return activePort.PortUri;
    })
    .WithReference(appInsights);

builder.AddPythonApp("dotnet-chat-frontend", Path.Combine(sourceFolder, "shared", "webapp"), "app.py", virtualEnvironmentPath: virtualEnvironmentPath)
    .WithReference(dotnetAgentApp)
    .WaitFor(dotnetAgentApp)
    .WithHttpEndpoint(env: "PORT")
    .WithOtlpExporter()
    .WithEnvironment("OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED", "true");


builder.Build().Run();
