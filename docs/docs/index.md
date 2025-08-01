# Unlock your agents potential with Model Context Protocol and PostgreSQL Workshop

## A 50-minute interactive workshop

Imagine you are a sales manager at Zava, a retail DIY company with stores across Washington State and a growing online presence. You specialize in outdoor equipment, home improvement tools, and DIY supplies. 

You need to analyze sales data to find trends, understand customer preferences, and make informed business decisions. To help you, Zava has developed a conversational agent that can answer questions about your sales data and even help customers find products using image search.

![Zava Sales Analysis Agent](media/persona.png)

## What you will learn in the workshop

Learn to build an AI agent that analyzes sales data, answers product questions, and helps customers find products using image search. Key topics:

3. **Azure AI Foundry**: Rapidly build and deploy AI agents with integrated tools and observability.
1. **Azure AI Foundry Agent Service**: Build and deploy AI agents with integrated tools and observability.
2. **Model Context Protocol (MCP)**: Connect LLMs to external tools, data, and systems for enhanced functionality.

### Just starting your AI Agents journey?

If you're new to AI agents, start with the [Build your code-first agent with Azure AI Foundry](https://aka.ms/aitour/WRK552){:target="_blank"} workshop. You'll learn to build a code-first agent using Azure AI Foundry, integrating LLMs with databases, documents, and Bing search — a solid foundation for more advanced agents like the Zava Agent.

## What is an LLM-Powered AI Agent?

A Large Language Model (LLM) powered AI Agent is semi-autonomous software designed to achieve a given goal without requiring predefined steps or processes. Instead of following explicitly programmed instructions, the agent determines how to accomplish a task using instructions and context.

For example, if a user asks, "**Show the total sales for each store as a pie chart**", the app doesn't rely on predefined logic for this request. Instead, the LLM interprets the request, manages the conversation flow and context, and orchestrates the necessary actions to produce the store sales pie chart.

Unlike traditional applications, where developers define the logic and workflows to support business processes, AI Agents shift this responsibility to the LLM. In these systems, prompt engineering, clear instructions, and tool development are critical to ensuring the app performs as intended.

## Introduction to the Azure AI Foundry

[Azure AI Foundry](https://azure.microsoft.com/products/ai-foundry/){:target="_blank"} is Microsoft’s secure, flexible platform for designing, customizing, and managing AI apps and agents. Everything—models, agents, tools, and observability—lives behind a single portal, SDK, and REST endpoint, so you can ship to cloud or edge with governance and cost controls in place from day one.

![Azure AI Foundrt Architecture](media/azure-ai-foundry.png)

## What is the Foundry Agent Service?

The Foundry Agent Service offers a fully managed cloud service with SDKs for [Python](https://learn.microsoft.com/azure/ai-services/agents/quickstart?pivots=programming-language-python-azure){:target="_blank"}, [C#](https://learn.microsoft.com/azure/ai-services/agents/quickstart?pivots=programming-language-csharp){:target="_blank"}, and [TypeScript](https://learn.microsoft.com/azure/ai-foundry/agents/quickstart?pivots=programming-language-typescript){:target="_blank"}. The Foundry SDKs simplify AI agent development, reducing complex tasks like tool calling to just a few lines of code.

!!! info
    MCP (Model Context Protocol) provides a standardized way to connect LLMs to external tools and systems. Unlike traditional function calling, MCP offers a more robust, secure, and scalable approach to tool integration, enabling sophisticated interactions between AI agents and data sources.

The Foundry Agent Service offers several advantages over traditional agent platforms:

- **Rapid Deployment**: Optimized SDK for fast deployment, letting developers focus on building agents.
- **Scalability**: Designed to handle varying user loads without performance issues.
- **Custom Integrations**: Supports MCP (Model Context Protocol) for robust tool integration and external data access.
- **Built-in Tools**: Includes Fabric, SharePoint, Azure AI Search, and Azure Storage for quick development.
- **RAG-Style Search**: Features a built-in vector store for efficient file and semantic search.
- **Conversation State Management**: Maintains context across multiple interactions.
- **AI Model Compatibility**: Works with various AI models.

Learn more about the Foundry Agent Service in the [Foundry Agent Service documentation](https://learn.microsoft.com/azure/ai-services/agents/overview){:target="_blank"}.

## AI Agent Frameworks

Popular agent frameworks include LangChain, Semantic Kernel, and CrewAI. What distinguishes the Foundry Agent Service is its seamless integration capabilities and an SDK optimized for rapid deployment. In complex multi-agent scenarios, solutions will combine SDKs like Semantic Kernel and AutoGen with the Foundry Agent Service to build robust and scalable systems.
