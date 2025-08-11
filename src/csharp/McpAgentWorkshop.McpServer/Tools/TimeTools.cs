using System.ComponentModel;
using System.Diagnostics;
using ModelContextProtocol.Server;

namespace McpAgentWorkshop.McpServer.Tools;

[McpServerToolType]
public class TimeTools
{
    [McpServerTool]
    [Description("Get the current UTC date and time in ISO format. Useful for date-based queries, filtering recent data, or understanding the current context for time-sensitive analysis.")]
    public static string GetCurrentUtcDate()
    {
        var activity = Diagnostics.ActivitySource.StartActivity(
            name: nameof(GetCurrentUtcDate),
            kind: ActivityKind.Server,
            links: Diagnostics.ActivityLinkFromCurrent());

        return $"Current UTC Date/Time: {DateTime.UtcNow:yyyy-MM-ddTHH:mm:ss.fffffZ}";
    }
}