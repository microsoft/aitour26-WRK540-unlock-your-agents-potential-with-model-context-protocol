namespace McpAgentWorkshop.McpServer;

internal static class HttpContextAccessorExtensions
{
    internal static string GetRequestUserId(this IHttpContextAccessor httpContextAccessor)
    {
        if (httpContextAccessor.HttpContext is null)
        {
            throw new InvalidOperationException("HttpContext is not available.");
        }

        var rlsHeader = httpContextAccessor.HttpContext.Request.Headers["x-rls-user-id"].FirstOrDefault();
        if (string.IsNullOrEmpty(rlsHeader))
        {
            rlsHeader = "00000000-0000-0000-0000-000000000000";
        }

        return rlsHeader;
    }

}