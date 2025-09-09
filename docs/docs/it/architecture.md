## Tecnologie principali in sintesi

- **Servizio Agenti Azure AI Foundry**
  Ospita l'agente guidato da LLM; orchestra strumenti (inclusi i server MCP); gestisce contesto, Code Interpreter e streaming di token; e fornisce autenticazione, logging e scalabilità.
- **Server MCP**
  MCP (Model Context Protocol) è uno standard aperto che fornisce agli LLM un'interfaccia unificata a strumenti esterni, API e dati. Standardizza la scoperta degli strumenti (come OpenAPI per REST) e migliora la componibilità rendendo gli strumenti facili da aggiornare o sostituire man mano che le esigenze si evolvono.
- **PostgreSQL + pgvector**
  Memorizza dati relazionali ed embeddings; supporta query sia relazionali (SQL) che semantiche (vettoriali) (tramite pgvector), governate da SQL e RLS.

**Insieme:** il Servizio Agenti instrada le intenzioni dell'utente; il server MCP le traduce in chiamate a strumenti/SQL; PostgreSQL+pgvector risponde a domande semantiche e analitiche.

## Architettura (alto livello)

```plaintext
┌─────────────────────┐                         ┌─────────────────┐
│   App Agente Zava   │       stdio/https       │   Server MCP    │
│   (app.py)          │◄───────────────────────►│ (sales_analysis)│
│                     │      Trasporti MCP      └─────────────────┘
│ ┌─────────────────┐ │                                 │
│ │ Servizio        │ │                                 ▼
│ │ Agenti AI Azure │ │                         ┌─────────────────┐
│ │ + Streaming     │ │                         │ Azure Database  │
│ │                 │ │                         │ per PostgreSQL  │
│ └─────────────────┘ │                         │   + pgvector    │
└─────────────────────┘                         └─────────────────┘
         │                                              |
         ▼                                              ▼
┌─────────────────────┐                         ┌─────────────────┐
│ Distribuzioni       │                         │ Database Vendite │
│ Modelli Azure OpenAI│                         │ Zava con        │
│ - gpt-4o-mini       │                         │ Ricerca         │
│ - text-embedding-3- │                         │ Semantica       │
│   small             │                         └─────────────────┘
└─────────────────────┘
```

## Vantaggi principali dei Server MCP

- **Interoperabilità** – Collega agenti AI a strumenti abilitati MCP di qualsiasi fornitore con codice personalizzato minimo.
- **Hook di sicurezza** – Integra accesso, permessi e logging delle attività.
- **Riusabilità** – Costruisci una volta, riusa attraverso progetti, cloud e runtime.
- **Semplicità operativa** – Un singolo contratto riduce boilerplate e manutenzione.

## Best practice dimostrate

- **API asincrone:** Il servizio agenti e PostgreSQL usano API asincrone; ideali con FastAPI/ASP.NET/Streamlit.
- **Streaming di token:** Migliora la latenza percepita nell'UI.
- **Osservabilità:** Tracciamento e metriche integrate supportano monitoraggio e ottimizzazione.
- **Sicurezza database:** PostgreSQL è protetto con privilegi dell'agente limitati e Row-Level Security (RLS), limitando gli agenti solo ai loro dati autorizzati.
- **Code Interpreter:** Il [Code Interpreter del Servizio Agenti Azure AI](https://learn.microsoft.com/azure/ai-services/agents/how-to/tools/code-interpreter?view=azure-python-preview&tabs=python&pivots=overview){:target="_blank"} esegue codice generato da LLM su richiesta in un ambiente **sandboxed**, prevenendo azioni oltre lo scopo dell'agente.

### Estensibilità

Il pattern del workshop può essere adattato (es. supporto clienti) aggiornando il database + istruzioni dell'agente in Foundry.

## Architettura DevTunnel

Nell'ambiente workshop, il Servizio Agenti gira in Azure ma deve connettersi al tuo Server MCP in esecuzione locale. DevTunnel crea un tunnel sicuro che espone il tuo Server MCP locale al Servizio Agenti basato su cloud.

```plaintext
          Cloud Azure                           Sviluppo Locale
    ┌─────────────────────┐                  ┌─────────────────────┐
    │   App Agente Zava   │                  │                     │
    │   (Ospitato Azure)  │                  │  ┌─────────────────┐│
    │                     │                  │  │   Server MCP    ││
    │ ┌─────────────────┐ │                  │  │ (sales_analysis)││
    │ │ Servizio        │ │                  │  │ localhost:8000  ││
    │ │ Agenti AI Azure │ │                  │  └─────────────────┘│
    │ └─────────────────┘ │                  │           │         │
    └─────────────────────┘                  │           ▼         │
              │                              │  ┌─────────────────┐│
              │ Richieste HTTPS              │  │   PostgreSQL    ││
              ▼                              │  │   + pgvector    ││
    ┌─────────────────────┐                  │  └─────────────────┘│
    │   DevTunnel         │                  │                     │
    │   Endpoint Pubblico │◄─────────────────┼──── Tunnel Sicuro   │
    │ (*.devtunnels.ms)   │    Port Forward  │                     │
    └─────────────────────┘                  └─────────────────────┘
```

**Come Funziona DevTunnel nel Workshop:**

1. **Sviluppo Locale**: Esegui il Server MCP localmente su `localhost:8000`
2. **Creazione DevTunnel**: DevTunnel crea un endpoint HTTPS pubblico (es. `https://abc123.devtunnels.ms`) connesso a `localhost:8000`.
3. **Integrazione Azure**: Il Servizio Agenti ospitato su Azure si connette al Server MCP attraverso l'endpoint DevTunnel.
4. **Operazione Trasparente**: Il servizio agenti opera normalmente, inconsapevole di accedere al Server MCP in esecuzione locale attraverso un tunnel.

Questa configurazione ti permette di:

- Sviluppare e debuggare localmente mentre usi servizi AI basati su cloud
- Testare scenari realistici senza distribuire il Server MCP su Azure

*Tradotto usando GitHub Copilot.*
