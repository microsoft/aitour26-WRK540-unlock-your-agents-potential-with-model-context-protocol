using System.Text.Json.Serialization;

namespace McpAgentWorkshop.WorkshopApi.Models;

public record RlsUserResult(string Message, [property: JsonPropertyName("rls_user_id")] string RlsUserId);