using AspireDevTunnels.AppHost.Commands;
using AspireDevTunnels.AppHost.Resources;

namespace AspireDevTunnels.AppHost.Extensions;

internal static class DevTunnelResourceExtensions
{
    public static async Task<DevTunnel> CreateTunnelAsync(
        this DevTunnelResource devTunnelResource,
        CancellationToken cancellationToken = default)
    {
        Console.WriteLine($"Creating tunnel {devTunnelResource.Name}...");

        List<string> commandLineArgs = DevTunnelCommandArgs.CreateTunnelArguments(devTunnelResource.Name);

        return await DevTunnelCommands.RunProcessAsync<DevTunnel>(commandLineArgs, cancellationToken);
    }

    public static async Task<DevTunnelPort> AddPortAsync(
        this DevTunnelResource devTunnelResource,
        int port,
        string protocol = "https",
        CancellationToken cancellationToken = default)
    {
        Console.WriteLine($"Adding tunnel {devTunnelResource.Name} port {port}...");

        List<string> commandLineArgs = DevTunnelCommandArgs.AddPortArguments(port, protocol);

        return await DevTunnelCommands.RunProcessAsync<DevTunnelPort>(commandLineArgs, cancellationToken);
    }

    public static async Task AllowAnonymousAccessAsync(
        this DevTunnelResource devTunnelResource,
        CancellationToken cancellationToken = default)
    {
        Console.WriteLine($"Allowing Anonymous Access for {devTunnelResource.Name}...");

        List<string> commandLineArgs = DevTunnelCommandArgs.AllowAnonymousAccessArguments(devTunnelResource.Name);

        await DevTunnelCommands.RunProcessAsync(commandLineArgs, cancellationToken);
    }

    public static async Task<DevTunnelAccessInfo> GetAuthTokenAsync(
        this DevTunnelResource devTunnelResource,
        CancellationToken cancellationToken = default)
    {
        Console.WriteLine($"Retrieving auth token for {devTunnelResource.Name}...");

        List<string> commandLineArgs = DevTunnelCommandArgs.GetAuthTokenArguments(devTunnelResource.Name);

        return await DevTunnelCommands.RunProcessAsync<DevTunnelAccessInfo>(commandLineArgs, cancellationToken);
    }

    public static async Task<DevTunnel> GetTunnelDetailsAsync(
        this DevTunnelResource devTunnelResource,
        CancellationToken cancellationToken = default)
    {
        Console.WriteLine($"Retrieving tunnel details for {devTunnelResource.Name}...");

        List<string> commandLineArgs = DevTunnelCommandArgs.GetTunnelDetailsArguments(devTunnelResource.Name);

        // Silent error since this is used to detect existing tunnel which will fails if does not exist (first time run)
        DevTunnelCommandResult<DevTunnel> devTunnelCommandResult =
            await DevTunnelCommands.TryRunProcessAsync<DevTunnel>(commandLineArgs, cancellationToken);

        return devTunnelCommandResult.Value;
    }

    public static async Task<DevTunnelPort> GetPortDetailsAsync(
        this DevTunnelResource devTunnelResource,
        int port,
        CancellationToken cancellationToken = default)
    {
        Console.WriteLine($"Retrieving port details for {devTunnelResource.Name} port {port}...");

        List<string> commandLineArgs = DevTunnelCommandArgs.GetPortDetailsArguments(devTunnelResource.Name, port);

        // Silent error since this is used to detect existing ports which will fails if does not exist (first time run)
        DevTunnelCommandResult<DevTunnelPort> devTunnelCommandResult =
            await DevTunnelCommands.TryRunProcessAsync<DevTunnelPort>(commandLineArgs, cancellationToken);

        return devTunnelCommandResult.Value;
    }

    public static async Task VerifyDevTunnelCliInstalledAsync(
        this DevTunnelResource devTunnelResource,
        CancellationToken cancellationToken = default)
    {
        Console.WriteLine($"Verifying DevTunnel Resources Exist on machine for tunnel {devTunnelResource.Name}...");

        List<string> commandLineArgs = DevTunnelCommandArgs.VerifyDevTunnelCliInstalledArguments();

        DevTunnelCommandResult devTunnelCommandResult =
            await DevTunnelCommands.TryRunProcessAsync(commandLineArgs, cancellationToken);

        if (!devTunnelCommandResult.IsSuccess)
        {
            throw new InvalidOperationException(
                "DevTunnel CLI is not installed. Please install from https://learn.microsoft.com/en-us/azure/developer/dev-tunnels/get-started.");
        }
    }

    public static async Task VerifyUserLoggedInAsync(
        this DevTunnelResource devTunnelResource,
        CancellationToken cancellationToken = default)
    {
        Console.WriteLine($"Verifying User is Logged in for tunnel {devTunnelResource.Name}...");

        List<string> commandLineArgs = DevTunnelCommandArgs.VerifyUserLoggedInArguments();

        DevTunnelUserInfo devTunnelUserInfo =
            await DevTunnelCommands.RunProcessAsync<DevTunnelUserInfo>(commandLineArgs, cancellationToken);

        // Exit code is still 0 when user is not logged in.
        // Sample output: { "status": "Not logged in" }
        if (devTunnelUserInfo.Status.Contains("Not logged in", StringComparison.OrdinalIgnoreCase))
        {
            throw new InvalidOperationException(
                "No Logged In User detected. Please log in using 'devtunnel user login'.");
        }
        else
        {
            Console.WriteLine($"Logged In User: {devTunnelUserInfo.Username}");
        }
    }

    public static bool VerifyShouldInitialize(
        this DevTunnelResource devTunnelResource)
    {
        Console.WriteLine($"Detecting explicit startup properties for tunnel {devTunnelResource.Name}...");

        ExplicitStartupAnnotation? explicitStartAnnotation = devTunnelResource.Annotations
            .OfType<ExplicitStartupAnnotation>()
            .FirstOrDefault();

        return explicitStartAnnotation is null || (devTunnelResource.SkippedInitializationForExplicitStart && !devTunnelResource.IsInitialized);
    }
}
