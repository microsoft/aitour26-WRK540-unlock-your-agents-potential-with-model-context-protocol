# Zava Sales Agent — Architecture (Concise)

## Overview
The Zava Sales Agent is a conversational application that answers questions about sales data and can generate charts for a retail DIY business. It runs on Azure and uses an Azure OpenAI model as its core reasoning engine. Management and monitoring happen in Azure AI Foundry.

## High-Level Design

```
User ──> Azure AI Agents Service ──(tool calls/streaming)──> MCP Client
         │
         └─> Azure OpenAI (GPT-4/4o-mini)

MCP Client ◄── stdio/HTTPS ──► MCP Server (sales_analysis)
                                   │
                                   └─> Azure Database for PostgreSQL (+ pgvector, RLS)
```

This follows the MCP pattern: the agent talks to an MCP **client**, which speaks to an MCP **server** exposing tools and data access; in the workshop this runs locally via **stdio**, while production uses **HTTPS**.

## Components

- **Azure AI Agents Service + Streaming**  
  Hosts the agent, streams tokens for responsiveness.

- **Azure OpenAI model**  
  GPT-4/4o-mini powers reasoning and language.

- **Azure AI Foundry (control plane & SDK)**  
  Used to manage the solution and develop with Python, including built-in support for Code Interpreter and MCP.

- **MCP Server (custom Python)**  
  Bridges the agent to the database and tools: discovers schemas, generates/executes SQL, and provides time utilities. Returns structured JSON.

- **Database: Azure Database for PostgreSQL (pgvector, normalized schema, RLS)**  
  Stores sales/product data with performance indexes; pgvector enables similarity scenarios; Row-Level Security limits store access.

## Request Flow

1. **User asks a question** (e.g., sales by product).  
2. **Agent (Azure AI Agents Service)** decides which tool calls are needed and streams partial responses for speed.  
3. **MCP Client → MCP Server** forwards tool calls.  
4. **MCP Server**  
   - Fetches schema details for accurate queries,  
   - Generates and executes SQL against PostgreSQL,  
   - Provides time services where needed,  
   - Returns structured results.  
5. **Agent** may use **Code Interpreter** to turn results into charts and summaries for the user.

## Transports
- **Workshop:** `stdio` between MCP client and server (simple local dev).  
- **Production:** `HTTPS` with auth, logging, and rate/safety policies.

## Non-Functional Practices

- **Asynchronous I/O** for the agent service and PostgreSQL to improve throughput and efficiency.  
- **Token streaming** to reduce perceived latency.  
- **Observability** via tracing and metrics to monitor performance and usage.

## Extensibility
Swap or add tools/data by updating the MCP server and agent instructions. The same pattern adapts easily to other domains (e.g., customer support).

---

**In one sentence:** Azure AI Agents (with Azure OpenAI) call MCP tools over stdio/HTTPS to query a PostgreSQL+pgvector store, with schema-aware SQL execution and strong NFRs (async, streaming, observability), managed through Azure AI Foundry.
