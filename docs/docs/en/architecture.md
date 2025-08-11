# Architecture Overview

## Core technologies at a glance

- **Azure AI Foundry Agent Service**
  Hosts the LLM-driven agent, handles tool (inc MCP Servers) orchestration, context management, Code Interpreter, and token streaming, and provides auth, logging, and scale.
- **MCP Servers**
  MCP (Model Context Protocol) is an open standard that lets LLMs access external tools, APIs, and data sources through a unified interface. It standardizes tool discovery and access (like OpenAPI for REST) and improves composability by making it easier to update or swap tools as business needs and evolve.
- **PostgreSQL + pgvector**
  Stores relational data and embeddings; supports both relational (SQL) and semantic (vector) queries (via pgvector), governed by SQL and RLS.

**Together:** the Agent Service routes user intents; the MCP server translates them into tool/SQL calls; PostgreSQL+pgvector answers semantic and analytical questions.

## Architecture (high level)

```plaintext
┌─────────────────────┐                         ┌─────────────────┐
│   Zava Agent App    │       stdio/https       │   MCP Server    │
│   (app.py)          │◄───────────────────────►│ (sales_analysis)│
│                     │      MCP Transports     └─────────────────┘
│ ┌─────────────────┐ │                                 │
│ │ Azure AI        │ │                                 ▼
│ │ Agents Service  │ │                         ┌─────────────────┐
│ │ + Streaming     │ │                         │ Azure Database  │
│ │                 │ │                         │ for PostgreSQL  │
│ └─────────────────┘ │                         │   + pgvector    │
└─────────────────────┘                         └─────────────────┘
         │                                              |
         ▼                                              ▼
┌─────────────────────┐                         ┌─────────────────┐
│ Azure OpenAI        │                         │ Zava Sales      │
│ Model Deployments   │                         │ Database with   │
│ - gpt-4o-mini       │                         │ Semantic Search │
│ - text-embedding-3- │                         └─────────────────┘
│   small             │
└─────────────────────┘
```

## Key benefits of MCP Servers

- **Interoperability** – Connect AI agents to any vendor’s MCP‑enabled tools with minimal custom code.
- **Security hooks** – Integrate sign‑in, permissions, and activity logging.
- **Reusability** – Build once, reuse across projects, clouds, and runtimes.
- **Operational simplicity** – A single contract reduces boilerplate and maintenance.

## Best practices demonstrated

- **Asynchronous APIs:** Agents service and PostgreSQL use async APIs; ideal with FastAPI/ASP.NET/Streamlit.
- **Token streaming:** Improves perceived latency in the UI.
- **Observability:** Built‑in tracing and metrics support monitoring and optimization.
- **Security:** PostgreSQL Row Level Security (RLS) ensures data access controls.

## Extensibility

The workshop pattern can be adapted (e.g., customer support) by updating the database + agent instructions in Foundry.
