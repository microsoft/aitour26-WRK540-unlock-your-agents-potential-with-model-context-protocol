using System.ComponentModel;
using System.Diagnostics;
using System.Text;
using ModelContextProtocol.Server;
using Npgsql;

namespace McpAgentWorkshop.McpServer.Tools;

[McpServerToolType]
public class DatabaseSchemaTools
{
    [McpServerTool, Description("Retrieve schemas for multiple tables. Use this tool only for schemas you have not already fetched during the conversation.")]
    public static async Task<string> GetMultipleTableSchemasAsync(
        IHttpContextAccessor httpContextAccessor,
        ILogger<DatabaseSchemaTools> logger,
        NpgsqlConnection connection,
        [Description("List of table names. Valid table names include 'retail.customers', 'retail.stores', 'retail.categories', 'retail.product_types', 'retail.products', 'retail.orders', 'retail.order_items', 'retail.inventory'.")]
        string[] tableNames)
    {
        var activity = Diagnostics.ActivitySource.StartActivity(
            name: nameof(GetMultipleTableSchemasAsync),
            kind: ActivityKind.Server,
            links: Diagnostics.ActivityLinkFromCurrent());

        if (tableNames is null || tableNames.Length == 0)
        {
            logger.LogError("Table names cannot be null or empty.");
            throw new ArgumentException("Table names cannot be null or empty.", nameof(tableNames));
        }

        logger.LogInformation("Fetching schemas for tables: {TableNames}", string.Join(", ", tableNames));

        var rlsUserId = httpContextAccessor.GetRequestUserId();

        logger.LogInformation("RLS User ID: {RlsUserId}", rlsUserId);

        await connection.OpenAsync();

        using var command = connection.CreateCommand();
        command.CommandText = """
        SELECT set_config('app.current_rls_user_id', (@rlsUserId), false)
        """;
        command.Parameters.AddWithValue("rlsUserId", rlsUserId);

        await command.ExecuteNonQueryAsync();

        command.Parameters.Clear();
        StringBuilder schemas = new();
        foreach (var tableName in tableNames)
        {
            try
            {
                var (schema, table) = ParseTableName(tableName);

                command.CommandText = """
                SELECT EXISTS (
                    SELECT 1 FROM information_schema.tables 
                    WHERE table_schema = (@schema) AND table_name = (@table)
                )
                """;
                command.Parameters.Clear();
                command.Parameters.AddWithValue("schema", schema);
                command.Parameters.AddWithValue("table", table);

                var exists = (bool?)await command.ExecuteScalarAsync();
                if (exists is null || !exists.Value)
                {
                    schemas.Append($"**ERROR:** Table '{tableName}' not found");
                    continue;
                }

                var schemaData = await GetTableMetadataAsync(connection, tableName);
                var formattedSchema = FormatSchemaMetadataForAi(schemaData);

                schemas.Append($"\n\n{formattedSchema}");
            }
            catch (Exception e)
            {
                logger.LogError(e, "Error checking existence of table {TableName}", tableName);
                schemas.Append($"Error retrieving {tableName} schema: {e.Message}");
            }
        }

        return schemas.ToString();
    }

    private static (string schema, string table) ParseTableName(string tableName)
    {
        if (string.IsNullOrWhiteSpace(tableName) || !tableName.Contains('.'))
        {
            throw new ArgumentException($"Table name '{tableName}' must be in 'schema.table' format (e.g., 'retail.customers')", nameof(tableName));
        }

        var parts = tableName.Split('.', 2);
        if (parts.Length != 2 || string.IsNullOrWhiteSpace(parts[0]) || string.IsNullOrWhiteSpace(parts[1]))
        {
            throw new ArgumentException($"Table name '{tableName}' must be in 'schema.table' format (e.g., 'retail.customers')", nameof(tableName));
        }

        return (parts[0], parts[1]);
    }

