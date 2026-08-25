using System.ClientModel;
using System.Diagnostics;
using System.Runtime.CompilerServices;
using Azure.AI.Agents.Persistent;
using McpAgentWorkshop.WorkshopApi.Models;

namespace McpAgentWorkshop.WorkshopApi.Services;

public partial class AgentService(
    PersistentAgentsClient persistentAgentsClient,
    IWebHostEnvironment hostEnvironment,
    IConfiguration configuration,
    ILogger<AgentService> logger) : IAsyncDisposable
{
    private PersistentAgent? persistentAgent;
    private const string AgentName = "Zava DIY Sales Analysis Agent";
    private const string InstructionsFile = "mcp_server_tools_with_code_interpreter.txt";
    private const string ZavaMcpToolLabel = "ZavaSalesAnalysisMcpServer";

    public async Task InitialiseAgentAsync()
    {
        using var activity = Diagnostics.ActivitySource.StartActivity(name: "Zava Agent Initialization");

        logger.LogInformation("Creating new agent: {AgentName}", AgentName);

        var instructions = Path.Combine(sharedPath, "instructions", InstructionsFile);

        using var stream = new FileStream(instructions, FileMode.Open, FileAccess.Read);
        using var reader = new StreamReader(stream);
        var instructionsContent = await reader.ReadToEndAsync();

        string? devtunnelUrl = configuration.GetValue<string>("services:dotnet-mcp-server:http:0") ?? configuration.GetValue<string>("DEV_TUNNEL_URL");

        if (devtunnelUrl is null)
        {
            logger.LogError("DEV_TUNNEL_URL configuration is missing. Cannot create agent.");
            throw new InvalidOperationException("DEV_TUNNEL_URL configuration is required to create the agent.");
        }

        devtunnelUrl = devtunnelUrl.EndsWith('/') ? devtunnelUrl : devtunnelUrl + "/";

        // var mcpTool = new MCPToolDefinition(
        //     ZavaMcpToolLabel,
        //     devtunnelUrl + "mcp");

        // var codeInterpreterTool = new CodeInterpreterToolDefinition();

        // IEnumerable<ToolDefinition> tools = [mcpTool, codeInterpreterTool];

        // persistentAgent = await persistentAgentsClient.Administration.CreateAgentAsync(
        //         name: AgentName,
        //         model: configuration.GetValue<string>("MODEL_DEPLOYMENT_NAME"),
        //         instructions: instructionsContent,
        //         temperature: modelTemperature,
        //         tools: tools);

        // logger.LogInformation("Agent created with ID: {AgentId}", persistentAgent.Id);
    }

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

        using var activity = Diagnostics.ActivitySource.StartActivity(spanName, ActivityKind.Server);

        PersistentAgentThread sessionThread;
        AsyncCollectionResult<StreamingUpdate>? runStream = null;
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
                MaxCompletionTokens = maxCompletionTokens,
                MaxPromptTokens = maxPromptTokens,
                Temperature = modelTemperature,
                TopP = topP,
                TruncationStrategy = new Truncation(TruncationStrategy.LastMessages) { LastMessages = 5 },
                ToolResources = toolResources
            };

            // Start streaming run with dynamic tool resources
            runStream = persistentAgentsClient.Runs.CreateRunStreamingAsync(
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

        if (runStream is null)
        {
            yield return new ChatErrorResponse("Streaming error: No updates received");
            yield break;
        }

        await foreach (var update in runStream)
        {
            var responseStream = HandleStreamingUpdateAsync(update, toolResources);
            await foreach (var chatResponse in responseStream)
            {
                yield return chatResponse;
            }
        }
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
                // Simulate a human-in-the-loop workflow but we'll do auto-approval here
                var submitToolApprovalUpdate = (SubmitToolApprovalUpdate)update;
                logger.LogInformation("Approving MCP tool call: {Name}, Arguments: {Arguments}", submitToolApprovalUpdate.Name, submitToolApprovalUpdate.Arguments);
                List<ToolApproval> toolApprovals = [];

                ToolApproval toolApproval = PersistentAgentsModelFactory.ToolApproval(
                    submitToolApprovalUpdate.ToolCallId,
                    true,
                    // Forward on the MCP headers to the approval call. This ensures RLS flows through
                    toolResources.Mcp.SelectMany(mcp => mcp.Headers).ToDictionary(h => h.Key, h => h.Value));

                toolApprovals.Add(toolApproval);

                var toolOutputStream = persistentAgentsClient.Runs.SubmitToolOutputsToStreamAsync(submitToolApprovalUpdate, toolOutputs: [], toolApprovals: toolApprovals);
                await foreach (var toolUpdate in toolOutputStream)
                {
                    var approvalUpdateResponses = HandleStreamingUpdateAsync(toolUpdate, toolResources);
                    await foreach (var response in approvalUpdateResponses)
                    {
                        yield return response;
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
}
