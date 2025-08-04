## What You'll Learn

In this lab, you will:

- Use DevTunnel to make your local MCP server accessible to cloud-based agent services
- Set up your environment for hands-on experimentation with the Model Context Protocol

## Introduction

The Model Context Protocol (MCP) server is a crucial component that handles the communication between Large Language Models (LLMs) and external tools and data sources. You’ll run the MCP server on your local machine, but the Azure AI Foundry Agent Service requires internet access to connect to it. To make your local MCP server accessible from the internet, you’ll use a DevTunnel. This allows the Agent Service to communicate with your MCP server as if it were running as a service in Azure.

## Interface options for MCP

MCP supports two main interfaces for connecting LLMs with tools:

- **Streamable HTTP Transport**: For web-based APIs and services.
- **Stdio Transport**: For local scripts and command-line tools.

This lab uses the Streamable HTTP transport interface to integrate with the Azure AI Foundry Agent Service.

!!! note
    Normally, you'd deploy the MCP server in a production environment, but for this workshop, you'll run it locally in your development environment. This allows you to test and interact with the MCP tools without needing a full deployment.

### Start up a DevTunnel for the MCP Server

1. In a new terminal, authenticate DevTunnel. You'll be prompted to log in with your Azure account, use the same account you used to log in to the Azure AI Foundry Agent Service or Azure Portal. Run the following command:

    ```bash
    devtunnel login
    ```

1. Next, in the terminal where the MCP server is running, start a DevTunnel by running:

    ```bash
    devtunnel host -p 8000 --allow-anonymous
    ```

    This will output a URL that you'll need for the agent to connect to the MCP server. The output will be similar to:

    ```text
    Hosting port: 8000
    Connect via browser: https://<tunnel-id>-8000.aue.devtunnels.ms
    Inspect network activity: https://<tunnel-id>-8000-inspect.aue.devtunnels.ms
    ```

## Update the DevTunnel Environment Variable

1. Copy the **Connect via browser** URL to the clipboard - you'll need it in the next lab to configure the agent.
2. Open the `.env` file in the workshop folder.
3. Update the `DEV_TUNNEL_URL` variable with the copied URL.

    ```text
    DEV_TUNNEL_URL=https://<tunnel-id>-8000.aue.devtunnels.ms
    ```

## Start the Agent App

1. Copy the text below to the clipboard:

    ```text
    Debug: Select and Start Debugging
    ```

2. Press <kbd>F1</kbd> to open the VS Code Command Palette.
3. Paste the text into the Command Palette and select **Debug: Select and Start Debugging**.
4. Select **🌎🤖Debug Compound: Agent and MCP (http)** from the list. This will start the agent app and the web chat client.

## Start a conversation with the Agent

Switch to the **Web Chat** tab in your browser. You should see the agent app running and ready to accept questions.

### Debugging with DevTunnel

You can use DevTunnel to debug the MCP server and the agent app. This allows you to inspect network activity and troubleshoot issues in real-time.

1. Select the **Inspect network activity** URL from the DevTunnel output.
2. This will open a new tab in your browser where you can see the network activity of the MCP server and the agent app.
3. You can use this to debug any issues that arise during the workshop.

You can also set breakpoints in the MCP server code and the agent app code to debug specific issues. To do this:

1. Open the `sales_analysis.py` file in the `mcp_server` folder.
2. Set a breakpoint by clicking in the gutter next to the line number where you want to pause execution.
3. When the execution reaches the breakpoint, you can inspect variables, step through code, and evaluate expressions in the Debug Console.
