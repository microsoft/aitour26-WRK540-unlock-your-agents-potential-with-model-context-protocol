## 学習内容

このラボでは、MCPサーバーと[PostgreSQL Vector](https://github.com/pgvector/pgvector){:target="\_blank"}拡張機能を有効にしたPostgreSQLデータベースを使用して、Azure AI Agentでセマンティック検索機能を有効にします。

## はじめに

このラボでは、MCPサーバーとPostgreSQLを使用してセマンティック検索でAzure AI Agentをアップグレードします。

Zavaのすべての製品名と説明は、OpenAI埋め込みモデル（text-embedding-3-small）でベクトルに変換され、データベースに格納されています。これにより、エージェントがユーザーの意図を理解し、より正確な応答を提供できるようになります。

??? info "開発者向け：PostgreSQLセマンティック検索の仕組みは？"

    ### 製品説明と名前のベクトル化

    Zava製品名と説明がどのようにベクトル化されたかについて詳しくは、[Zava DIY PostgreSQLデータベースジェネレーターREADME](https://github.com/microsoft/aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol/tree/main/data/database){:target="_blank"}を参照してください。



    === "Python"

        ### LLMがMCPサーバーツールを呼び出し

        ユーザーのクエリと提供された指示に基づいて、LLMは関連製品を見つけるためにMCPサーバーツール`semantic_search_products`を呼び出すことを決定します。

        以下のイベントシーケンスが発生します：

        1. MCPツール`semantic_search_products`がユーザーのクエリ説明で呼び出されます。
        1. MCPサーバーはOpenAI埋め込みモデル（text-embedding-3-small）を使用してクエリのベクトルを生成します。クエリのベクトル化コードは`generate_query_embedding`メソッドにあります。
        1. MCPサーバーは次に、PostgreSQLデータベースに対してセマンティック検索を実行し、類似ベクトルを持つ製品を見つけます。

        ### PostgreSQLセマンティック検索の概要

        `semantic_search_products` MCPサーバーツールは、ベクトル化されたクエリを使用してデータベース内の最も類似した製品ベクトルを見つけるSQLクエリを実行します。SQLクエリは、pgvector拡張機能が提供する`<->`演算子を使用してベクトル間の距離を計算します。

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

        ### LLMがMCPサーバーツールを呼び出し

        ユーザーのクエリと提供された指示に基づいて、LLMは関連製品を見つけるためにMCPサーバーツール`semantic_search_products`を呼び出すことを決定します。

        以下のイベントシーケンスが発生します：

        1. MCPツール`semantic_search_products`がユーザーのクエリ説明で呼び出されます。
        2. MCPサーバーはOpenAI埋め込みモデル（text-embedding-3-small）を使用してクエリのベクトルを生成します。`EmbeddingGeneratorExtensions.cs`ファイルの`GenerateVectorAsync`メソッドを参照してください。
        3. MCPサーバーは次に、PostgreSQLデータベースに対してセマンティック検索を実行し、類似ベクトルを持つ製品を見つけます。

        ### PostgreSQLセマンティック検索の概要

        `semantic_search_products` MCPサーバーツールは、ベクトル化されたクエリを使用してデータベース内の最も類似した製品ベクトルを見つけるSQLクエリを実行します。SQLクエリは、pgvector拡張機能が提供する`<->`演算子を使用してベクトル間の距離を計算します。

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

## ラボ演習

前のラボではエージェントに売上データについて質問できましたが、完全一致に限定されていました。このラボでは、Model Context Protocol（MCP）を使用してセマンティック検索を実装することで、エージェントの機能を拡張します。これにより、エージェントは完全一致でないクエリを理解して応答できるようになり、より複雑な質問でユーザーを支援する能力が向上します。

1. ブラウザのWeb Chatタブに以下の質問を貼り付けます：

   ```text
   What 18 amp circuit breakers do we sell?
   ```

   エージェントは以下のようなメッセージで応答します：

   _"当社の在庫に特定の18アンペアのサーキットブレーカーは見つかりませんでした。ただし、他のタイプのサーキットブレーカーが利用可能かもしれません。一般的なサーキットブレーカーまたは他の関連製品を検索しますか？😊"_

## エージェントアプリを停止する

VS Codeから、<kbd>Shift + F5</kbd>を押してエージェントアプリを停止します。

=== "Python"

    ## セマンティック検索を実装する

    このセクションでは、Model Context Protocol（MCP）を使用してセマンティック検索を実装し、エージェントの機能を強化します。

    1. <kbd>F1</kbd>を押してVS Code Command Paletteを**開きます**。
    2. **Open File**と入力し、**File: Open File...**を選択します。
    3. ファイルピッカーに以下のパスを**貼り付け**、<kbd>Enter</kbd>を押します：

        ```text
        /workspace/src/python/mcp_server/sales_analysis/sales_analysis.py
        ```

    4. 70行目あたりまでスクロールし、`semantic_search_products`メソッドを探します。このメソッドは売上データのセマンティック検索を実行する責任があります。**@mcp.tool()**デコレータがコメントアウトされていることがわかります。このデコレータはメソッドをMCPツールとして登録し、エージェントから呼び出せるようにするために使用されます。

    5. 行の先頭の`#`を削除して`@mcp.tool()`デコレータをアンコメントします。これによりセマンティック検索ツールが有効になります。

        ```python
        # @mcp.tool()
        async def semantic_search_products(
            ctx: Context,
            query_description: Annotated[str, Field(
            ...
        ```

    6. 次に、セマンティック検索ツールを使用するようにエージェントの指示を有効にする必要があります。`app.py`ファイルに戻ります。
    7. 30行目あたりまでスクロールし、`# INSTRUCTIONS_FILE = "instructions/mcp_server_tools_with_semantic_search.txt"`の行を見つけます。
    8. 行の先頭の`#`を削除してアンコメントします。これによりエージェントがセマンティック検索ツールを使用できるようになります。

        ```python
        INSTRUCTIONS_FILE = "instructions/mcp_server_tools_with_semantic_search.txt"
        ```

=== "C#"

    ## セマンティック検索を実装する

    このセクションでは、Model Context Protocol（MCP）を使用してセマンティック検索を実装し、エージェントの機能を強化します。

    1. `McpAgentWorkshop.WorkshopApi`プロジェクトから`McpHost.cs`ファイルを開きます。
    1. 他のMCPツールがMCPサーバーに登録されている場所を見つけ、`SemanticSearchTools`クラスをMCPツールとして登録します。

        ```csharp
        builder.Services.AddMcpTool<SemanticSearchTools>();
        ```

        !!! info "注意"
            MCPサーバーが検索をどのように実行するかを学ぶために、`SemanticSearchTools`の実装を読んでください。

    1. 次に、セマンティック検索ツールを使用するようにエージェントの指示を有効にする必要があります。`AgentService`クラスに戻り、const `InstructionsFile`を`mcp_server_tools_with_semantic_search.txt`に変更します。

## エージェント指示を確認する

1. <kbd>F1</kbd>を押してVS Code Command Paletteを開きます。
2. **Open File**と入力し、**File: Open File...**を選択します。
3. ファイルピッカーに以下のパスを貼り付け、<kbd>Enter</kbd>を押します：

   ```text
   /workspace/src/shared/instructions/mcp_server_tools_with_semantic_search.txt
   ```

4. ファイル内の指示を確認します。これらの指示は、売上データに関する質問に答えるためにセマンティック検索ツールを使用するようエージェントに指示します。

## セマンティック検索ツール付きでエージェントアプリを起動する

1. <kbd>F5</kbd>を押してエージェントアプリを**起動**します。これにより、更新された指示とセマンティック検索ツールを有効にしてエージェントが開始されます。
2. ブラウザで**Web Chat**を開きます。
3. チャットに以下の質問を入力します：

    ```text
    What 18 amp circuit breakers do we sell?
    ```

    エージェントは質問のセマンティックな意味を理解し、関連する売上データで適切に応答します。

    !!! info "注意"
        MCPセマンティック検索ツールは以下のように動作します：

        1. 質問は製品説明と同じOpenAI埋め込みモデル（text-embedding-3-small）を使用してベクトルに変換されます。
        2. このベクトルはPostgreSQLデータベース内の類似製品ベクトルを検索するために使用されます。
        3. エージェントは結果を受け取り、それらを使用して応答を生成します。

## エグゼクティブレポートを作成する

このワークショップの最終プロンプトは以下の通りです：

```plaintext
Write an executive report on the sales performance of different stores for these circuit breakers.
```

## エージェントアプリを実行したままにする

次のラボでセキュアなエージェントデータアクセスを探索するために、エージェントアプリを実行したままにしてください。
