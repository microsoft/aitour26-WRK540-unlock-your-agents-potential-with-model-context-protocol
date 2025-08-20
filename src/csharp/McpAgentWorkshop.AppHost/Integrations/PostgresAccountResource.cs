namespace McpAgentWorkshop.AppHost.Integrations;

public class PostgresAccountResource(string name, PostgresDatabaseResource postgresDatabase, ParameterResource username, ParameterResource password) : Resource(name), IResourceWithConnectionString
{
    public PostgresDatabaseResource PostgresDatabase { get; } = postgresDatabase;
    public ParameterResource Username { get; } = username;
    public ParameterResource Password { get; } = password;

    private ReferenceExpression ConnectionString =>
        ReferenceExpression.Create(
            $"Host={PostgresDatabase.Parent.PrimaryEndpoint.Property(EndpointProperty.Host)};Port={PostgresDatabase.Parent.PrimaryEndpoint.Property(EndpointProperty.Port)};Username={Username};Password={Password};Database={PostgresDatabase.DatabaseName}");

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
