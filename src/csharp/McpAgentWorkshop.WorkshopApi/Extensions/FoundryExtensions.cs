using System.Data.Common;
using Azure.AI.Agents.Persistent;
using Azure.Identity;

namespace McpAgentWorkshop.WorkshopApi.Extensions;

public static class FoundryExtensions
{
    public static void AddPersistentAgentsClient(this IHostApplicationBuilder builder, string name)
    {
        ArgumentException.ThrowIfNullOrEmpty(name, nameof(name));

        builder.Services.AddSingleton(sp =>
        {
            var config = sp.GetRequiredService<IConfiguration>();
            var connString = config.GetConnectionString(name);
            ArgumentException.ThrowIfNullOrEmpty(connString, $"Connection string '{name}' not found");

            var csb = new DbConnectionStringBuilder { ConnectionString = connString };
            if (!csb.TryGetValue("Endpoint", out var endpoint) || endpoint is not string endpointString)
            {
                throw new ArgumentException($"Connection string '{name}' must contain an 'Endpoint' key.");
            }

            var projectName = config.GetValue<string>("FoundryProjectName");
            ArgumentException.ThrowIfNullOrEmpty(projectName, $"Foundry project name not found");

            var projectsEndpoint = $"{endpointString}/api/projects/{projectName}";

            return new PersistentAgentsClient(projectsEndpoint, new AzureCliCredential());
        });
    }
}
