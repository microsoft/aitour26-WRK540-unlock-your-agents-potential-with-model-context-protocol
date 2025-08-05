MCP (Model Context Protocol) is an open standard that lets AI agents access external tools, APIs, and data sources through a unified interface. It standardizes tool discovery and access, similar to OpenAPI for REST services. MCP improves AI system composability and agility by simplifying updates or replacements of AI tools as your business needs evolve.

# Key Benefits

- **Interoperability** – Connect AI agents to any vendor’s MCP-enabled tools with minimal custom code.  
- **Security hooks** – Integrate sign-in, permissions, and activity logging.  
- **Reusability** – Build once, reuse across projects, clouds, and runtimes.  
- **Operational simplicity** – Single contract reduces boilerplate and maintenance.

# Architecture

```
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

# How It Works

MCP uses a client-server model for AI agent interactions with external resources:

- **MCP Host:** Runtime or platform running the AI agent (e.g., Azure AI Foundry Agent Service).  
- **MCP Client:** SDK converting AI agent tool calls into MCP requests.  
- **MCP Server:** Registers tools, executes requests, returns JSON results. Supports authentication, authorization, and logging.

### Components on MCP Server

- **Resources:** Data sources like databases, APIs, file stores.  
- **Tools:** Registered functions or APIs executed on demand.  
- **Prompts (optional):** Versioned templates for reuse.  
- **Policies (optional):** Limits and safety checks (rate, depth, authentication).

### MCP Transports

- **HTTP/HTTPS:** Standard web protocols with streaming support.  
- **stdio:** Lightweight local or containerized transport sharing runtime.

This workshop uses stdio for local MCP communication. Production deployments use HTTPS for scalability and security.

# Use Case

In this workshop, the MCP server links the Azure AI Agent to Zava's sales data. When you ask about products, sales, or inventory:

1. The AI agent generates MCP Server requests.  
2. The MCP Server:  
    - Provides schema info for accurate queries.  
    - Runs SQL queries, returns structured data.  
    - Offers time services for time-sensitive reports.

This enables real-time insights into Zava's sales operations efficiently.
