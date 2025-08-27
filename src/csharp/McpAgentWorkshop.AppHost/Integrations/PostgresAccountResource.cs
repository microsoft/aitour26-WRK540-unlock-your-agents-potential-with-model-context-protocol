using Aspire.Hosting.Azure;

namespace McpAgentWorkshop.AppHost.Integrations;

public class PostgresAccountResource(string name, AzurePostgresFlexibleServerDatabaseResource postgresDatabase, ParameterResource username, ParameterResource password) : Resource(name), IResourceWithConnectionString
{
    public AzurePostgresFlexibleServerDatabaseResource PostgresDatabase { get; } = postgresDatabase;
    public ParameterResource Username { get; } = username;
    public ParameterResource Password { get; } = password;

    private ReferenceExpression ConnectionString =>
        ReferenceExpression.Create(
            $"{PostgresDatabase.ConnectionStringExpression};Username={Username};Password={Password};Database={PostgresDatabase.DatabaseName}");

    /// <summary>
    /// Gets the connection string expression for the PostgreSQL server.
    /// </summary>
    public ReferenceExpression ConnectionStringExpression
    {
        get
        {
            if (this.TryGetLastAnnotation<ConnectionStringRedirectAnnotation>(out var connectionStringAnnotation))
            {
                return connectionStringAnnotation.Resource.ConnectionStringExpression;
            }

            return ConnectionString;
        }
    }
}
