using System.Text.Json;
using McpAgentWorkshop.WorkshopApi.Models;

namespace McpAgentWorkshop.WorkshopApi.Extensions;

internal static class StreamWriterExtensions
{
    private static readonly JsonSerializerOptions serialisationOptions = new() { PropertyNamingPolicy = JsonNamingPolicy.CamelCase };

    internal static async Task WriteStreamingResponseAsync<T>(this StreamWriter writer, T data)
        where T : notnull, ChatResponse
    {
        await writer.WriteLineAsync($"data: {JsonSerializer.Serialize(data, serialisationOptions)}");
        await writer.WriteLineAsync();  // Empty line is required for SSE
        await writer.FlushAsync();
    }
}