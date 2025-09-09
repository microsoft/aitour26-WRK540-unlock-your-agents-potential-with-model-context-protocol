# 实验 4：保护代理数据

## 您将学到什么

在本实验中，您将使用模型上下文协议 (MCP) 和 PostgreSQL 行级安全性 (RLS) 来保护代理数据。代理具有只读数据库访问权限，数据通过用户角色（总部和门店经理）保护，确保只有授权用户才能访问特定信息。

## 简介

PostgreSQL 数据库使用行级安全性 (RLS) 根据用户角色控制数据访问。Web 聊天客户端默认为 `Head office` 角色（完全数据访问），但切换到 `Store Manager` 角色会将访问限制为仅特定角色的数据。

MCP 服务器为代理提供对 Zava 数据库的访问。当代理服务处理用户请求时，用户角色 (UUID) 通过 MCP 工具资源标头传递给 MCP 服务器，以确保执行基于角色的安全性。

在正常操作中，门店经理会与代理进行身份验证，并相应地设置他们的用户角色。但这是一个工作坊，我们将手动选择一个角色。

??? info "面向开发人员：PostgreSQL 行级安全性如何工作？"

    ### PostgreSQL RLS 安全概述

    行级安全性 (RLS) 根据用户权限自动过滤数据库行。这允许多个用户共享相同的数据库表，同时只看到他们有权访问的数据。
    
    在此系统中，总部用户可以看到所有门店的所有数据，而门店经理仅限于查看自己门店的信息。下面的示例展示了如何为 `retail.orders` 表实施 RLS 策略，对 `retail.order_items`、`retail.inventory` 和 `retail.customers` 表应用相同的策略。

    ```sql
    CREATE POLICY store_manager_orders ON retail.orders
    FOR ALL TO PUBLIC
    USING (
        -- 总部可以看到所有数据
        current_setting('app.current_rls_user_id', true) = '00000000-0000-0000-0000-000000000000'
        OR
        -- 门店经理只能看到自己门店的数据
        EXISTS (SELECT 1 FROM retail.stores s WHERE s.store_id = retail.orders.store_id 
                AND s.rls_user_id::text = current_setting('app.current_rls_user_id', true))
    );
    ```

    **结果**：门店经理只看到自己门店的数据，而总部看到所有内容 - 全部使用相同的数据库和表。



    === "Python"

        您可以在 `workshop/chat_manager.py` 文件中找到负责设置用户角色的代码。

        ```python
        if request.rls_user_id:
            # 使用 RLS 用户 ID 标头创建动态工具资源
            mcp_tool_resource = MCPToolResource(
                server_label="ZavaSalesAnalysisMcpServer",
                headers={"x-rls-user-id": request.rls_user_id},
                require_approval="never",
            )
            tool_resources.mcp = [mcp_tool_resource]
        ```

        检索 RLS 用户 ID 的代码在 `mcp_server/sales_analysis/sales_analysis.py` 中。如果服务器未检测到 RLS 标头，它默认为总部角色。此回退仅适用于工作坊使用，不应在生产中应用。

        ```python
        def get_rls_user_id(ctx: Context) -> str:
            """从请求上下文获取行级安全用户 ID。"""

            rls_user_id = get_header(ctx, "x-rls-user-id")
            if rls_user_id is None:
                # 如果未提供则默认为占位符
                rls_user_id = "00000000-0000-0000-0000-000000000000"
            return rls_user_id
        ```

    === "C#"

        您可以在 `AgentService` 类中找到负责在向 MCP 服务器的请求上设置用户角色的代码。

        ```csharp
        var mcpToolResource = new MCPToolResource(ZavaMcpToolLabel, new Dictionary<string, string>
        {
            { "x-rls-user-id", request.RlsUserId }
        });
        var toolResources = new ToolResources();
        toolResources.Mcp.Add(mcpToolResource);
        ```

        然后将 `MCPToolResource` 添加到 `ToolResources` 集合中，该集合使用 `CreateRunStreamingOptions.ToolResources` 属性提供给流式运行，这是因为 RLS 用户 ID 是来自客户端的动态值（不同的"登录"用户可能具有不同的 ID），我们需要确保它在线程_运行_上设置，而不是在创建代理时设置。

        由于 RLS 用户 ID 设置为代理转发到 MCP 服务器的标头，这可以从请求的 `HttpContext` 访问，可以从注入到 MCP 工具方法中的 `IHttpContextAccessor` 访问。已创建扩展方法 `HttpContextAccessorExtensions.GetRequestUserId`，可在工具内使用：

        ```csharp
        public async Task<string> ExecuteSalesQueryAsync(
            NpgsqlConnection connection,
            ILogger<SalesTools> logger,
            IHttpContextAccessor httpContextAccessor,
            [Description("A well-formed PostgreSQL query.")] string query
        )
        {
            ...

            var rlsUserId = httpContextAccessor.GetRequestUserId();

            ...
        }
        ```

    ### 设置 Postgres RLS 用户 ID

    现在 MCP 服务器有了 RLS 用户 ID，需要在 PostgreSQL 连接上设置它。

    === "Python"

        Python 解决方案通过在 `mcp_server/sales_analysis/sales_analysis_postgres.py` 中的 `execute_query` 方法内调用 `set_config()` 在每个 PostgreSQL 连接上设置 RLS 用户 ID。

        ```python
        ...
        conn = await self.get_connection()
        await conn.execute("SELECT set_config('app.current_rls_user_id', $1, false)", rls_user_id)

        rows = await conn.fetch(sql_query)
        ...
        ```

    === "C#"

        C# 解决方案通过在 `SalesTools.cs` 中的 `ExecuteSalesQueryAsync` 方法中打开连接后立即执行 SQL 命令来设置 RLS 上下文变量，在 PostgreSQL 连接上设置 RLS 用户 ID。

        ```csharp
        ...
        await using var cmd = new NpgsqlCommand("SELECT set_config('app.current_rls_user_id', @rlsUserId, false)", connection);
        cmd.Parameters.AddWithValue("rlsUserId", rlsUserId ?? string.Empty);
        await cmd.ExecuteNonQueryAsync();

        await using var queryCmd = new NpgsqlCommand(query, connection);
        await using var reader = await queryCmd.ExecuteReaderAsync();
        ...
        ```



## 实验练习

### 总部角色

默认情况下，Web 客户端以 `Head Office` 角色运行，该角色对所有数据具有完全访问权限。

1. 在聊天中输入以下查询：

   ```text
   Show sales by store
   ```

   您将看到返回所有门店的数据。完美。

### 选择门店经理角色

1. 切换回浏览器中的代理 Web Chat 选项卡。
2. 选择页面右上角的 `settings` 图标。
3. 从下拉菜单中选择一个 `Store location`。
4. 选择 `Save`，现在代理将使用选定门店位置的数据访问权限进行操作。

   ![](../media/select_store_manager_role.png)

现在代理将只能访问选定门店位置的数据。

!!! info "注意"
    更改用户将重置聊天会话，因为上下文与用户绑定。

尝试以下查询：

```text
Show sales by store
```

您会注意到代理只返回选定门店位置的数据。这演示了代理的数据访问如何根据选定的门店经理角色进行限制。

![](../media/select_seattle_store_role.png)

*使用 GitHub Copilot 翻译。*
