using McpAgentWorkshop.McpServer.Tools;
using Npgsql;

var builder = WebApplication.CreateBuilder(args);

builder.AddServiceDefaults();

builder.Services.AddMcpServer()
    .WithHttpTransport(o => o.Stateless = true)
    .WithTools<EchoTools>()
    .WithTools<DatabaseSchemaTools>()
    .WithTools<SalesTools>()
    .WithTools<TimeTools>();

builder.Services.AddHttpContextAccessor();

builder.AddNpgsqlDataSource("store-manager", configureDataSourceBuilder: dsb =>
{
    dsb.UseVector();
});

builder.AddAzureOpenAIClient("ai-foundry")
    .AddEmbeddingGenerator(builder.Configuration.GetValue<string>("EMBEDDING_MODEL_DEPLOYMENT_NAME") ?? "text-embedding-3-small");

var app = builder.Build();

app.MapDefaultEndpoints();

app.MapMcp("/mcp");

app.Run();
