using System.Diagnostics;

namespace McpAgentWorkshop.WorkshopApi;

internal static class Diagnostics
{
    public static readonly ActivitySource ActivitySource = new("McpAgentWorkshop.WorkshopApi", "1.0.0");
}
