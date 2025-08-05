MCP (Model Context Protocol) è uno standard aperto che permette agli agenti AI di accedere a strumenti esterni, API e fonti di dati attraverso un'interfaccia unificata. Standardizza la scoperta e l'accesso agli strumenti, simile ad OpenAPI per i servizi REST. MCP migliora la componibilità e l'agilità dei sistemi AI semplificando aggiornamenti o sostituzioni di strumenti AI man mano che le tue esigenze aziendali evolvono.

# Benefici Chiave

- **Interoperabilità** – Connetti agenti AI a strumenti abilitati MCP di qualsiasi fornitore con codice personalizzato minimo.  
- **Hook di sicurezza** – Integra accesso, permessi e logging delle attività.  
- **Riusabilità** – Costruisci una volta, riusa attraverso progetti, cloud e runtime.  
- **Semplicità operativa** – Un singolo contratto riduce boilerplate e manutenzione.

# Architettura

```
┌─────────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Agente Azure AI   │    │   Client MCP    │    │   Server MCP    │
│   (main.py)         │◄──►│ (mcp_client.py) │◄──►│ (mcp_server_sales_analysis.py) │
│                     │    └─────────────────┘    └─────────────────┘
│ ┌─────────────────┐ │                                   │
│ │ Servizio        │ │                                   ▼
│ │ Agenti Azure AI │ │                           ┌─────────────────┐
│ │ + Streaming     │ │                           │ Azure Database  │
│ │                 │ │                           │ for PostgreSQL  │
│ └─────────────────┘ │                           │       +         │
└─────────────────────┘                           │    pgvector     │
         │                                        └─────────────────┘
         ▼                                                │
┌─────────────────────┐                           ┌─────────────────┐
│ Azure OpenAI        │                           │ 8 Tabelle       │
│ Model Deployment    │                           │ Normalizzate    │
│ (GPT-4, etc.)       │                           │ con Indici di   │
└─────────────────────┘                           │ Performance     │
                                                  └─────────────────┘
```

# Come Funziona

MCP usa un modello client-server per le interazioni degli agenti AI con risorse esterne:

- **Host MCP:** Runtime o piattaforma che esegue l'agente AI (es., Servizio Agente Azure AI Foundry).  
- **Client MCP:** SDK che converte chiamate di strumenti dell'agente AI in richieste MCP.  
- **Server MCP:** Registra strumenti, esegue richieste, restituisce risultati JSON. Supporta autenticazione, autorizzazione e logging.

### Componenti sul Server MCP

- **Risorse:** Fonti di dati come database, API, archivi file.  
- **Strumenti:** Funzioni registrate o API eseguite su richiesta.  
- **Prompt (opzionale):** Template con versioni per riuso.  
- **Politiche (opzionale):** Limiti e controlli di sicurezza (tasso, profondità, autenticazione).

### Transport MCP

- **HTTP/HTTPS:** Protocolli web standard con supporto streaming.  
- **stdio:** Transport leggero locale o containerizzato che condivide runtime.

Questo workshop usa stdio per comunicazione MCP locale. Le distribuzioni di produzione usano HTTPS per scalabilità e sicurezza.

# Caso d'Uso

In questo workshop, il server MCP collega l'Agente Azure AI ai dati di vendita di Zava. Quando chiedi di prodotti, vendite o inventario:

1. L'agente AI genera richieste Server MCP.  
2. Il Server MCP:  
    - Fornisce informazioni di schema per query accurate.  
    - Esegue query SQL, restituisce dati strutturati.  
    - Offre servizi tempo per report sensibili al tempo.

Questo abilita insight in tempo reale nelle operazioni di vendita di Zava efficientemente.

*Tradotto utilizzando GitHub Copilot e GPT-4o.*
