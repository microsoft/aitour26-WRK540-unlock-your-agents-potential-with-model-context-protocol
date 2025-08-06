using System.Diagnostics;
using System.Text.Json;

namespace AspireDevTunnels.AppHost.Commands;

internal class DevTunnelCommands
{
    private static readonly JsonSerializerOptions jsonSerializerOptions = new(JsonSerializerDefaults.Web);

    public static async Task<T> RunProcessAsync<T>(
        List<string> commandLineArgs,
        CancellationToken cancellationToken = default)
    {
        DevTunnelCommandResult<T> devTunnelCommandResult =
            await TryRunProcessAsync<T>(commandLineArgs, cancellationToken);

        return devTunnelCommandResult.IsSuccess
            ? devTunnelCommandResult.Value
            : throw new Exception($"Error: {devTunnelCommandResult.Error}");
    }

    public static async Task<DevTunnelCommandResult> RunProcessAsync(
        List<string> commandLineArgs,
        CancellationToken cancellationToken = default)
    {
        DevTunnelCommandResult devTunnelCommandResult =
            await TryRunProcessAsync(commandLineArgs, cancellationToken);

        return devTunnelCommandResult.IsSuccess
            ? devTunnelCommandResult
            : throw new Exception($"Error: {devTunnelCommandResult.Error}");
    }

    public static async Task<DevTunnelCommandResult<T>> TryRunProcessAsync<T>(
        List<string> commandLineArgs,
        CancellationToken cancellationToken = default)
    {
        DevTunnelCommandResult devTunnelCommandResult =
            await TryRunProcessAsync(commandLineArgs, cancellationToken);

        string errorMessage = devTunnelCommandResult switch
        {
            { ExitCode: < 0 } => $"Error: {devTunnelCommandResult.Error}",
            { ExitCode: > 0 } => $"Error: {devTunnelCommandResult.Error}",
            { Error: not null } => devTunnelCommandResult.Error,

            { } when string.IsNullOrWhiteSpace(devTunnelCommandResult.Output) =>
                "No output received from the command: " + string.Join(" ", commandLineArgs),

            _ => devTunnelCommandResult.Error,
        };

        if (string.IsNullOrEmpty(errorMessage))
        {
            T devTunnelCommandResultValue =
                JsonSerializer.Deserialize<T>(devTunnelCommandResult.Output,
                    jsonSerializerOptions);

            return new DevTunnelCommandResult<T>(
                devTunnelCommandResultValue,
                devTunnelCommandResult.Output,
                devTunnelCommandResult.Error,
                devTunnelCommandResult.ExitCode);
        }
        else
        {
            return new DevTunnelCommandResult<T>(
                default,
                devTunnelCommandResult.Output,
                errorMessage,
                !devTunnelCommandResult.IsSuccess
                ? devTunnelCommandResult.ExitCode
                : -1);
        }
    }

    public static async Task<DevTunnelCommandResult> TryRunProcessAsync(
        List<string> commandLineArgs,
        CancellationToken cancellationToken = default)
    {
        ProcessStartInfo processStartInfo = GenerateProcessStartInfo(commandLineArgs);

        using Process process = new()
        {
            StartInfo = processStartInfo,
        };

        process.Start();

        string output = await process.StandardOutput.ReadToEndAsync(cancellationToken);
        string error = await process.StandardError.ReadToEndAsync(cancellationToken);

        await process.WaitForExitAsync(cancellationToken);

        return new DevTunnelCommandResult(output, error, process.ExitCode);
    }

    public static ProcessStartInfo GenerateProcessStartInfo(List<string> commandLineArgs) =>
        new()
        {
            FileName = "devtunnel",
            Arguments = string.Join(" ", commandLineArgs),
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            UseShellExecute = false,
            CreateNoWindow = true,
        };
}
