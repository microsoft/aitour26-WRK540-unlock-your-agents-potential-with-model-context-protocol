using McpAgentWorkshop.McpServer.Tools;

var builder = WebApplication.CreateBuilder(args);

builder.AddServiceDefaults();

builder.Services.AddMcpServer()
    .WithHttpTransport(o => o.Stateless = true)
    .WithTools<EchoTools>()
    .WithTools<DatabaseSchemaTools>()
    .WithTools<SalesTools>()
    .WithTools<TimeTools>();

builder.Services.AddHttpContextAccessor();

builder.AddNpgsqlDataSource("zava");

var app = builder.Build();

app.MapDefaultEndpoints();

app.MapMcp("/mcp");

app.Run();
