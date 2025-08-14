using System.ComponentModel;
using ModelContextProtocol.Server;

namespace McpAgentWorkshop.McpServer.Tools;

[McpServerToolType]
public class EchoTools
{
    [McpServerTool, Description("Echoes the provided message back to the caller.")]
    public static string Echo([Description("The message to echo back")] string message)
    {
        return $"Echo: {message}";
    }
}