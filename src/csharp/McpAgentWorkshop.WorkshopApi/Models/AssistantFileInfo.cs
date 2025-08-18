using System.Text.Json.Serialization;

namespace McpAgentWorkshop.WorkshopApi.Models;

public record AssistantFileInfo(
    [property: JsonPropertyName("file_id")] string FileId,
    [property: JsonPropertyName("file_name")] string FileName,
    [property: JsonPropertyName("file_path")] string FilePath,
    [property: JsonPropertyName("relative_path")] string RelativePath,
    [property: JsonPropertyName("is_image")] bool IsImage,
    [property: JsonPropertyName("attachment_name")] string AttachmentName);