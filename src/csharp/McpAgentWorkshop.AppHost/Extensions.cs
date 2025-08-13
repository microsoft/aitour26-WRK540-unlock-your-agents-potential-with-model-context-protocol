using Aspire.Hosting.Python;

namespace Aspire.Hosting;

public static class Extensions
{
    public static IResourceBuilder<PythonAppResource> WithPostgres(this IResourceBuilder<PythonAppResource> builder, IResourceBuilder<PostgresDatabaseResource> db)
    {
        builder.WithEnvironment("POSTGRES_URL", () => $"postgresql://{db.Resource.Parent.UserNameParameter?.ToString() ?? "postgres"}:{db.Resource.Parent.PasswordParameter.Value}@{db.Resource.Parent.PrimaryEndpoint.Host}:{db.Resource.Parent.PrimaryEndpoint.Port}/{db.Resource.Name}")
               .WaitFor(db);

        return builder;
    }
}
