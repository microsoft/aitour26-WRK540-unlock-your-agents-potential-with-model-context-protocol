## 学習内容

このラボでは、Model Context Protocol（MCP）とPostgreSQL Row Level Security（RLS）を使用してエージェントデータを保護します。エージェントには読み取り専用のデータベースアクセス権があり、データはユーザー権限（本社と店舗マネージャー）によって保護され、認可されたユーザーのみが特定の情報にアクセスできることを保証します。

## はじめに

PostgreSQLデータベースは、Row Level Security（RLS）を使用してユーザー権限別にデータアクセスを制御します。Webチャットクライアントはデフォルトで`本社`権限（全データアクセス）ですが、`店舗マネージャー`権限に切り替えると権限固有のデータのみへのアクセスに制限されます。

MCPサーバーは、エージェントにZavaデータベースへのアクセスを提供します。エージェントサービスがユーザーリクエストを処理する際、ユーザー権限（UUID）がMCPツールリソースヘッダーを介してMCPサーバーに渡され、権限ベースのセキュリティが確実に実施されます。

通常の動作では、店舗マネージャーはエージェントで認証し、そのユーザー権限が適切に設定されます。しかし、これはワークショップなので、手動で権限を選択します。

??? info "開発者向け：PostgreSQL Row Level Securityの仕組みは？"

    ### PostgreSQL RLSセキュリティ概要

    Row Level Security（RLS）は、ユーザー権限に基づいてデータベース行を自動的にフィルタリングします。これにより、複数のユーザーが同じデータベーステーブルを共有しながら、認可されたデータのみを見ることができます。
    
    このシステムでは、本社ユーザーはすべての店舗のすべてのデータを見ることができ、店舗マネージャーは自分の店舗の情報のみを表示するよう制限されます。以下の例は、`retail.orders`テーブルでRLSポリシーがどのように実装されているかを示しており、同一のポリシーが`retail.order_items`、`retail.inventory`、`retail.customers`テーブルにも適用されています。

    ```sql
    CREATE POLICY store_manager_orders ON retail.orders
    FOR ALL TO PUBLIC
    USING (
        -- 本社はすべてのデータを見る
        current_setting('app.current_rls_user_id', true) = '00000000-0000-0000-0000-000000000000'
        OR
        -- 店舗マネージャーは自分の店舗のデータのみを見る
        EXISTS (SELECT 1 FROM retail.stores s WHERE s.store_id = retail.orders.store_id 
                AND s.rls_user_id::text = current_setting('app.current_rls_user_id', true))
    );
    ```

    **結果：** 店舗マネージャーは自分の店舗のデータのみを見ることができ、本社はすべてを見ることができます - すべて同じデータベースとテーブルを使用します。



    === "Python"

        ユーザー権限の設定を担当するコードは、`workshop/chat_manager.py`ファイルにあります。

        ```python
        if request.rls_user_id:
            # RLSユーザーIDヘッダー付きの動的ツールリソースを作成
            mcp_tool_resource = MCPToolResource(
                server_label="ZavaSalesAnalysisMcpServer",
                headers={"x-rls-user-id": request.rls_user_id},
                require_approval="never",
            )
            tool_resources.mcp = [mcp_tool_resource]
        ```

        RLS User IDを取得するコードは`mcp_server/sales_analysis/sales_analysis.py`にあります。サーバーがRLSヘッダーを検出しない場合、本社権限にデフォルト設定されます。このフォールバックはワークショップ用のみで、本番環境では適用すべきではありません。

        ```python
        def get_rls_user_id(ctx: Context) -> str:
            """リクエストコンテキストからRow Level SecurityユーザーIDを取得。"""

            rls_user_id = get_header(ctx, "x-rls-user-id")
            if rls_user_id is None:
                # 提供されていない場合はプレースホルダーにデフォルト設定
                rls_user_id = "00000000-0000-0000-0000-000000000000"
            return rls_user_id
        ```

    === "C#"

        MCPサーバーへのリクエストでユーザー権限を設定する責任を持つコードは、`AgentService`クラスにあります。

        ```csharp
        var mcpToolResource = new MCPToolResource(ZavaMcpToolLabel, new Dictionary<string, string>
        {
            { "x-rls-user-id", request.RlsUserId }
        });
        var toolResources = new ToolResources();
        toolResources.Mcp.Add(mcpToolResource);
        ```

        `MCPToolResource`は`ToolResources`コレクションに追加され、`CreateRunStreamingOptions.ToolResources`プロパティを使用してストリーミング実行に提供されます。これは、RLSユーザーIDがクライアントからの動的な値（異なる「ログイン」ユーザーは異なるIDを持つ可能性）であるため、エージェント作成時ではなくスレッド_実行_時に設定する必要があることを保証します。

        RLSユーザーIDは、エージェントがMCPサーバーに転送するヘッダーとして設定されるため、リクエストの`HttpContext`からアクセスされ、MCPツールメソッドに注入される`IHttpContextAccessor`からアクセスできます。拡張メソッド`HttpContextAccessorExtensions.GetRequestUserId`が作成され、ツール内で使用できます：

        ```csharp
        public async Task<string> ExecuteSalesQueryAsync(
            NpgsqlConnection connection,
            ILogger<SalesTools> logger,
            IHttpContextAccessor httpContextAccessor,
            [Description("正しい形式のPostgreSQLクエリ。")] string query
        )
        {
            ...

            var rlsUserId = httpContextAccessor.GetRequestUserId();

            ...
        }
        ```

    ### Postgres RLS User IDを設定する

    MCPサーバーがRLS User IDを取得したら、PostgreSQL接続で設定する必要があります。

    === "Python"

        Pythonソリューションは、`mcp_server/sales_analysis/sales_analysis_postgres.py`の`execute_query`メソッド内で`set_config()`を呼び出すことで、各PostgreSQL接続でRLS User IDを設定します。

        ```python
        ...
        conn = await self.get_connection()
        await conn.execute("SELECT set_config('app.current_rls_user_id', $1, false)", rls_user_id)

        rows = await conn.fetch(sql_query)
        ...
        ```

    === "C#"

        C#ソリューションは、`SalesTools.cs`の`ExecuteSalesQueryAsync`メソッドで接続を開いた直後にRLSコンテキスト変数を設定するSQLコマンドを実行することで、PostgreSQL接続でRLS User IDを設定します。

        ```csharp
        ...
        await using var cmd = new NpgsqlCommand("SELECT set_config('app.current_rls_user_id', @rlsUserId, false)", connection);
        cmd.Parameters.AddWithValue("rlsUserId", rlsUserId ?? string.Empty);
        await cmd.ExecuteNonQueryAsync();

        await using var queryCmd = new NpgsqlCommand(query, connection);
        await using var reader = await queryCmd.ExecuteReaderAsync();
        ...
        ```



## ラボ演習

### 本社権限

デフォルトでは、Webクライアントはすべてのデータにフルアクセスできる`本社`権限で動作します。

1. チャットに以下のクエリを入力します：

   ```text
   Show sales by store
   ```

   すべての店舗のデータが返されることがわかります。完璧です。

### 店舗マネージャー権限を選択する

1. ブラウザのAgents Web Chatタブに戻ります。
2. ページ右上の`設定`アイコンを選択します。
3. ドロップダウンメニューから`Store location`を選択します。
4. `Save`を選択すると、エージェントは選択した店舗ロケーションのデータアクセス権限で動作します。

   ![](../media/select_store_manager_role.png)

これでエージェントは選択した店舗ロケーションのデータのみにアクセスできるようになります。

!!! info "注意"
    ユーザーを変更するとチャットセッションがリセットされます。コンテキストがユーザーに紐づいているためです。

以下のクエリを試してください：

```text
Show sales by store
```

エージェントが選択した店舗ロケーションのデータのみを返すことがわかります。これは、選択した店舗マネージャー権限に基づいてエージェントのデータアクセスが制限されていることを示しています。

![](../media/select_seattle_store_role.png)
