using Aspire.Hosting.Azure;

var builder = DistributedApplication.CreateBuilder(args);

var chatDeployment = builder.AddParameter("ChatModelDeploymentName");
var embeddingDeployment = builder.AddParameter("EmbeddingModelDeploymentName");
var rg = builder.AddParameter("ResourceGroupName");
var foundryResourceName = builder.AddParameter("FoundryResourceName");
var foundryProjectName = builder.AddParameter("FoundryProjectName");
var appInsightsName = builder.AddParameter("ApplicationInsightsName");
var uniqueSuffix = builder.Configuration["Parameters:UniqueSuffix"] ?? Environment.MachineName.ToLowerInvariant().Replace(".", "-").Replace("_", "-")[..4];

var appInsights = builder.AddAzureApplicationInsights("app-insights")
    .RunAsExisting(appInsightsName, rg);

var foundry = builder.AddAzureAIFoundry("ai-foundry")
    .RunAsExisting(foundryResourceName, rg);

var devtunnel = builder.AddDevTunnel($"mcp-devtunnel-{uniqueSuffix}")
    .WithAnonymousAccess();

IResourceBuilder<IResourceWithConnectionString> storeManagerUser;
IResourceBuilder<AzurePostgresFlexibleServerDatabaseResource>? zava = null;

if (builder.Configuration["ConnectionStrings:Postgres"] is not null)
{
    storeManagerUser = builder.AddConnectionString("store-manager", ReferenceExpression.Create($"{builder.Configuration["ConnectionStrings:Postgres"]}"));
}
else
{
    var pg = builder.AddAzurePostgresFlexibleServer("pg");
    if (builder.Configuration["Parameters:PostgresName"] is not null)
    {
        pg.RunAsExisting(builder.AddParameter("PostgresName"), rg);
    }
    else
    {
        pg.RunAsContainer(configureContainer: containerBuilder =>
        {
            containerBuilder
                .WithPgAdmin()
                .WithInitFiles(Path.Combine(Environment.CurrentDirectory, "..", "..", "..", "scripts"))
                // Use the pgvector image for PostgreSQL with pgvector extension
                .WithImage("pgvector/pgvector", "pg17")
                .WithLifetime(ContainerLifetime.Persistent);
        });

    }
    zava = pg.AddDatabase("zava");
    storeManagerUser = zava.AddPostgresAccount(
        "store-manager",
        builder.AddParameter("store-manager-user", "store_manager"),
        builder.AddParameter("store-manager-password", "StoreManager123!"));
}

var mcpServer = builder.AddProject<Projects.McpAgentWorkshop_McpServer>("dotnet-mcp-server")
    .WithReference(storeManagerUser)
    .WithReference(appInsights)
    .WithReference(foundry)
    .WaitFor(foundry);
devtunnel.WithReference(mcpServer);

if (zava is not null)
{
    mcpServer.WaitFor(zava);
}

var agentApp = builder.AddProject<Projects.McpAgentWorkshop_WorkshopApi>("dotnet-agent-app")
    .WithReference(mcpServer)
    .WaitFor(mcpServer)
    .WaitFor(devtunnel)
    .WithReference(appInsights)
    .WithReference(foundry)
    .WaitFor(foundry)
    .WithEnvironment("MODEL_DEPLOYMENT_NAME", chatDeployment)
    .WithEnvironment("EMBEDDING_MODEL_DEPLOYMENT_NAME", embeddingDeployment)
    .WithEnvironment("FoundryProjectName", foundryProjectName)
    .WithEnvironment("AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED", "true")
    .WithReference(mcpServer, devtunnel);

builder.AddFrontend("dotnet-chat-frontend")
    .WithReference(agentApp)
    .WaitFor(agentApp);

builder.AddMcpInspector("mcp-inspector")
    .WithMcpServer(mcpServer, isDefault: true);

builder.Build().Run();
