MCP (Protocolo de Contexto de Modelo) é um padrão aberto que permite aos agentes de IA acessar ferramentas externas, APIs e fontes de dados através de uma interface unificada. Ele padroniza a descoberta e acesso a ferramentas, similar ao OpenAPI para serviços REST. O MCP melhora a composabilidade e agilidade de sistemas de IA simplificando atualizações ou substituições de ferramentas de IA conforme suas necessidades comerciais evoluem.

# Benefícios Principais

- **Interoperabilidade** – Conecte agentes de IA a ferramentas habilitadas para MCP de qualquer fornecedor com código personalizado mínimo.  
- **Ganchos de segurança** – Integre login, permissões e registro de atividades.  
- **Reutilização** – Construa uma vez, reutilize em projetos, nuvens e runtimes.  
- **Simplicidade operacional** – Contrato único reduz código repetitivo e manutenção.

# Arquitetura

```
┌─────────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Agente Azure AI   │    │   Cliente MCP   │    │   Servidor MCP  │
│   (main.py)         │◄──►│ (mcp_client.py) │◄──►│ (mcp_server_sales_analysis.py) │
│                     │    └─────────────────┘    └─────────────────┘
│ ┌─────────────────┐ │                                   │
│ │ Serviço         │ │                                   ▼
│ │ Agentes Azure   │ │                           ┌─────────────────┐
│ │ AI + Streaming  │ │                           │ Azure Database  │
│ │                 │ │                           │ for PostgreSQL  │
│ └─────────────────┘ │                           │       +         │
└─────────────────────┘                           │    pgvector     │
         │                                        └─────────────────┘
         ▼                                                │
┌─────────────────────┐                           ┌─────────────────┐
│ Implantação Modelo  │                           │ 8 Tabelas       │
│ Azure OpenAI        │                           │ Normalizadas    │
│ (GPT-4, etc.)       │                           │ com Índices de  │
└─────────────────────┘                           │ Desempenho      │
                                                  └─────────────────┘
```

# Como Funciona

O MCP usa um modelo cliente-servidor para interações de agente de IA com recursos externos:

- **Host MCP:** Runtime ou plataforma executando o agente de IA (ex: Serviço de Agente Azure AI Foundry).  
- **Cliente MCP:** SDK convertendo chamadas de ferramentas do agente de IA em solicitações MCP.  
- **Servidor MCP:** Registra ferramentas, executa solicitações, retorna resultados JSON. Suporta autenticação, autorização e registro.

### Componentes no Servidor MCP

- **Recursos:** Fontes de dados como bancos de dados, APIs, armazenamentos de arquivos.  
- **Ferramentas:** Funções ou APIs registradas executadas sob demanda.  
- **Prompts (opcional):** Templates versionados para reutilização.  
- **Políticas (opcional):** Limites e verificações de segurança (taxa, profundidade, autenticação).

### Transportes MCP

- **HTTP/HTTPS:** Protocolos web padrão com suporte a streaming.  
- **stdio:** Transporte leve local ou containerizado compartilhando runtime.

Este workshop usa stdio para comunicação MCP local. Implantações de produção usam HTTPS para escalabilidade e segurança.

# Caso de Uso

Neste workshop, o servidor MCP vincula o Agente Azure AI aos dados de vendas da Zava. Quando você pergunta sobre produtos, vendas ou inventário:

1. O agente de IA gera solicitações do Servidor MCP.  
2. O Servidor MCP:  
    - Fornece informações de esquema para consultas precisas.  
    - Executa consultas SQL, retorna dados estruturados.  
    - Oferece serviços de tempo para relatórios sensíveis ao tempo.

Isso habilita insights em tempo real sobre as operações de vendas da Zava de forma eficiente.

*Traduzido usando GitHub Copilot e GPT-4o.*
