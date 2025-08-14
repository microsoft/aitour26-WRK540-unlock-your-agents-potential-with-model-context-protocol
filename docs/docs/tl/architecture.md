## Mga pangunahing teknolohiya sa isang tingin

- **Azure AI Foundry Agent Service**
  Naghahost ng LLM-driven agent; nag-o-orchestrate ng mga tool (kabilang ang mga MCP Server); namamahala ng context, Code Interpreter, at token streaming; at nagbibigay ng authentication, logging, at scaling.
- **MCP Servers**
  Ang MCP (Model Context Protocol) ay isang open standard na nagbibigay sa mga LLM ng pinag-isang interface sa panlabas na mga tool, API, at datos. Istandardisa nito ang tool discovery (tulad ng OpenAPI para sa REST) at pinapahusay ang composability sa pamamagitan ng pagpapadali ng pag-update o pagpapalit ng mga tool habang umuunlad ang pangangailangan.
- **PostgreSQL + pgvector**
  Nagtatago ng relational data at embeddings; sumusuporta sa parehong relational (SQL) at semantic (vector) queries (sa pamamagitan ng pgvector), pinamamahalaan ng SQL at RLS.

**Sama-sama:** Ipinapasa ng Agent Service ang user intents; isinasalin ito ng MCP server sa mga tool/SQL calls; sinasagot ng PostgreSQL+pgvector ang semantic at analytical na mga tanong.

## Arkitektura (high level)

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

## Mga pangunahing benepisyo ng MCP Servers

- **Interoperability** – Ikonekta ang AI agents sa anumang vendor na MCP‑enabled tools na may minimal na custom code.
- **Security hooks** – Isama ang sign‑in, permissions, at activity logging.
- **Reusability** – Bumuo nang isang beses, gamitin muli sa magkakaibang proyekto, cloud, at runtime.
- **Operational simplicity** – Isang kontrata lang kaya mas kaunting boilerplate at maintenance.

## Mga best practice na ipinapakita

- **Asynchronous APIs:** Gumagamit ng async APIs ang Agents service at PostgreSQL; perpekto sa FastAPI/ASP.NET/Streamlit.
- **Token streaming:** Pinapaganda ang perceived latency sa UI.
- **Observability:** Built‑in tracing at metrics para sa monitoring at optimization.
- **Database security:** Sini-secure ang PostgreSQL gamit ang restricted agent privileges at Row‑Level Security (RLS), nililimitahan ang mga agent sa awtorisadong datos lamang.
- **Code Interpreter:** Ang [Azure AI Agents Service Code Interpreter](https://learn.microsoft.com/azure/ai-services/agents/how-to/tools/code-interpreter?view=azure-python-preview&tabs=python&pivots=overview){:target="_blank"} ay nagpapatakbo ng LLM‑generated code on demand sa isang **sandboxed** na environment, pumipigil sa mga aksyon na lampas sa saklaw ng agent.

## Extensibility

Maaaring iakma ang workshop pattern (hal., para sa customer support) sa pamamagitan ng pag-update ng database + agent instructions sa Foundry.

*Isinalin gamit ang GitHub Copilot.*
