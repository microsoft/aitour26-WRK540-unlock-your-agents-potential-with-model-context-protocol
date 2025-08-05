namespace AspireDevTunnels.AppHost.Commands;

internal static class DevTunnelCommandArgs
{
    public static List<string> CreateTunnelArguments(string tunnelId) =>
        ["create", tunnelId, "--json"];

    public static List<string> AddPortArguments(int port, string protocol) =>
        ["port", "add", "-p", port.ToString(), "--protocol", protocol, "--json"];

    public static List<string> AllowAnonymousAccessArguments(string tunnelId) =>
        ["access", "create", tunnelId, "--anonymous"];

    public static List<string> GetTunnelDetailsArguments(string tunnelId) =>
        ["show", tunnelId, "--json"];

    public static List<string> GetPortDetailsArguments(string tunnelId, int port) =>
        ["port", "show", tunnelId, "--port-number", port.ToString(), "--json"];

    public static List<string> GetAuthTokenArguments(string tunnelId) =>
        ["token", tunnelId, "--scopes", "connect", "--json"];

    public static List<string> VerifyDevTunnelCliInstalledArguments() =>
        ["--version"];

    public static List<string> VerifyUserLoggedInArguments() =>
        ["user", "show", "--json"];
}
