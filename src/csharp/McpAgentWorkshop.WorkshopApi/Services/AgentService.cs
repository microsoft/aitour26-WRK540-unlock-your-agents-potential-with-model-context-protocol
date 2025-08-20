using System.ClientModel;
using System.Runtime.CompilerServices;
using Azure.AI.Agents.Persistent;
using McpAgentWorkshop.WorkshopApi.Models;

namespace McpAgentWorkshop.WorkshopApi.Services;

public class AgentService(
    PersistentAgentsClient persistentAgentsClient,
    IWebHostEnvironment hostEnvironment,
    IConfiguration configuration,
    ILogger<AgentService> logger) : IAsyncDisposable
{
    private PersistentAgent? persistentAgent;
    private readonly IDictionary<string, PersistentAgentThread> sessionThreads = new Dictionary<string, PersistentAgentThread>();
    private readonly SemaphoreSlim sessionLock = new(1, 1);
    private readonly SemaphoreSlim agentLock = new(1, 1);
    private const string AgentName = "Zava DIY Sales Analysis Agent";
    private const string InstructionsFile = "mcp_server_tools_with_code_interpreter.txt";
    private const string ZavaMcpToolLabel = "ZavaSalesAnalysisMcpServer";
    private readonly string sharedPath = Path.Combine(hostEnvironment.ContentRootPath, "..", "..", "shared");

    public bool IsAgentAvailable => persistentAgent is not null;

    public async ValueTask DisposeAsync()
    {
        foreach (var thread in sessionThreads.Values)
        {
            await persistentAgentsClient.Threads.DeleteThreadAsync(thread.Id);
        }

        if (persistentAgent is not null)
        {
            await persistentAgentsClient.Administration.DeleteAgentAsync(persistentAgent.Id);
        }

        sessionLock.Dispose();
        agentLock.Dispose();
    }

    public async Task InitialiseAsync()
    {
        logger.LogInformation("Initialising agent service...");

        // Create or find the single agent
        persistentAgent = await GetOrCreateAgentAsync();
    }

    private async Task<PersistentAgent> GetOrCreateAgentAsync()
    {
        // var agentsList = persistentAgentsClient.Administration.GetAgentsAsync();

        // await foreach (var agent in agentsList)
        // {
        //     if (agent.Name == AgentName)
        //     {
        //         logger.LogInformation("Found existing agent: {AgentName}", agent.Name);
        //         return agent;
        //     }
        // }

        // Create new agent if not found
        return await CreateAgentAsync();
    }

    private async Task<PersistentAgent> CreateAgentAsync()
    {
        logger.LogInformation("Creating new agent: {AgentName}", AgentName);

        var instructions = Path.Combine(sharedPath, "instructions", InstructionsFile);

        using var stream = new FileStream(instructions, FileMode.Open, FileAccess.Read);
        using var reader = new StreamReader(stream);
        var instructionsContent = await reader.ReadToEndAsync();

        string? devtunnelUrl = configuration.GetValue<string>("DEV_TUNNEL_URL");

        if (devtunnelUrl is null)
        {
            logger.LogError("DEV_TUNNEL_URL configuration is missing. Cannot create agent.");
            throw new InvalidOperationException("DEV_TUNNEL_URL configuration is required to create the agent.");
        }

        devtunnelUrl = devtunnelUrl.EndsWith('/') ? devtunnelUrl : devtunnelUrl + "/";

        var mcpTool = new MCPToolDefinition(ZavaMcpToolLabel, devtunnelUrl + "mcp");

        // Create agent without tool resources - we'll set them per run
        PersistentAgent pa = await persistentAgentsClient.Administration.CreateAgentAsync(
                name: AgentName,
                model: configuration.GetValue<string>("MODEL_DEPLOYMENT_NAME"),
                instructions: instructionsContent,
                temperature: 0.1f,
                tools: [mcpTool, new CodeInterpreterToolDefinition()]);

        logger.LogInformation("Agent created with ID: {AgentId}", pa.Id);

        return pa;
    }

    private async Task<PersistentAgentThread> GetOrCreateThreadAsync(string sessionId, CancellationToken cancellationToken = default)
    {
        await sessionLock.WaitAsync();
        try
        {
            if (sessionThreads.TryGetValue(sessionId, out var existingThread))
            {
                return existingThread;
            }

            // Create new thread for this session
            var threadResponse = await persistentAgentsClient.Threads.CreateThreadAsync(cancellationToken: cancellationToken);
            var thread = threadResponse.Value;
            sessionThreads[sessionId] = thread;
            logger.LogInformation("Created new thread {ThreadId} for session {SessionId}", thread.Id, sessionId);

            return thread;
        }
        finally
        {
            sessionLock.Release();
        }
    }

    public async Task ClearSessionThreadAsync(string sessionId)
    {
        await sessionLock.WaitAsync();
        try
        {
            if (sessionThreads.TryGetValue(sessionId, out var thread))
            {
                if (persistentAgent is not null)
                {
                    using var activity = Diagnostics.ActivitySource.StartActivity("Zava Agent Chat Thread Deletion");
                    activity?.SetTag("thread_id", thread.Id);
                    activity?.SetTag("session_id", sessionId);
                    activity?.SetTag("agent_id", persistentAgent.Id);
                    activity?.SetTag("date_time", DateTime.UtcNow.ToString("O"));

                    await persistentAgentsClient.Threads.DeleteThreadAsync(thread.Id);
                }
                sessionThreads.Remove(sessionId);
            }
        }
        finally
        {
            sessionLock.Release();
        }

        logger.LogInformation("Cleared thread for session {SessionId}", sessionId);
    }

    private async IAsyncEnumerable<ChatResponse> HandleStreamingUpdateAsync(StreamingUpdate update, ToolResources toolResources)
    {
        switch (update.UpdateKind)
        {
            case StreamingUpdateReason.MessageUpdated:
                // The agent has a response to the user - stream the content
                var messageContentUpdate = (MessageContentUpdate)update;
                yield return new ChatContentResponse(messageContentUpdate.Text ?? "");
                yield break;

            case StreamingUpdateReason.RunRequiresAction:
                // The run requires an action from the application, such as a tool output submission
                var submitToolApprovalUpdate = (SubmitToolApprovalUpdate)update;
                logger.LogInformation("Approving MCP tool call: {Name}, Arguments: {Arguments}", submitToolApprovalUpdate.Name, submitToolApprovalUpdate.Arguments);
                List<ToolApproval> toolApprovals = [];

                ToolApproval toolApproval = PersistentAgentsModelFactory.ToolApproval(
                    submitToolApprovalUpdate.ToolCallId,
                    true,
                    toolResources.Mcp.SelectMany(mcp => mcp.Headers).ToDictionary(h => h.Key, h => h.Value));

                toolApprovals.Add(toolApproval);

                var toolOutputStream = persistentAgentsClient.Runs.SubmitToolOutputsToStreamAsync(submitToolApprovalUpdate, toolOutputs: [], toolApprovals: toolApprovals);
                await foreach (var toolUpdate in toolOutputStream)
                {
                    var response = HandleStreamingUpdateAsync(toolUpdate, toolResources);
                    await foreach (var res in response)
                    {
                        yield return res;
                    }
                }
                yield break;

            case StreamingUpdateReason.MessageCompleted:
                // Message is complete - handle any file content
                var messageStatusUpdate = (MessageStatusUpdate)update;
                var threadMessage = messageStatusUpdate.Value;
                foreach (var contentItem in threadMessage.ContentItems)
                {
                    if (contentItem is MessageImageFileContent imageContent)
                    {
                        var fileInfo = await DownloadImageFileContentAsync(imageContent);
                        yield return new ChatFileResponse(fileInfo);
                    }
                }
                yield break;

            case StreamingUpdateReason.RunCompleted:
                // The run is complete
                yield return new ChatCompletionResponse();
                yield break;

            case StreamingUpdateReason.RunFailed:
                // The run failed
                var runFailedUpdate = (RunUpdate)update;
                var errorMessage = runFailedUpdate.Value.LastError?.Message ?? "Unknown error";
                yield return new ChatErrorResponse($"Run failed: {errorMessage}");
                yield break;

            default:
                yield break;
        }
    }

    /// <summary>
    /// Process chat message and stream responses.
    /// This method implements the same logic as the Python process_chat_message method,
    /// including session management, message creation, and streaming responses.
    /// </summary>
    public async IAsyncEnumerable<ChatResponse> ProcessChatMessageAsync(ChatRequest request, [EnumeratorCancellation] CancellationToken cancellationToken)
    {
        if (persistentAgent is null)
        {
            yield return new ChatErrorResponse("Agent not initialized");
            yield break;
        }

        if (string.IsNullOrWhiteSpace(request.Message))
        {
            yield return new ChatErrorResponse("Empty message");
            yield break;
        }

        if (string.IsNullOrWhiteSpace(request.RlsUserId))
        {
            yield return new ChatErrorResponse("RLS User ID is required");
            yield break;
        }

        var sessionId = request.SessionId ?? "default";

        // Create a span for this chat request  
        var messagePreview = request.Message.Length > 50 ?
            request.Message[..50] + "..." :
            request.Message;
        var spanName = $"Zava Agent Chat Request: {messagePreview}";

        using var activity = Diagnostics.ActivitySource.StartActivity(spanName);

        PersistentAgentThread sessionThread;
        AsyncCollectionResult<StreamingUpdate>? streamingUpdates = null;
        string? errorMessage = null;
        // Create tool resources for this RLS user
        var mcpToolResource = new MCPToolResource(ZavaMcpToolLabel, new Dictionary<string, string>
        {
            { "x-rls-user-id", request.RlsUserId }
        });
        var toolResources = new ToolResources();
        toolResources.Mcp.Add(mcpToolResource);


        try
        {
            // Get or create thread for this session
            sessionThread = await GetOrCreateThreadAsync(sessionId, cancellationToken: cancellationToken);

            // Add some attributes to the span for better observability
            activity?.SetTag("user_message", request.Message);
            activity?.SetTag("operation_type", "chat_request");
            activity?.SetTag("agent_id", persistentAgent!.Id);
            activity?.SetTag("thread_id", sessionThread.Id);
            activity?.SetTag("session_id", sessionId);
            activity?.SetTag("rls_user_id", request.RlsUserId);

            // Create message in thread  
            await persistentAgentsClient.Messages.CreateMessageAsync(
                threadId: sessionThread.Id,
                role: MessageRole.User,
                content: request.Message,
                cancellationToken: cancellationToken);

            // Create run options with dynamic tool resources
            var runOptions = new CreateRunStreamingOptions
            {
                MaxCompletionTokens = 2 * 10240,
                MaxPromptTokens = 6 * 10240,
                Temperature = 0.1f,
                TopP = 0.1f,
                TruncationStrategy = new Truncation(TruncationStrategy.LastMessages) { LastMessages = 5 },
                ToolResources = toolResources
            };

            // Start streaming run with dynamic tool resources
            streamingUpdates = persistentAgentsClient.Runs.CreateRunStreamingAsync(
                threadId: sessionThread.Id,
                agentId: persistentAgent.Id,
                options: runOptions,
                cancellationToken: cancellationToken
            );
        }
        catch (Exception e)
        {
            logger.LogError(e, "Processing chat message failed");
            errorMessage = $"Streaming error: {e.Message}";
        }

        if (errorMessage is not null)
        {
            yield return new ChatErrorResponse(errorMessage);
            yield break;
        }

        await foreach (var update in streamingUpdates!)
        {
            var response = HandleStreamingUpdateAsync(update, toolResources);
            await foreach (var res in response)
            {
                yield return res;
            }
        }
    }

    private async Task<AssistantFileInfo> DownloadImageFileContentAsync(MessageImageFileContent imageContent)
    {
        logger.LogInformation("Getting file with ID: {FileId}", imageContent.FileId);

        BinaryData fileContent = await persistentAgentsClient.Files.GetFileContentAsync(imageContent.FileId);
        string directory = Path.Combine(sharedPath, "files");
        if (!Directory.Exists(directory))
        {
            Directory.CreateDirectory(directory);
        }

        string fileName = imageContent.FileId + ".png";
        string filePath = Path.Combine(directory, fileName);
        await File.WriteAllBytesAsync(filePath, fileContent.ToArray());

        logger.LogInformation("File save to {Path}", Path.GetFullPath(filePath));

        return new AssistantFileInfo(FileId: imageContent.FileId,
            FileName: fileName,
            FilePath: filePath,
            RelativePath: Path.Combine("files", fileName),
            IsImage: true,
            AttachmentName: fileName);
    }

    internal async Task<byte[]?> GetFileInfoAsync(string path)
    {
        string fullPath = Path.Combine(sharedPath, "files", path);

        if (!File.Exists(fullPath))
        {
            return null;
        }

        return await File.ReadAllBytesAsync(fullPath);
    }
}
