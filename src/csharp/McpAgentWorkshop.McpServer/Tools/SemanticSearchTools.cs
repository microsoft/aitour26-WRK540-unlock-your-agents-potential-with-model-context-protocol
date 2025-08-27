using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using Microsoft.Extensions.AI;
using ModelContextProtocol.Server;
using Npgsql;
using Pgvector;

namespace McpAgentWorkshop.McpServer.Tools;

[McpServerToolType]
public class SemanticSearchTools
{
    [McpServerTool, Description("Search for Zava products using natural language descriptions to find matches based on semantic similarity—considering functionality, form, use, and other attributes.")]
    public async Task<IEnumerable<SemanticSearchResult>> SemanticSearchProductsAsync(
        NpgsqlConnection connection,
        IEmbeddingGenerator<string, Embedding<float>> embeddingGenerator,
        ILogger<SalesTools> logger,
        IHttpContextAccessor httpContextAccessor,
        [Description("Describe the Zava product you're looking for using natural language. Include purpose, features, or use case. For example: 'waterproof electrical box for outdoor use', '15 amp circuit breaker', or 'LED light bulbs for kitchen ceiling'.")] string query,
        [Description("The maximum number of products to return. Defaults to 20.")] int maxRows = 20,
        [Description("A value between 20 and 80 that sets the minimum similarity threshold. Products below this value are excluded. Defaults to 30.0.")] float similarityThreshold = 30f)
    {
        if (similarityThreshold < 20f || similarityThreshold > 80f)
            throw new ArgumentOutOfRangeException(nameof(similarityThreshold), similarityThreshold, "similarityThreshold must be between 20 and 80 (inclusive).");

        var activity = Diagnostics.ActivitySource.StartActivity(
                    name: nameof(SemanticSearchProductsAsync),
                    kind: ActivityKind.Server,
                    links: Diagnostics.ActivityLinkFromCurrent());

        var rlsUserId = httpContextAccessor.GetRequestUserId();

        logger.LogInformation("Semantic search query: {Query}", query);
        logger.LogInformation("Manager ID: {UserId}", rlsUserId);
        logger.LogInformation("Max rows: {MaxRows}", maxRows);

        var embeddings = await embeddingGenerator.GenerateVectorAsync(query);

        // Convert similarity percentage threshold to distance threshold
        // Similarity percentage = (1 - distance) * 100
        // So distance = 1 - (similarity_percentage / 100)
        var distanceThreshold = 1.0 - (similarityThreshold / 100.0);

        try
        {
            await connection.OpenAsync();

            await using var cmd = new NpgsqlCommand("SELECT set_config('app.current_rls_user_id', @rlsUserId, false)", connection);
            cmd.Parameters.AddWithValue("rlsUserId", rlsUserId ?? string.Empty);
            await cmd.ExecuteNonQueryAsync();

            await using var searchCmd = new NpgsqlCommand("""
            SELECT 
                p.*,
                (pde.description_embedding <=> $1::vector) as similarity_distance
            FROM retail.product_description_embeddings pde
            JOIN retail.products p ON pde.product_id = p.product_id
            WHERE (pde.description_embedding <=> $1::vector) <= $3
            ORDER BY similarity_distance
            LIMIT $2
            """, connection);
            searchCmd.Parameters.AddWithValue(new Vector(embeddings));
            searchCmd.Parameters.AddWithValue(maxRows);
            searchCmd.Parameters.AddWithValue(distanceThreshold);

            await using var reader = await searchCmd.ExecuteReaderAsync();
            var results = new List<SemanticSearchResult>();
            while (await reader.ReadAsync())
            {
                results.Add(new SemanticSearchResult(
                    ProductId: reader.GetInt32("product_id"),
                    Sku: reader.GetString("sku"),
                    ProductName: reader.GetString("product_name"),
                    CategoryId: reader.GetInt32("category_id"),
                    TypeId: reader.GetInt32("type_id"),
                    Cost: reader.GetFloat("cost"),
                    BasePrice: reader.GetFloat("base_price"),
                    GrossMarginPercent: reader.GetFloat("gross_margin_percent"),
                    ProductDescription: reader.GetString("product_description"),
                    SimilarityDistance: reader.GetFloat("similarity_distance")));
            }

            return results;
        }
        catch (NpgsqlException ex)
        {
            logger.LogError(ex, "Database error during semantic search.");
            throw;
        }
        catch (Exception ex)
        {
            logger.LogError(ex, "Unexpected error during semantic search.");
            throw;
        }
    }
}

public record SemanticSearchResult(
    int ProductId,
    string Sku,
    string ProductName,
    int CategoryId,
    int TypeId,
    float Cost,
    float BasePrice,
    float GrossMarginPercent,
    string ProductDescription,
    float SimilarityDistance)
{
    public float SimilarityPercent => (1 - SimilarityDistance) * 100;
}