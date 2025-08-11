namespace McpAgentWorkshop.WorkshopApi.Models;

public record ChatResponse(bool Done);

public record ChatErrorResponse(string Error) : ChatResponse(true);

public record ChatContentResponse(string Content) : ChatResponse(false);

public record ChatFileResponse(Dictionary<string, string> FileInfo) : ChatResponse(false);

public record ChatCompletionResponse() : ChatResponse(true);