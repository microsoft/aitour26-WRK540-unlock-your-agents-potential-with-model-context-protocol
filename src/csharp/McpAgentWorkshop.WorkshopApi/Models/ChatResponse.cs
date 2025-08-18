using System.Text.Json.Serialization;

namespace McpAgentWorkshop.WorkshopApi.Models;

[JsonDerivedType(typeof(ChatContentResponse))]
[JsonDerivedType(typeof(ChatErrorResponse))]
[JsonDerivedType(typeof(ChatFileResponse))]
[JsonDerivedType(typeof(ChatCompletionResponse))]
public record ChatResponse(bool Done);

public record ChatErrorResponse(string Error) : ChatResponse(true);

public record ChatContentResponse(string Content) : ChatResponse(false);

public record ChatFileResponse([property: JsonPropertyName("file_info")] AssistantFileInfo FileInfo) : ChatResponse(false);

public record ChatCompletionResponse() : ChatResponse(true);
