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
    Hosting port: 8010
    Connect via browser: https://<tunnel-id>-8010.aue.devtunnels.ms
    Inspect network activity: https://<tunnel-id>-8010-inspect.aue.devtunnels.ms
    ```

1. Copy the **Connect via browser** URL to the clipboard - you'll need it in the next lab to configure the agent.

## Next Steps

Once the Dev Tunnel is running, you can proceed to the next lab where you'll configure the agent to use MCP Server and start interacting with the system.