    private static async Task<Dictionary<string, object>> GetTableMetadataAsync(NpgsqlConnection connection, string tableName)
    {
        var (schema, table) = ParseTableName(tableName);

        // Get column information
        var columns = new List<Dictionary<string, object>>();
        using (var cmd = connection.CreateCommand())
        {
            cmd.CommandText = """
                SELECT 
                    column_name,
                    data_type,
                    is_nullable,
                    column_default,
                    ordinal_position
                FROM information_schema.columns 
                WHERE table_schema = (@schema) AND table_name = (@table)
                ORDER BY ordinal_position
            """;
            cmd.Parameters.AddWithValue("schema", schema);
            cmd.Parameters.AddWithValue("table", table);

            using var reader = await cmd.ExecuteReaderAsync();
            while (await reader.ReadAsync())
            {
                columns.Add(new Dictionary<string, object>
                {
                    ["column_name"] = reader["column_name"],
                    ["data_type"] = reader["data_type"],
                    ["is_nullable"] = reader["is_nullable"],
                    ["column_default"] = reader["column_default"],
                    ["ordinal_position"] = reader["ordinal_position"]
                });
            }
            cmd.Parameters.Clear();
        }

        // Get primary key information
        var pkColumns = new HashSet<string>();
        using (var cmd = connection.CreateCommand())
        {
            cmd.CommandText = """
                SELECT kcu.column_name
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu 
                    ON tc.constraint_name = kcu.constraint_name
                    AND tc.table_schema = kcu.table_schema
                WHERE tc.constraint_type = 'PRIMARY KEY'
                    AND tc.table_schema = (@schema) 
                    AND tc.table_name = (@table)
            """;
            cmd.Parameters.AddWithValue("schema", schema);
            cmd.Parameters.AddWithValue("table", table);

            using var reader = await cmd.ExecuteReaderAsync();
            while (await reader.ReadAsync())
            {
                pkColumns.Add(reader["column_name"].ToString() ?? "");
            }
            cmd.Parameters.Clear();
        }

        // Get foreign key information
        var foreignKeys = new List<Dictionary<string, object>>();
        using (var cmd = connection.CreateCommand())
        {
            cmd.CommandText = """
                SELECT 
                    kcu.column_name,
                    ccu.table_name AS foreign_table_name,
                    ccu.column_name AS foreign_column_name
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu 
                    ON tc.constraint_name = kcu.constraint_name
                    AND tc.table_schema = kcu.table_schema
                JOIN information_schema.constraint_column_usage ccu 
                    ON ccu.constraint_name = tc.constraint_name
                    AND ccu.table_schema = tc.table_schema
                WHERE tc.constraint_type = 'FOREIGN KEY'
                    AND tc.table_schema = (@schema) 
                    AND tc.table_name = (@table)
            """;
            cmd.Parameters.AddWithValue("schema", schema);
            cmd.Parameters.AddWithValue("table", table);

            using var reader = await cmd.ExecuteReaderAsync();
            while (await reader.ReadAsync())
            {
                foreignKeys.Add(new Dictionary<string, object>
                {
                    ["column"] = reader["column_name"],
                    ["references_table"] = reader["foreign_table_name"],
                    ["references_column"] = reader["foreign_column_name"],
                    ["description"] = $"{reader["column_name"]} links to {reader["foreign_table_name"]}.{reader["foreign_column_name"]}",
                    ["relationship_type"] = InferRelationshipType($"{schema}.{reader["foreign_table_name"]}")
                });
            }
            cmd.Parameters.Clear();
        }

        var columnsFormat = string.Join(", ", columns.Select(col => $"{col["column_name"]}:{col["data_type"]}"));

        // Enum queries (example for stores, categories, etc.)
        var enumData = new Dictionary<string, object>();
        var lowerTable = table.ToLowerInvariant();
        if (lowerTable == "stores")
        {
            enumData["available_stores"] = await FetchDistinctValuesAsync(connection, "store_name", $"{schema}.stores");
        }
        else if (lowerTable == "categories")
        {
            enumData["available_categories"] = await FetchDistinctValuesAsync(connection, "category_name", $"{schema}.categories");
        }
        else if (lowerTable == "product_types")
        {
            enumData["available_product_types"] = await FetchDistinctValuesAsync(connection, "type_name", $"{schema}.product_types");
        }
        else if (lowerTable == "orders")
        {
            enumData["available_years"] = await FetchDistinctYearsAsync(connection, $"{schema}.orders");
        }

        var schemaData = new Dictionary<string, object>
        {
            ["table_name"] = tableName,
            ["parsed_table_name"] = table,
            ["schema_name"] = schema,
            ["description"] = $"Table containing {table} data",
            ["columns_format"] = columnsFormat,
            ["columns"] = columns.Select(col => new Dictionary<string, object>
            {
                ["name"] = col["column_name"],
                ["type"] = col["data_type"],
                ["primary_key"] = pkColumns.Contains(col["column_name"].ToString() ?? ""),
                ["required"] = (col["is_nullable"]?.ToString() ?? "") == "NO",
                ["default_value"] = col["column_default"]
            }).ToList(),
            ["foreign_keys"] = foreignKeys
        };

        foreach (var kvp in enumData)
            schemaData[kvp.Key] = kvp.Value;

        return schemaData;
    }

    private static async Task<List<string>> FetchDistinctValuesAsync(NpgsqlConnection connection, string column, string qualifiedTable)
    {
        var values = new List<string>();
        using var cmd = connection.CreateCommand();
        cmd.CommandText = $"SELECT DISTINCT {column} FROM {qualifiedTable} WHERE {column} IS NOT NULL ORDER BY {column}";
        using var reader = await cmd.ExecuteReaderAsync();
        while (await reader.ReadAsync())
        {
            if (reader[0] != DBNull.Value)
                values.Add(reader[0].ToString() ?? "");
        }
        return values;
    }

