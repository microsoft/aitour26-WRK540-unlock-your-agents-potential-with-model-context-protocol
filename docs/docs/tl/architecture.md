## Mga Core technologies sa isang sulyap

- **Azure AI Foundry Agent Service**
  Nag-host ng LLM-driven agent; nag-orchestrate ng tools (kasama ang MCP Servers); namamahala ng context, Code Interpreter, at token streaming; at nagbibigay ng authentication, logging, at scaling.
- **MCP Servers**
  Ang MCP (Model Context Protocol) ay open standard na nagbibigay sa mga LLM ng unified interface sa external tools, APIs, at data. Pinapastandard nito ang tool discovery (tulad ng OpenAPI para sa REST) at pinapahusay ang composability sa pamamagitan ng paggawa ng mga tools na madaling i-update o palitan habang umuunlad ang mga pangangailangan.
- **PostgreSQL + pgvector**
  Nag-iimbak ng relational data at embeddings; sumusuporta sa relational (SQL) at semantic (vector) queries (via pgvector), na pinapamahalaan ng SQL at RLS.

**Sama-sama:** nire-route ng Agent Service ang user intents; sinasalin ng MCP server ang mga ito sa tool/SQL calls; sinasagot ng PostgreSQL+pgvector ang semantic at analytical questions.

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

## Mga Key benefits ng MCP Servers

- **Interoperability** – Ikonekta ang AI agents sa anumang vendor's MCP‑enabled tools na may minimal custom code.
- **Security hooks** – Isama ang sign‑in, permissions, at activity logging.
- **Reusability** – Gawin minsan, gamitin muli sa mga projects, clouds, at runtimes.
- **Operational simplicity** – Isang contract ang nagbabawas ng boilerplate at maintenance.

## Mga Best practices na ipinakita

- **Asynchronous APIs:** Gumagamit ang agents service at PostgreSQL ng async APIs; ideal sa FastAPI/ASP.NET/Streamlit.
- **Token streaming:** Pinapahusay ang perceived latency sa UI.
- **Observability:** Built‑in tracing at metrics support para sa monitoring at optimization.
- **Database security:** Secured ang PostgreSQL na may restricted agent privileges at Row‑Level Security (RLS), na naglilimita sa mga agents sa kanilang authorized data lamang.
- **Code Interpreter:** Ang [Azure AI Agents Service Code Interpreter](https://learn.microsoft.com/azure/ai-services/agents/how-to/tools/code-interpreter?view=azure-python-preview&tabs=python&pivots=overview){:target="_blank"} ay tumatakbo ng LLM‑generated code on demand sa **sandboxed** environment, na pumipigil sa mga actions na lampas sa scope ng agent.

## Extensibility

Maaaring i-adapt ang workshop pattern (e.g., customer support) sa pamamagitan ng pag-update ng database + agent instructions sa Foundry.

*Isinalin gamit ang GitHub Copilot.*
