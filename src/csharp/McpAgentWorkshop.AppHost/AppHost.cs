using AspireDevTunnels.AppHost.Extensions;

var builder = DistributedApplication.CreateBuilder(args);

var foundryEndpoint = builder.AddParameter("FoundryEndpoint");
var chatDeployment = builder.AddParameter("ChatModelDeploymentName");
var embeddingDeployment = builder.AddParameter("EmbeddingModelDeploymentName");
var aoai = builder.AddParameter("AzureOpenAIEndpoint");
var rg = builder.AddParameter("ResourceGroupName");
var foundryResourceName = builder.AddParameter("FoundryResourceName");
var foundryProjectName = builder.AddParameter("FoundryProjectName");

var appInsights = builder.AddConnectionString("ApplicationInsights", "APPLICATIONINSIGHTS_CONNECTION_STRING");

var foundry = builder.AddAzureAIFoundry("ai-foundry")
    .RunAsExisting(foundryResourceName, rg);

var pg = builder.AddPostgres("pg")
    .WithPgAdmin()
    .WithInitFiles(Path.Combine(Environment.CurrentDirectory, "..", "..", "..", "scripts"))
    // Use the pgvector image for PostgreSQL with pgvector extension
    .WithImage("pgvector/pgvector", "pg17")
    .WithLifetime(ContainerLifetime.Persistent)
    ;

var zava = pg.AddDatabase("zava");
var storeManagerUser = zava.AddPostgresAccount(
    "store-manager",
    builder.AddParameter("store-manager-user", "store_manager"),
    builder.AddParameter("store-manager-password", "StoreManager123!"));

var devtunnel = builder.AddDevTunnel("mcp-devtunnel");

builder.AddMcpInspector("mcp-inspector");

var dotnetMcpServer = builder.AddProject<Projects.McpAgentWorkshop_McpServer>("dotnet-mcp-server")
    .WithReference(storeManagerUser)
    .WaitFor(zava)
    .WithDevTunnel(devtunnel)
    .WithReference(appInsights);

var dotnetAgentApp = builder.AddProject<Projects.McpAgentWorkshop_WorkshopApi>("dotnet-agent-app")
    .WithReference(dotnetMcpServer)
    .WaitFor(dotnetMcpServer)
    .WaitFor(devtunnel)
    .WithDevTunnelEnvironmentVariable(devtunnel, dotnetMcpServer)
    .WithReference(appInsights)
    .WithReference(foundry)
    .WithEnvironment("MODEL_DEPLOYMENT_NAME", chatDeployment)
    .WithEnvironment("EMBEDDING_MODEL_DEPLOYMENT_NAME", embeddingDeployment)
    .WithEnvironment("FoundryProjectName", foundryProjectName)
    .WithEnvironment("AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED", "true");

builder.AddFrontend("dotnet-chat-frontend")
    .WithReference(dotnetAgentApp)
    .WaitFor(dotnetAgentApp);

if (args.Contains("--python"))
{
    builder.AddPythonWorkshop(zava, devtunnel, appInsights, foundryEndpoint, chatDeployment, embeddingDeployment, aoai);
}

builder.Build().Run();
