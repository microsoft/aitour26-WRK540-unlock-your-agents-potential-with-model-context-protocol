MCP (Model Context Protocol) is an emerging open standard that enables large language models (LLMs) to access external tools, APIs, and data sources through a consistent interface.

Technically, MCP standardizes tool discovery and access for AI agents—similar to how the OpenAPI Specification does for REST services.

From a business perspective, MCP improves agility by making it easier to update or replace AI tools as your needs evolve.


## Benefits of MCP

- **Interoperability** – Connect an LLM to tools from any vendor that exposes an MCP interface, with little or no bespoke code.
- **Security hooks** – MCP includes hooks so you can plug in your own sign-in, permissions, and activity-logging systems.
- **Reusability** – Implement a tool once and reuse it across projects, clouds, and runtimes.
- **Operational simplicity** – When all parties adopt MCP, a single contract reduces boilerplate and lowers maintenance overhead.

## How MCP Works

MCP uses a client-server model to organize interactions between AI models and external resources:

- **MCP Host:** The runtime or platform where the LLM executes (e.g., Azure AI Foundry Agent Service).
- **MCP Client:** A library or SDK that converts the model’s tool calls or data queries into MCP‑formatted requests and forwards them to the server.
- **MCP Server:** A service that registers tools, exposes them for discovery, executes them on request, and returns results in a standardized JSON format. It can be extended with authentication, authorization, and logging as needed.

### Key Components on an MCP Server

- **Resources** – Data sources (databases, APIs, file stores) the server can query and return in a canonical format.
- **Tools** – Named functions or APIs registered with the server that it can execute on demand.
- **Prompts (optional)** – Versioned prompt templates the server can store for reuse across models or projects.
- **Policies (optional)** – Limits and safety checks (rate, depth, authentication) the server enforces around each tool call.

### MCP Transports

MCP supports multiple transport protocols for communication between clients and servers, including:

- HTTP/HTTPS (streamable) – Standard web protocols, often with streaming support for real-time, scalable communication.
- stdio – Lightweight transport for local or containerized setups, where the client and server share the same runtime.

This workshop uses stdio for MCP communication to avoid network overhead—ideal for local use. In production, however, MCP servers are deployed in the cloud and should use HTTPS for scalability and security.

## Real-World Applications

- **Enterprise Data Integration:** Connect LLMs to databases, CRMs, internal tools.
- **Agentic AI:** Enable autonomous agents with tool access.

## MCP in the Zava Sales Agent

In this workshop, the MCP server connects the Azure AI Agent with Zava's sales data. When you ask about products, sales, or inventory:

1. The LLM generates MCP Server requests based on your query
1. The MCP Server:
      1. Provides schema info to help the LLM generate accurate queries
      2. Runs SQL queries and returns structured data for natural-language responses
      3. Provides time services for time-sensitive reports

<!-- 4. It enables image search via [pgvector](https://learn.microsoft.com/en-us/azure/postgresql/flexible-server/how-to-use-pgvector){:target="_blank"} -->

This lets the agent deliver real-time insights into Zava's sales operations efficiently.

## Architecture

```text
┌─────────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Azure AI Agent    │    │   MCP Client    │    │   MCP Server    │
│   (main.py)         │◄──►│ (mcp_client.py) │◄──►│ (mcp_server_sales_analysis.py) │
│                     │    └─────────────────┘    └─────────────────┘
│ ┌─────────────────┐ │                                   │
│ │ Azure AI        │ │                                   ▼
│ │ Agents Service  │ │                           ┌─────────────────┐
│ │ + Streaming     │ │                           │ Azure Database  │
│ │                 │ │                           │ for PostgreSQL  │
│ └─────────────────┘ │                           │       +         │
└─────────────────────┘                           │    pgvector     │
         │                                        └─────────────────┘
         ▼                                                │
┌─────────────────────┐                           ┌─────────────────┐
│ Azure OpenAI        │                           │ 8 Normalized    │
│ Model Deployment    │                           │ Tables with     │
│ (GPT-4, etc.)       │                           │ Performance     │
└─────────────────────┘                           │ Indexes         │
                                                  └─────────────────┘
```

This architecture shows how the Azure AI Agent interacts with the MCP Client and Server to access external data and tools, enabling powerful AI capabilities.
