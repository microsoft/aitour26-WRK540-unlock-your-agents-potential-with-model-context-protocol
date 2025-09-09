# 实验 2：启动您的代理

## 您将学到什么

在本实验中，您将启用代码解释器来分析销售数据并使用自然语言创建图表。

## 简介

在本实验中，您将使用两个工具扩展 Azure AI 代理：

- **代码解释器**：让代理生成并运行 Python 代码进行数据分析和可视化。
- **MCP 服务器工具**：允许代理使用 MCP 工具访问外部数据源，在我们的案例中是 PostgreSQL 数据库中的数据。

## 实验练习

### 启用代码解释器和 MCP 服务器

在本实验中，您将启用两个协同工作的强大工具：代码解释器（执行 AI 生成的 Python 代码进行数据分析和可视化）和 MCP 服务器（提供对存储在 PostgreSQL 中的 Zava 销售数据的安全访问）。

=== "Python"

    1. **打开** `app.py`。
    2. **向下滚动到大约第 50 行**，找到将代码解释器和 MCP 工具添加到代理工具集的行。这些行当前在开头用 `#` 注释掉了。
    3. **取消注释**以下行：

        ```python
        
        # code_interpreter = CodeInterpreterTool()
        # self.toolset.add(code_interpreter)
        
        # mcp_tools = McpTool(
        #     server_label="ZavaSalesAnalysisMcpServer",
        #     server_url=Config.DEV_TUNNEL_URL,
        #     allowed_tools=[
        #         "get_multiple_table_schemas",
        #         "execute_sales_query",
        #         "get_current_utc_date",
        #         "semantic_search_products",
        #     ],
        # )

        # mcp_tools.set_approval_mode("never")  # No human in the loop
        # self.toolset.add(mcp_tools)
        ```

        !!! info "这段代码做什么？"
            - **代码解释器**：使代理能够执行 Python 代码进行数据分析和可视化。
            - **MCP 服务器工具**：提供对外部数据源的访问，具有特定的允许工具且无需人工批准。对于生产应用程序，考虑为敏感操作启用人工参与授权。

    4. **查看**您取消注释的代码。代码应该完全像这样：

        取消注释后，您的代码应如下所示：

        ```python
        class AgentManager:
            """管理 Azure AI 代理生命周期和依赖项。"""

            async def _setup_agent_tools(self) -> None:
                """设置 MCP 工具和代码解释器。"""
                logger.info("设置代理工具...")
                self.toolset = AsyncToolSet()

                code_interpreter = CodeInterpreterTool()
                self.toolset.add(code_interpreter)

                mcp_tools = McpTool(
                    server_label="ZavaSalesAnalysisMcpServer",
                    server_url=Config.DEV_TUNNEL_URL,
                    allowed_tools=[
                        "get_multiple_table_schemas",
                        "execute_sales_query",
                        "get_current_utc_date",
                        "semantic_search_products",
                    ],
                )

                mcp_tools.set_approval_mode("never")  # 无人工参与
                self.toolset.add(mcp_tools)
        ```

    ## 启动代理应用

    1. 将以下文本复制到剪贴板：

    ```text
    Debug: Select and Start Debugging
    ```

    2. 按 <kbd>F1</kbd> 打开 VS Code 命令面板。
    3. 将文本粘贴到命令面板中并选择**Debug: Select and Start Debugging**。
    4. 从列表中选择**🌎🤖Debug Compound: Agent and MCP (http)**。这将启动代理应用和 Web 聊天客户端。

    这将启动以下进程：

    1. DevTunnel (workshop) 任务
    2. Web Chat (workshop)
    3. Agent Manager (workshop)
    4. MCP Server (workshop)

    在 VS Code 中，您将在终端面板中看到这些正在运行。

    ![图像显示了 VS Code 终端面板中正在运行的进程](../media/vs-code-processes.png)

    ## 打开代理 Web 聊天客户端

    === "@活动参与者"

        选择以下链接在浏览器中打开 Web Chat 应用。

        [打开 Web Chat](http://localhost:8005){:target="_blank"}

    === "自主学习者"

        ## 使端口 8005 公开

        您需要使端口 8005 公开才能在浏览器中访问 Web 聊天客户端。

        1. 在 VS Code 底部面板中选择**端口**选项卡。
        2. 右键单击**Web Chat App (8005)**端口并选择**端口可见性**。
        3. 选择**公开**。

        ![](../media/make-port-public.png)


        ## 在浏览器中打开 Web Chat 客户端

        1. 将以下文本复制到剪贴板：

        ```text
        Open Port in Browser
        ```

        2. 按 <kbd>F1</kbd> 打开 VS Code 命令面板。
        3. 将文本粘贴到命令面板中并选择**Open Port in Browser**。
        4. 从列表中选择**8005**。这将在浏览器中打开代理 Web 聊天客户端。

    ![](../media/agent_web_chat.png)

=== "C#"

    1. 从 `McpAgentWorkshop.WorkshopApi` 项目的 `Services` 文件夹中**打开** `AgentService.cs`。
    2. 导航到 `InitialiseAgentAsync` 方法。
    3. **取消注释**以下行：

        ```csharp
        // var mcpTool = new MCPToolDefinition(
        //     ZavaMcpToolLabel,
        //     devtunnelUrl + "mcp");

        // var codeInterpreterTool = new CodeInterpreterToolDefinition();

        // IEnumerable<ToolDefinition> tools = [mcpTool, codeInterpreterTool];

        // persistentAgent = await persistentAgentsClient.Administration.CreateAgentAsync(
        //         name: AgentName,
        //         model: configuration.GetValue<string>("MODEL_DEPLOYMENT_NAME"),
        //         instructions: instructionsContent,
        //         temperature: modelTemperature,
        //         tools: tools);

        // logger.LogInformation("Agent created with ID: {AgentId}", persistentAgent.Id);
        ```

    ## 启动代理应用

    4. 按 <kbd>F1</kbd> 打开 VS Code 命令面板。
    5. 选择**Debug Aspire**作为启动配置。

    一旦调试器启动，浏览器窗口将打开 Aspire 仪表板。一旦所有资源都启动，您可以通过单击链接**Workshop Frontend**来启动工作坊 Web 应用程序。

    ![Aspire 仪表板](../media//lab-2-start-agent-aspire-dashboard.png)

    !!! tip "故障排除"
        如果浏览器无法加载，请尝试硬刷新页面（Ctrl + F5 或 Cmd + Shift + R）。如果仍然无法加载，请参考[故障排除指南](./dotnet-troubleshooting.md)。

## 开始与代理对话

从 Web 聊天客户端，您可以开始与代理对话。代理设计用于回答有关 Zava 销售数据的问题并使用代码解释器生成可视化。

1. 产品销售分析。复制并粘贴以下问题到聊天中：

    ```text
    Show the top 10 products by revenue by store for the last quarter
    ```

    片刻后，代理将用显示每个门店上个季度前 10 个产品收入的表格进行回应。

    !!! info
        代理使用 LLM 调用三个 MCP 服务器工具来获取数据并在表格中显示：

        1. **get_current_utc_date()**：获取当前日期和时间，以便代理可以确定相对于当前日期的上个季度。
        2. **get_multiple_table_schemas()**：获取数据库中 LLM 生成有效 SQL 所需的表架构。
        3. **execute_sales_query**：执行 SQL 查询，从 PostgreSQL 数据库获取上个季度前 10 个产品的收入。

    !!! tip
        === "Python"

            切换回 VS Code 并从终端面板中选择**MCP Server (workspace)**，您将看到 Azure AI Foundry 代理服务对 MCP 服务器的调用。

            ![](../media/mcp-server-in-action.png)

        === "C#"

            在 Aspire 仪表板中，您可以选择 `dotnet-mcp-server` 资源的日志来查看 Azure AI Foundry 代理服务对 MCP 服务器的调用。

            您还可以打开跟踪视图并找到应用程序的端到端跟踪，从 Web 聊天中的用户输入到代理调用和 MCP 工具调用。

            ![跟踪概述](../media/lab-7-trace-overview.png)

2. 生成饼图。复制并粘贴以下问题到聊天中：

    ```text
    Show sales by store as a pie chart for this financial year
    ```

    代理将用显示当前财政年度按门店销售分布的饼图进行回应。

    !!! info
        这可能感觉像魔术，那么背后发生了什么让这一切工作？

        Foundry 代理服务编排以下步骤：

        1. 像上一个问题一样，代理确定是否具有查询所需的表架构。如果没有，它使用**get_multiple_table_schemas()**工具获取当前日期和数据库架构。
        2. 代理然后使用**execute_sales_query**工具获取销售数据
        3. 使用返回的数据，LLM 编写 Python 代码创建饼图。
        4. 最后，代码解释器执行 Python 代码生成图表。

3. 继续询问有关 Zava 销售数据的问题，看看代码解释器的实际操作。以下是您可能想尝试的一些后续问题：

    - `Determine which products or categories drive sales. Show as a Bar Chart.`
    - `What would be the impact of a shock event (e.g., 20% sales drop in one region) on global sales distribution? Show as a Grouped Bar Chart.`
      - 跟进 `What if the shock event was 50%?`
    - `Which regions have sales above or below the average? Show as a Bar Chart with Deviation from Average.`
    - `Which regions have discounts above or below the average? Show as a Bar Chart with Deviation from Average.`
    - `Simulate future sales by region using a Monte Carlo simulation to estimate confidence intervals. Show as a Line with Confidence Bands using vivid colors.`

<!-- ## 停止代理应用

1. 切换回 VS Code 编辑器。
1. 按 <kbd>Shift + F5</kbd> 停止代理应用。 -->

## 保持代理应用运行

让代理应用保持运行，因为您将在下一个实验中使用它来扩展代理的更多工具和功能。

*使用 GitHub Copilot 翻译。*
