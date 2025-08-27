using System.Text.Json.Serialization;

namespace McpAgentWorkshop.WorkshopApi.Models;

public record ChatRequest(
    string Message,
    [property: JsonPropertyName("session_id")] string? SessionId,
    [property: JsonPropertyName("rls_user_id")] string? RlsUserId);
