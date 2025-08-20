namespace AspireDevTunnels.AppHost.Commands;

public class DevTunnelCommandResult(string output, string error, int exitCode)
{
    public string Output { get; init; } = output;

    public string Error { get; init; } = error;

    public int ExitCode { get; init; } = exitCode;

    public bool IsSuccess => ExitCode == 0;
}

public class DevTunnelCommandResult<T> : DevTunnelCommandResult
{
    public T Value { get; init; }

    public DevTunnelCommandResult(T value, string output, string error, int exitCode)
        : base(output, error, exitCode)
    {
        Value = value;
    }
}
