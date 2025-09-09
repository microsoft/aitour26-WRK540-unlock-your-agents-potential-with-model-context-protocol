# 实验 3：MCP 语义搜索

## 您将学到什么

在本实验中，您将使用 MCP 服务器和启用了 [PostgreSQL Vector](https://github.com/pgvector/pgvector){:target="\_blank"} 扩展的 PostgreSQL 数据库在 Azure AI 代理中启用语义搜索功能。

## 简介

本实验使用 MCP 服务器和 PostgreSQL 升级 Azure AI 代理的语义搜索功能。

所有 Zava 的产品名称和描述都已使用 OpenAI 嵌入模型 (text-embedding-3-small) 转换为向量并存储在数据库中。这使代理能够理解用户意图并提供更准确的响应。

??? info "面向开发人员：PostgreSQL 语义搜索如何工作？"

    ### 产品描述和名称向量化

    要了解更多关于 Zava 产品名称和描述如何向量化的信息，请参阅 [Zava DIY PostgreSQL 数据库生成器 README](https://github.com/microsoft/aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol/tree/main/data/database){:target="_blank"}。



    === "Python"

        ### LLM 调用 MCP 服务器工具

        基于用户的查询和提供的指令，LLM 决定调用 MCP 服务器工具 `semantic_search_products` 来查找相关产品。

        发生以下事件序列：

        1. 使用用户的查询描述调用 MCP 工具 `semantic_search_products`。
        1. MCP 服务器使用 OpenAI 嵌入模型 (text-embedding-3-small) 为查询生成向量。查看查询向量化的代码在 `generate_query_embedding` 方法中。
        1. 然后 MCP 服务器对 PostgreSQL 数据库执行语义搜索，以查找具有相似向量的产品。

        ### PostgreSQL 语义搜索概述

        `semantic_search_products` MCP 服务器工具然后执行一个 SQL 查询，该查询使用向量化查询在数据库中查找最相似的产品向量。SQL 查询使用 pgvector 扩展提供的 `<->` 运算符来计算向量之间的距离。

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

        ### LLM 调用 MCP 服务器工具

        基于用户的查询和提供的指令，LLM 决定调用 MCP 服务器工具 `semantic_search_products` 来查找相关产品。

        发生以下事件序列：

        1. 使用用户的查询描述调用 MCP 工具 `semantic_search_products`。
        2. MCP 服务器使用 OpenAI 嵌入模型 (text-embedding-3-small) 为查询生成向量。请参阅 `EmbeddingGeneratorExtensions.cs` 文件中的 `GenerateVectorAsync` 方法。
        3. 然后 MCP 服务器对 PostgreSQL 数据库执行语义搜索，以查找具有相似向量的产品。

        ### PostgreSQL 语义搜索概述

        `semantic_search_products` MCP 服务器工具然后执行一个 SQL 查询，该查询使用向量化查询在数据库中查找最相似的产品向量。SQL 查询使用 pgvector 扩展提供的 `<->` 运算符来计算向量之间的距离。

        ```csharp
        public async Task<IEnumerable<SemanticSearchResult>> SemanticSearchProductsAsync(
        ...
            await using var searchCmd = new NpgsqlCommand("""
            SELECT 
                p.*,
                (pde.description_embedding <=> $1::vector) as similarity_distance
            FROM retail.product_description_embedings pde
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

## 实验练习

从上一个实验中，您可以向代理询问有关销售数据的问题，但仅限于精确匹配。在本实验中，您通过使用模型上下文协议 (MCP) 实现语义搜索来扩展代理的功能。这将允许代理理解并响应不是精确匹配的查询，提高其协助用户处理更复杂问题的能力。

1. 将以下问题粘贴到浏览器中的 Web Chat 选项卡：

   ```text
   What 18 amp circuit breakers do we sell?
   ```

   代理响应类似于以下消息：

   _"我在我们的库存中找不到任何特定的 18 安培断路器。不过，我们可能有其他类型的断路器可用。您想让我搜索一般断路器或其他相关产品吗？😊"_

## 停止代理应用

从 VS Code，按 <kbd>Shift + F5</kbd> 停止代理应用。

=== "Python"

    ## 实现语义搜索

    在本节中，您将使用模型上下文协议 (MCP) 实现语义搜索，以增强代理的功能。

    1. 按 <kbd>F1</kbd> **打开** VS Code 命令面板。
    2. 键入**Open File**并选择**File: Open File...**。
    3. 将以下路径**粘贴**到文件选择器中并按 <kbd>Enter</kbd>：

        ```text
        /workspace/src/python/mcp_server/sales_analysis/sales_analysis.py
        ```

    4. 向下滚动到大约第 70 行，查找 `semantic_search_products` 方法。此方法负责对销售数据执行语义搜索。您会注意到 **@mcp.tool()** 装饰器被注释掉了。此装饰器用于将方法注册为 MCP 工具，允许代理调用它。

    5. 通过删除行开头的 `#` 来取消注释 `@mcp.tool()` 装饰器。这将启用语义搜索工具。

        ```python
        # @mcp.tool()
        async def semantic_search_products(
            ctx: Context,
            query_description: Annotated[str, Field(
            ...
        ```

    6. 接下来，您需要启用代理指令以使用语义搜索工具。切换回 `app.py` 文件。
    7. 向下滚动到大约第 30 行，找到行 `# INSTRUCTIONS_FILE = "instructions/mcp_server_tools_with_semantic_search.txt"`。
    8. 通过删除开头的 `#` 来取消注释该行。这将使代理能够使用语义搜索工具。

        ```python
        INSTRUCTIONS_FILE = "instructions/mcp_server_tools_with_semantic_search.txt"
        ```

=== "C#"

    ## 实现语义搜索

    在本节中，您将使用模型上下文协议 (MCP) 实现语义搜索，以增强代理的功能。

    1. 从 `McpAgentWorkshop.WorkshopApi` 项目中打开 `McpHost.cs` 文件。
    1. 找到其他 MCP 工具在 MCP 服务器中注册的位置，并将 `SemanticSearchTools` 类注册为 MCP 工具。

        ```csharp
        builder.Services.AddMcpTool<SemanticSearchTools>();
        ```

        !!! info "注意"
            阅读 `SemanticSearchTools` 的实现，了解 MCP 服务器如何执行搜索。

    1. 接下来，您需要启用代理指令以使用语义搜索工具。切换回 `AgentService` 类并将常量 `InstructionsFile` 更改为 `mcp_server_tools_with_semantic_search.txt`。

## 查看代理指令

1. 按 <kbd>F1</kbd> 打开 VS Code 命令面板。
2. 键入**Open File**并选择**File: Open File...**。
3. 将以下路径粘贴到文件选择器中并按 <kbd>Enter</kbd>：

   ```text
   /workspace/src/shared/instructions/mcp_server_tools_with_semantic_search.txt
   ```

4. 查看文件中的指令。这些指令指示代理使用语义搜索工具回答有关销售数据的问题。

## 启动带有语义搜索工具的代理应用

1. 按 <kbd>F5</kbd> **启动**代理应用。这将启动具有更新指令和启用语义搜索工具的代理。
2. 在浏览器中打开**Web Chat**。
3. 在聊天中输入以下问题：

    ```text
    What 18 amp circuit breakers do we sell?
    ```

    代理现在理解问题的语义含义，并相应地用相关销售数据进行响应。

    !!! info "注意"
        MCP 语义搜索工具的工作原理如下：

        1. 问题使用与产品描述相同的 OpenAI 嵌入模型 (text-embedding-3-small) 转换为向量。
        2. 此向量用于在 PostgreSQL 数据库中搜索相似的产品向量。
        3. 代理接收结果并使用它们生成响应。

## 编写执行报告

本工作坊的最后提示如下：

```plaintext
Write an executive report on the sales performance of different stores for these circuit breakers.
```

## 保持代理应用运行

让代理应用保持运行，因为您将在下一个实验中使用它来探索安全的代理数据访问。

*使用 GitHub Copilot 翻译。*
