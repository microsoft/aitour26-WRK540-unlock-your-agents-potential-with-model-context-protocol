## What You'll Learn

In this lab, you'll enable the Code Interpreter to analyze sales data and create charts using natural language.

## Introduction

In this lab, you will extend the Azure AI Agent with two tools:

- **Code Interpreter:** Lets the agent generate and run Python code for data analysis and visualization.
- **MCP Server tools:** Allow the agent to access external data sources using MCP Tools, in our case data in a PostgreSQL database.

## Lab Exercise

### Enable the Code Interpreter and MCP Server

In this lab, you'll enable two powerful tools that work together: the Code Interpreter (which executes AI-generated Python code for data analysis and visualization) and the MCP Server (which provides secure access to Zava's sales data stored in PostgreSQL).

=== "Python"

    1. **Open** the `app.py`.
    2. **Scroll down to line 67** and find the lines that add the Code Interpreter tool and the MCP Server tools to the agent's toolset. These line are currently commented out with **# plus space** characters at the beginning.
    3. **Uncomment** the following lines:

        !!! warning "Indentation matters in Python!"
            When uncommenting, delete both the `#` symbol AND the space that follows it. This ensures the code maintains proper Python indentation and aligns correctly with the surrounding code.

        ```python
        # self.toolset.add(code_interpreter_tool)
        # self.toolset.add(mcp_server_tools)
        ```

        !!! info "What does this code do?"
            - **Code Interpreter tool**: Enables the agent to execute Python code for data analysis and visualization.
            - **MCP Server tools**: Provides access to external data sources with specific allowed tools and no human approval required. For production applications, consider enabling human-in-the-loop authorization for sensitive operations.

    4. **Review** the code you uncommented. The code should look exactly like this:

        After uncommenting, your code should look like this:

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

    ## Start the Agent App

    1. Copy the text below to the clipboard:

    ```text
    Debug: Select and Start Debugging
    ```

    1. Press <kbd>F1</kbd> to open the VS Code Command Palette.
    1. Paste the text into the Command Palette and select **Debug: Select and Start Debugging**.
    1. Select **🌎🤖Debug Compound: Agent and MCP (http)** from the list. This will start the agent app and the web chat client.

    This starts the following processes:

    1.  DevTunnel (workshop) Task
    2.  Web Chat (workshop)
    3.  Agent Manager (workshop)
    4.  MCP Server (workshop)

    In VS Code you'll see these running in the TERMINAL panel.

    ![The image shows the running processes in the VS Code TERMINAL panel](../media/vs-code-processes.png)

    ## Open the Agent Web Chat Client

    === "@Event Attendees"

        Select the following link to open the Web Chat app in the browser.

        [Open Web Chat](http://localhost:8005){:target="_blank"}

    === "Self-Guided Learners"

        ## Make Port 8005 Public

        You need to make port 8005 public in order to access the web chat client in your browser.

        1. Select the **Ports** tab in the bottom panel of VS Code.
        2. Right-click on the **Web Chat App (8005)** port and select **Port Visibility**.
        3. Select **Public**.

        ![](../media/make-port-public.png)


        ## Open the Web Chat Client in the Browser

        1.  Copy the text below to the clipboard:

        ```text
        Open Port in Browser
        ```

        2.  Press <kbd>F1</kbd> to open the VS Code Command Palette.
        3.  Paste the text into the Command Palette and select **Open Port in Browser**.
        4.  Select **8005** from the list. This will open the agent web chat client in your browser.

    ![](../media/agent_web_chat.png)

=== "C#"

    1. **Open** `AgentService.cs` from the `McpAgentWorkshop.WorkshopApi` project's `Services` folder.
    2. Navigate to the `InitialiseAgentAsync` method.
    3. **Uncomment** the following lines:

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

    ## Start the Agent App

    4. Press <kbd>F1</kbd> to open the VS Code Command Palette.
    5. Select **Debug Aspire** as the launch configuration.

    Once the debugger has launched, a browser window will open with the Aspire dashboard. Once all resources have started, you can launch the workshop web application by clicking the link **Workshop Frontend**.

    ![Aspire dashboard](../media//lab-2-start-agent-aspire-dashboard.png)

    !!! tip "Troubleshooting"
        If the browser does not load, try hard-refreshing the page (Ctrl + F5 or Cmd + Shift + R). If it still does not load, refer to the [troubleshooting guide](./dotnet-troubleshooting.md).

## Start a Conversation with the Agent

From the web chat client, you can start a conversation with the agent. The agent is designed to answer questions about Zava's sales data and generate visualizations using the Code Interpreter.

1.  Product sales analysis. Copy and paste the following question into the chat:

    ```text
    Show the top 10 products by revenue by store for the last quarter
    ```

    After a moment, the agent will respond with a table showing the top 10 products by revenue for each store.

    !!! info
        The agent uses the LLM calls three MCP Server tools to fetch the data and display it in a table:

        1. **get_current_utc_date()**: Gets the current date and time so the agent can determine the last quarter relative to the current date.
        2. **get_multiple_table_schemas()**: Gets the schemas of the tables in the database required to by the LLM to generate valid SQL.
        3. **execute_sales_query**: Executes a SQL query to fetch the top 10 products by revenue for the last quarter from the PostgreSQL database.

    !!! tip
        === "Python"

            Switch back to VS Code and select **MCP Server (workspace)** from the TERMINAL panel and you'll see the calls made to the MCP Server by the Azure AI Foundry Agent Service.

            ![](../media/mcp-server-in-action.png)

        === "C#"

            In the Aspire dashboard, you can select the logs for the `dotnet-mcp-server` resource to see the calls made to the MCP Server by the Azure AI Foundry Agent Service.

            You can also open the trace view and find the end-to-end trace of the application, from the user input in the web chat, through to the agent calls and MCP tool calls.

            ![Trace overview](../media/lab-7-trace-overview.png)

2.  Generate a pie chart. Copy and paste the following question into the chat:

    ```text
    Show sales by store as a pie chart for this financial year
    ```

    The agent will respond with a pie chart showing the sales distribution by store for the current financial year.

    !!! info
        This might feel like magic, so what’s happening behind the scenes to make it all work?

        Foundry Agent Service orchestrates the following steps:

        1. Like the previous question, the agent determines if it has the table schemas required for the query. If not, it uses **get_multiple_table_schemas()** tools to get the current date and the database schema.
        2. The agent then uses the **execute_sales_query** tool to fetch the sales
        3. Using the returned data, the LLM writes Python code to create a Pie Chart.
        4. Finally, the Code Interpreter executes the Python code to generate the chart.

3.  Continue asking questions about Zava sales data to see the Code Interpreter in action. Here are a few follow-up questions you might like to try:

    - `Determine which products or categories drive sales. Show as a Bar Chart.`
    - `What would be the impact of a shock event (e.g., 20% sales drop in one region) on global sales distribution? Show as a Grouped Bar Chart.`
      - Follow up with `What if the shock event was 50%?`
    - `Which regions have sales above or below the average? Show as a Bar Chart with Deviation from Average.`
    - `Which regions have discounts above or below the average? Show as a Bar Chart with Deviation from Average.`
    - `Simulate future sales by region using a Monte Carlo simulation to estimate confidence intervals. Show as a Line with Confidence Bands using vivid colors.`

<!-- ## Stop the Agent App

1. Switch back to the VS Code editor.
1. Press <kbd>Shift + F5</kbd> to stop the agent app. -->

## Leave the Agent App Running

Leave the agent app running as you will use it in the next lab to extend the agent with more tools and capabilities.
