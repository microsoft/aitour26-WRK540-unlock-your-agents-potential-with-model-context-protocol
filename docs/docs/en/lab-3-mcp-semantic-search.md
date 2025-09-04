## What You'll Learn

In this lab, you enable semantic search capabilities in the Azure AI Agent using the MCP Server and the PostgreSQL database with the [PostgreSQL Vector](https://github.com/pgvector/pgvector){:target="\_blank"} extension enabled.

## Introduction

This lab upgrades the Azure AI Agent with semantic search using the MCP Server and PostgreSQL. 

All of Zava's product names and descriptions have been converted to vectors with the OpenAI embedding model (text-embedding-3-small) and stored in the database. This enables the agent to understand user intent and provide more accurate responses.

??? info "For Developers: How does PostgreSQL Semantic Search work?"

    ### Vectorizing the Product Descriptions and Names

    To learn more about how Zava product names and descriptions were vectorized, see the [Zava DIY PostgreSQL Database Generator README](https://github.com/microsoft/aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol/tree/main/data/database){:target="_blank"}.



    === "Python"

        ### LLM calls the MCP Server Tool

        Based on the user's query and the instructions provided, the LLM decides to call the MCP Server tool `semantic_search_products` to find relevant products.

        The following sequence of events occurs:

        1. The MCP tool `semantic_search_products` is invoked with the user's query description.
        1. The MCP server generates a vector for the query using the OpenAI embedding model (text-embedding-3-small). See the code for vectorizing the query is in the `generate_query_embedding` method.
        1. The MCP server then performs a semantic search against the PostgreSQL database to find products with similar vectors.

        ### PostgreSQL Semantic Search Overview

        The `semantic_search_products` MCP Server tool then executes a SQL query that uses the vectorized query to find the most similar product vectors in the database. The SQL query uses the `<->` operator provided by the pgvector extension to calculate the distance between vectors.

        ```python
        async def search_products_by_similarity(
            self, query_embedding: list[float], 
                rls_user_id: str, 
                max_rows: int = 20, 
                similarity_threshold: float = 30.0
        ) -> str:
                ...
                query = f"""
                    SELECT 
                        p.*,
                        (pde.description_embedding <=> $1::vector) as similarity_distance
                    FROM {SCHEMA_NAME}.product_description_embeddings pde
                    JOIN {SCHEMA_NAME}.products p ON pde.product_id = p.product_id
                    WHERE (pde.description_embedding <=> $1::vector) <= $3
                    ORDER BY similarity_distance
                    LIMIT $2
                """

                rows = await conn.fetch(query, embedding_str, max_rows, distance_threshold)
                ...
        ```



    === "C#"

        ### LLM calls the MCP Server Tool

        Based on the user's query and the instructions provided, the LLM decides to call the MCP Server tool `semantic_search_products` to find relevant products.

        The following sequence of events occurs:

        1. The MCP tool `semantic_search_products` is invoked with the user's query description.
        2. The MCP server generates a vector for the query using the OpenAI embedding model (text-embedding-3-small). See `GenerateVectorAsync` method in the `EmbeddingGeneratorExtensions.cs` file.
        3. The MCP server then performs a semantic search against the PostgreSQL database to find products with similar vectors.

        ### PostgreSQL Semantic Search Overview

        The `semantic_search_products` MCP Server tool then executes a SQL query that uses the vectorized query to find the most similar product vectors in the database. The SQL query uses the `<->` operator provided by the pgvector extension to calculate the distance between vectors.

        ```csharp
        public async Task<IEnumerable<SemanticSearchResult>> SemanticSearchProductsAsync(
        ...
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
        ```

## Lab Exercise

From the previous lab you can ask the agent questions about sales data, but it was limited to exact matches. In this lab, you extend the agent's capabilities by implementing semantic search using the Model Context Protocol (MCP). This will allow the agent to understand and respond to queries that are not exact matches, improving its ability to assist users with more complex questions.

1. Paste the following question into the Web Chat tab in your browser:

   ```text
   What 18 amp circuit breakers do we sell?
   ```

   The agent responds with something similar to this message:

   _"I couldn’t find any specific 18 amp circuit breakers in our inventory. However, we may have other types of circuit breakers available. Would you like me to search for general circuit breakers or any other related products? 😊"_

## Stop the Agent App

From VS Code, stop the agent app by pressing <kbd>Shift + F5</kbd>.

=== "Python"

    ## Implement Semantic Search

    In this section, you will implement semantic search using the Model Context Protocol (MCP) to enhance the agent's capabilities.

    1. Press <kbd>F1</kbd> to **open** the VS Code Command Palette.
    2. Type **Open File** and select **File: Open File...**.
    3. **Paste** the following path into the file picker and press <kbd>Enter</kbd>:

        ```text
        /workspace/src/python/mcp_server/sales_analysis/sales_analysis.py
        ```

    4. Scroll down to around line 70 and look for the `semantic_search_products` method. This method is responsible for performing semantic search on the sales data. You'll notice the **@mcp.tool()** decorator is commented out. This decorator is used to register the method as an MCP tool, allowing it to be called by the agent.

    5. Uncomment the `@mcp.tool()` decorator by removing the `#` at the beginning of the line. This will enable the semantic search tool.

        ```python
        # @mcp.tool()
        async def semantic_search_products(
            ctx: Context,
            query_description: Annotated[str, Field(
            ...
        ```

    6. Next, you need to enable the Agent instructions to use the semantic search tool. Switch back to the `app.py` file.
    7. Scroll down to around line 30 and find the line `# INSTRUCTIONS_FILE = "instructions/mcp_server_tools_with_semantic_search.txt"`.
    8. Uncomment the line by removing the `#` at the beginning. This will enable the agent to use the semantic search tool.

        ```python
        INSTRUCTIONS_FILE = "instructions/mcp_server_tools_with_semantic_search.txt"
        ```

=== "C#"

    ## Implement Semantic Search

    In this section, you will implement semantic search using the Model Context Protocol (MCP) to enhance the agent's capabilities.

    1. Open the `McpHost.cs` file.
    1. Locate where the other MCP tools are registered with the MCP server, and register the `SemanticSearchTools` class as an MCP tool.

        ```csharp
        builder.Services.AddMcpTool<SemanticSearchTools>();
        ```

        !!! info "Note"
            Have a read of the implementation of `SemanticSearchTools` to learn how the MCP server will be performing the search.

    1. Next, you need to enable the Agent instructions to use the semantic search tool. Switch back to the `AgentService` class and change the const `InstructionsFile` to `mcp_server_tools_with_semantic_search.txt`.

## Review the Agent Instructions

1. Press <kbd>F1</kbd> to open the VS Code Command Palette.
2. Type **Open File** and select **File: Open File...**.
3. Paste the following path into the file picker and press <kbd>Enter</kbd>:

   ```text
   /workspace/src/shared/instructions/mcp_server_tools_with_semantic_search.txt
   ```

4. Review the instructions in the file. These instructions instruct the agent to use the semantic search tool to answer questions about sales data.

## Start the Agent App with the Semantic Search Tool

1. **Start** the agent app by pressing <kbd>F5</kbd>. This will start the agent with the updated instructions and the semantic search tool enabled.
2. Open the **Web Chat** in your browser.
3. Enter the following question in the chat:

    ```text
    What 18 amp circuit breakers do we sell?
    ```

    The agent now understands the semantic meaning of the question and responds accordingly with relevant sales data.

    !!! info "Note"
        The MCP Semantic Search tool works as follows:

        1. The question is converted into a vector using the same OpenAI embedding model (text-embedding-3-small) as the product descriptions.
        2. This vector is used to search for similar product vectors in the PostgreSQL database.
        3. The agent receives the results and uses them to generate a response.

## Write an Executive Report

The final prompt for this workshop is as follows:

```plaintext
Write an executive report on the sales performance of different stores for these circuit breakers.
```

## Leave the Agent App Running

Leave the agent app running as you will use it in the next lab to explore secure agent data access.
