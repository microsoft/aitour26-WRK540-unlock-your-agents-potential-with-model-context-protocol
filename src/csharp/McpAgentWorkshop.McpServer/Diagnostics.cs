using System.Diagnostics;

namespace McpAgentWorkshop.McpServer;

internal static class Diagnostics
{
    internal static ActivitySource ActivitySource { get; } = new("McpAgentWorkshop.McpServer", "1.0.0");

    // internal static ActivityContext ExtractActivityContext(this DistributedContextPropagator propagator, JsonRpcMessage message)
    // {
    //     propagator.ExtractTraceIdAndState(message, ExtractContext, out var traceparent, out var tracestate);
    //     ActivityContext.TryParse(traceparent, tracestate, true, out var activityContext);
    //     return activityContext;
    // }

    internal static ActivityLink[] ActivityLinkFromCurrent() => Activity.Current is null ? [] : [new ActivityLink(Activity.Current.Context)];
}