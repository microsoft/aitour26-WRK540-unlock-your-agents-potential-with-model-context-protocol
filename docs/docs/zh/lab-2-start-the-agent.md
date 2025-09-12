## 学习内容

在本实验中，您将启用代码解释器来分析销售数据并使用自然语言创建图表。

## 介绍

在本实验中，您将使用两个工具扩展Azure AI代理：

- **代码解释器：** 允许代理生成并运行Python代码进行数据分析和可视化。
- **MCP服务器工具：** 允许代理使用MCP工具访问外部数据源，在我们的案例中是PostgreSQL数据库中的数据。

## 实验练习

### 启用代码解释器和MCP服务器

在本实验中，您将启用两个协同工作的强大工具：代码解释器（执行AI生成的Python代码进行数据分析和可视化）和MCP服务器（提供对存储在PostgreSQL中的Zava销售数据的安全访问）。

=== "Python"

    1. **打开** `app.py` 文件。
    2. **滚动到第67行** 并找到将代码解释器工具和MCP服务器工具添加到代理工具集的行。这些行目前在开头用 **# 加空格** 字符注释掉了。
    3. **取消注释** 以下行：

        !!! warning "Python中缩进很重要！"
            取消注释时，删除 `#` 符号和跟随的空格。这确保代码保持正确的Python缩进并与周围的代码正确对齐。

        ```python
        # self.toolset.add(code_interpreter_tool)
        # self.toolset.add(mcp_server_tools)
        ```

        !!! info "这段代码是做什么的？"
            - **代码解释器工具**：使代理能够执行Python代码进行数据分析和可视化。
            - **MCP服务器工具**：提供对外部数据源的访问，具有特定的允许工具且无需人工批准。对于生产应用程序，考虑为敏感操作启用人工在环授权。

    4. **检查** 您取消注释的代码。代码应该完全像这样：

        取消注释后，您的代码应该看起来像这样：

        ```python
        async def _setup_agent_tools(self) -> None:
            """Setup MCP tools and code interpreter."""
            logger.info("Setting up Agent tools...")
            self.toolset = AsyncToolSet()

            code_interpreter_tool = CodeInterpreterTool()

            mcp_server_tools = McpTool(
                server_label="ZavaSalesAnalysisMcpServer",
                server_url=Config.DEV_TUNNEL_URL,
                allowed_tools=[
                    "get_multiple_table_schemas",
                    "execute_sales_query",
                    "get_current_utc_date",
                    "semantic_search_products",
                ],
            )
            mcp_server_tools.set_approval_mode("never")  # No human in the loop

            self.toolset.add(code_interpreter_tool)
            self.toolset.add(mcp_server_tools)
        ```

    ## 启动代理应用

    1. 将下面的文本复制到剪贴板：

    ```text
    Debug: Select and Start Debugging
    ```

    1. 按 <kbd>F1</kbd> 打开VS Code命令面板。
    1. 将文本粘贴到命令面板中并选择 **Debug: Select and Start Debugging**。
    1. 从列表中选择 **🌎🤖Debug Compound: Agent and MCP (http)**。这将启动代理应用和Web聊天客户端。

    这启动以下进程：

    1.  DevTunnel (workshop) Task
    2.  Web Chat (workshop)
    3.  Agent Manager (workshop)
    4.  MCP Server (workshop)

    在VS Code中，您将看到这些在TERMINAL面板中运行。

    ![图像显示VS Code TERMINAL面板中运行的进程](../media/vs-code-processes.png)

    ## 打开代理Web聊天客户端

    === "@活动参与者"

        选择以下链接在浏览器中打开Web聊天应用。

        [打开Web聊天](http://localhost:8005){:target="_blank"}

    === "自学学习者"

        ## 使端口8005公开

        您需要使端口8005公开以便在浏览器中访问Web聊天客户端。

        1. 在VS Code底部面板中选择 **Ports** 标签。
        2. 右键单击 **Web Chat App (8005)** 端口并选择 **Port Visibility**。
        3. 选择 **Public**。

        ![](../media/make-port-public.png)


        ## 在浏览器中打开Web聊天客户端

        1.  将下面的文本复制到剪贴板：

        ```text
        Open Port in Browser
        ```

        2.  按 <kbd>F1</kbd> 打开VS Code命令面板。
        3.  将文本粘贴到命令面板中并选择 **Open Port in Browser**。
        4.  从列表中选择 **8005**。这将在您的浏览器中打开代理Web聊天客户端。

    ![](../media/agent_web_chat.png)

=== "C#"

    1. **打开** 来自 `McpAgentWorkshop.WorkshopApi` 项目的 `Services` 文件夹中的 `AgentService.cs`。
    2. 导航到 `InitialiseAgentAsync` 方法。
    3. **取消注释** 以下行：

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

    4. 按 <kbd>F1</kbd> 打开VS Code命令面板。
    5. 选择 **Debug Aspire** 作为启动配置。

    调试器启动后，将打开一个带有Aspire仪表板的浏览器窗口。所有资源启动后，您可以通过单击 **Workshop Frontend** 链接来启动研讨会Web应用程序。

    ![Aspire仪表板](../media//lab-2-start-agent-aspire-dashboard.png)

    !!! tip "故障排除"
        如果浏览器未加载，请尝试强制刷新页面（Ctrl + F5或Cmd + Shift + R）。如果仍未加载，请参考[故障排除指南](./dotnet-troubleshooting.md)。

## 开始与代理对话

从Web聊天客户端，您可以开始与代理对话。代理设计用于回答有关Zava销售数据的问题并使用代码解释器生成可视化。

1.  产品销售分析。将以下问题复制并粘贴到聊天中：

    ```text
    Show the top 10 products by revenue by store for the last quarter
    ```

    片刻后，代理将用显示每个商店按收入排名前10的产品的表格进行响应。

    !!! info
        代理使用LLM调用三个MCP服务器工具来获取数据并在表格中显示：

        1. **get_current_utc_date()**：获取当前日期和时间，以便代理可以确定相对于当前日期的上一季度。
        2. **get_multiple_table_schemas()**：获取数据库中LLM生成有效SQL所需的表架构。
        3. **execute_sales_query**：执行SQL查询以从PostgreSQL数据库获取上一季度按收入排名前10的产品。

    !!! tip
        === "Python"

            切换回VS Code并从TERMINAL面板选择 **MCP Server (workspace)**，您将看到Azure AI Foundry代理服务对MCP服务器进行的调用。

            ![](../media/mcp-server-in-action.png)

        === "C#"

            在Aspire仪表板中，您可以选择 `dotnet-mcp-server` 资源的日志来查看Azure AI Foundry代理服务对MCP服务器进行的调用。

            您还可以打开跟踪视图并找到应用程序的端到端跟踪，从Web聊天中的用户输入到代理调用和MCP工具调用。

            ![跟踪概览](../media/lab-7-trace-overview.png)

2.  生成饼图。将以下问题复制并粘贴到聊天中：

    ```text
    Show sales by store as a pie chart for this financial year
    ```

    代理将用显示当前财政年度按商店销售分布的饼图进行响应。

    !!! info
        这可能感觉像魔法，那么幕后发生了什么来使这一切工作？

        Foundry代理服务协调以下步骤：

        1. 像上一个问题一样，代理确定是否具有查询所需的表架构。如果没有，它使用 **get_multiple_table_schemas()** 工具获取当前日期和数据库架构。
        2. 然后代理使用 **execute_sales_query** 工具获取销售数据
        3. 使用返回的数据，LLM编写Python代码来创建饼图。
        4. 最后，代码解释器执行Python代码以生成图表。

3.  继续询问有关Zava销售数据的问题，以查看代码解释器的实际操作。以下是您可能想尝试的一些后续问题：

    - `Determine which products or categories drive sales. Show as a Bar Chart.`
    - `What would be the impact of a shock event (e.g., 20% sales drop in one region) on global sales distribution? Show as a Grouped Bar Chart.`
      - 跟进 `What if the shock event was 50%?`
    - `Which regions have sales above or below the average? Show as a Bar Chart with Deviation from Average.`
    - `Which regions have discounts above or below the average? Show as a Bar Chart with Deviation from Average.`
    - `Simulate future sales by region using a Monte Carlo simulation to estimate confidence intervals. Show as a Line with Confidence Bands using vivid colors.`

<!-- ## Stop the Agent App

1. Switch back to the VS Code editor.
1. Press <kbd>Shift + F5</kbd> to stop the agent app. -->

## 让代理应用保持运行

让代理应用保持运行，因为您将在下一个实验中使用它来扩展代理更多工具和功能。

*使用GitHub Copilot翻译。*