    private static async Task<List<string>> FetchDistinctYearsAsync(NpgsqlConnection connection, string qualifiedTable)
    {
        var years = new List<string>();
        using var cmd = connection.CreateCommand();
        cmd.CommandText = $"SELECT DISTINCT EXTRACT(YEAR FROM order_date)::text as year FROM {qualifiedTable} WHERE order_date IS NOT NULL ORDER BY year";
        using var reader = await cmd.ExecuteReaderAsync();
        while (await reader.ReadAsync())
        {
            if (reader["year"] != DBNull.Value)
                years.Add(reader["year"].ToString() ?? "");
        }
        return years;
    }

    private static string InferRelationshipType(string referencesTable)
    {
        var knownManyToOne = new HashSet<string>
        {
            "customers", "products", "stores", "categories", "product_types", "orders"
        };
        var parts = referencesTable.Split('.', 2);
        var tableName = parts.Length == 2 ? parts[1] : referencesTable;
        return knownManyToOne.Contains(tableName) ? "many_to_one" : "one_to_many";
    }

    private static string FormatSchemaMetadataForAi(Dictionary<string, object> schema)
    {
        if (schema.TryGetValue("error", out object? value))
            return $"**ERROR:** {value}";

        var tableDisplay = schema.GetValueOrDefault("table_name")?.ToString() ?? "unknown";
        string tableDescription;
        try
        {
            var (_, tableNameOnly) = ParseTableName(tableDisplay);
            tableDescription = tableNameOnly.Replace("_", " ");
        }
        catch
        {
            tableDescription = tableDisplay.Replace("_", " ");
        }

        var lines = new List<string>
        {
            $"# Table: {tableDisplay}",
            "",
            $"**Purpose:** {schema.GetValueOrDefault("description", "No description available")}",
            "\n## Schema",
            schema.GetValueOrDefault("columns_format", "N/A")?.ToString() ?? "N/A"
        };

        if (schema.TryGetValue("foreign_keys", out var fkObj) && fkObj is IEnumerable<object> foreignKeys && foreignKeys.Any())
        {
            lines.Add("\n## Relationships");
            foreach (var fkDict in foreignKeys.Cast<Dictionary<string, object>>())
            {
                var currentSchema = schema.GetValueOrDefault("schema_name")?.ToString();
                var fkTableRef = !string.IsNullOrEmpty(currentSchema)
                    ? $"{currentSchema}.{fkDict.GetValueOrDefault("references_table")}"
                    : fkDict.GetValueOrDefault("references_table")?.ToString();
                lines.Add(
                    $"- `{fkDict.GetValueOrDefault("column")}` → `{fkTableRef}.{fkDict.GetValueOrDefault("references_column")}` ({fkDict.GetValueOrDefault("relationship_type")?.ToString()?.ToUpperInvariant()})"
                );
            }
        }

        var enumFields = new (string key, string label)[]
        {
            ("available_stores", "Valid Stores"),
            ("available_categories", "Valid Categories"),
            ("available_product_types", "Valid Product Types"),
            ("available_years", "Available Years"),
            ("price_range", "Price Range"),
        };

        var enumLines = new List<string>();
        foreach (var (fieldKey, label) in enumFields)
        {
            if (schema.TryGetValue(fieldKey, out var valuesObj) && valuesObj is not null)
            {
                if (valuesObj is IEnumerable<string> valuesList)
                    enumLines.Add($"**{label}:** {string.Join(", ", valuesList)}");
                else
                    enumLines.Add($"**{label}:** {valuesObj}");
            }
        }

        if (enumLines.Count > 0)
        {
            lines.Add("\n## Valid Values");
            lines.AddRange(enumLines);
        }

        lines.Add("\n## Query Hints");
        lines.Add($"- Use `{tableDisplay}` for queries about {tableDescription}");
        if (schema.TryGetValue("foreign_keys", out fkObj) && fkObj is IEnumerable<object> foreignKeys2 && foreignKeys2.Any())
        {
            foreach (var fkDict in foreignKeys2.Cast<Dictionary<string, object>>())
            {
                var currentSchema = schema.GetValueOrDefault("schema_name")?.ToString();
                var fkTableRef = !string.IsNullOrEmpty(currentSchema)
                    ? $"{currentSchema}.{fkDict.GetValueOrDefault("references_table")}"
                    : fkDict.GetValueOrDefault("references_table")?.ToString();
                lines.Add($"- Join with `{fkTableRef}` using `{fkDict.GetValueOrDefault("column")}`");
            }
        }

        return string.Join("\n", lines) + "\n";
    }
}
