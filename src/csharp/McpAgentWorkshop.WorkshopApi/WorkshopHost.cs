using McpAgentWorkshop.WorkshopApi.Extensions;
using McpAgentWorkshop.WorkshopApi.Models;
using McpAgentWorkshop.WorkshopApi.Services;

var builder = WebApplication.CreateBuilder(args);

builder.AddServiceDefaults();

builder.Services.AddHealthChecks().AddCheck<AgentAvailableHealthCheck>("agent_available");

builder.AddPersistentAgentsClient("ai-foundry");

builder.Services.AddSingleton<AgentService>();

var app = builder.Build();

app.MapDefaultEndpoints();

app.MapPost("/chat/stream", (ChatRequest request, ILogger<Program> logger, HttpContext context, AgentService agentService, CancellationToken cancellationToken) =>
{
    context.Response.Headers.CacheControl = "no-cache";
    context.Response.Headers.Connection = "keep-alive";

    return TypedResults.Stream(async (stream) =>
    {
        IAsyncEnumerable<ChatResponse> responseStream = agentService.ProcessChatMessageAsync(request, cancellationToken);

        var writer = new StreamWriter(stream);

        await foreach (var response in responseStream)
        {
            await writer.WriteStreamingResponseAsync(response);
        }

    }, contentType: "text/event-stream");
});

app.MapGet("/files/{*path}", async (string path, AgentService agentService) =>
{
    var fileInfo = await agentService.GetFileInfoAsync(path);
    return fileInfo is not null ? TypedResults.File(fileInfo) : Results.NotFound();
});

var agentService = app.Services.GetRequiredService<AgentService>();
await agentService.InitialiseAsync();

app.Run();
