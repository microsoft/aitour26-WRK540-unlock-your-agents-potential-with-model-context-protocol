using System.Text.Json;
using McpAgentWorkshop.WorkshopApi.Models;

var builder = WebApplication.CreateBuilder(args);

builder.AddServiceDefaults();

builder.Services.AddHealthChecks().AddCheck<AgentAvailableHealthCheck>("test");

var app = builder.Build();

app.MapDefaultEndpoints();

app.MapPost("/chat/stream", (ChatRequest request, ILogger<Program> logger) =>
    TypedResults.Stream(async (stream) =>
    {
        var writer = new StreamWriter(stream);

        if (string.IsNullOrEmpty(request.Message))
        {
            logger.LogError("Received empty message");

            await writer.WriteStreamingResponseAsync(new ChatErrorResponse("Message was empty"));
        }
        else
        {
            await writer.WriteStreamingResponseAsync(new ChatContentResponse(request.Message));

            await Task.Delay(1000); // Simulate processing delay

            await writer.WriteStreamingResponseAsync(new ChatCompletionResponse());
        }

        await writer.FlushAsync();
    }));

app.Run();

internal static class StreamWriterExtensions
{
    internal static async Task WriteStreamingResponseAsync<T>(this StreamWriter writer, T data)
    {
        await writer.WriteLineAsync($"data: {JsonSerializer.Serialize(data)}");
        await writer.WriteLineAsync();  // Empty line is required for SSE
        await writer.FlushAsync();
    }
}
