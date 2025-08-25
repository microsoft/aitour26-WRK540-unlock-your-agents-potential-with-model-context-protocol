using Azure.AI.Agents.Persistent;
using McpAgentWorkshop.WorkshopApi.Models;

namespace McpAgentWorkshop.WorkshopApi.Services;

public partial class AgentService
{
    private readonly IDictionary<string, PersistentAgentThread> sessionThreads = new Dictionary<string, PersistentAgentThread>();
    private readonly SemaphoreSlim sessionLock = new(1, 1);
    private readonly SemaphoreSlim agentLock = new(1, 1);
    private readonly string sharedPath = Path.Combine(hostEnvironment.ContentRootPath, "..", "..", "shared");
    private const int maxCompletionTokens = 2 * 10240;
    private const int maxPromptTokens = 6 * 10240;
    private const float modelTemperature = 0.1f;
    private const float topP = 0.1f;

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

    private async Task<PersistentAgentThread> GetOrCreateThreadAsync(string sessionId, CancellationToken cancellationToken = default)
    {
        await sessionLock.WaitAsync(cancellationToken);
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
