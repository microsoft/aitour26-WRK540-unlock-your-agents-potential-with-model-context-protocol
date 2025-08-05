## Architettura della Soluzione

In questo workshop, creerai l'Agente di Vendite Zava: un agente conversazionale progettato per rispondere a domande sui dati di vendita, generare grafici per il business DIY retail di Zava.

## Componenti dell'App Agente

1. **Servizi Microsoft Azure**

    Questo agente è costruito sui servizi Microsoft Azure.

      - **Modello AI Generativa**: Il LLM sottostante che alimenta questa app è il LLM [Azure OpenAI gpt-4o-mini](https://learn.microsoft.com/azure/ai-foundry/openai/concepts/models?tabs=global-standard%2Cstandard-chat-completions#how-do-i-access-the-gpt-4o-and-gpt-4o-mini-models){:target="_blank"}.

      - **Piano di Controllo**: L'app e i suoi componenti architetturali sono gestiti e monitorati utilizzando il portale [Azure AI Foundry](https://ai.azure.com){:target="_blank"}, accessibile tramite browser.

2. **Azure AI Foundry (SDK)**

    Il workshop è offerto in [Python](https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme?view=azure-python-preview&context=%2Fazure%2Fai-services%2Fagents%2Fcontext%2Fcontext){:target="_blank"} utilizzando l'SDK Azure AI Foundry. L'SDK supporta le caratteristiche chiave del servizio Azure AI Agents, inclusi [Code Interpreter](https://learn.microsoft.com/azure/ai-services/agents/how-to/tools/code-interpreter?view=azure-python-preview&tabs=python&pivots=overview){:target="_blank"} e l'integrazione [Model Context Protocol (MCP)](https://modelcontextprotocol.io/){:target="_blank"}.

3. **Database**

    L'app è alimentata dal Database di Vendite Zava, un [server flessibile Azure Database for PostgreSQL](https://www.postgresql.org/){:target="_blank"} con estensione pgvector contenente dati di vendita completi per le operazioni DIY retail di Zava. 

    Il database supporta query complesse per dati di vendite, inventario e clienti. La Row-Level Security (RLS) garantisce che gli agenti accedano solo ai loro negozi assegnati.

4. **Server MCP**

    Il server Model Context Protocol (MCP) è un servizio Python personalizzato che funge da ponte tra l'agente e il database PostgreSQL. Gestisce:

     - **Scoperta dello Schema del Database**: Recupera automaticamente gli schemi del database per aiutare l'agente a comprendere i dati disponibili.
     - **Generazione di Query**: Trasforma le richieste in linguaggio naturale in query SQL.
     - **Esecuzione degli Strumenti**: Esegue query SQL e restituisce risultati in un formato che l'agente può utilizzare.
     - **Servizi Tempo**: Fornisce dati relativi al tempo per generare report sensibili al tempo.

## Estendere la Soluzione del Workshop

Il workshop è facilmente adattabile a casi d'uso come il supporto clienti aggiornando il database e personalizzando le istruzioni del Servizio Agente Foundry.

## Best Practice Dimostrate nell'App

L'app dimostra anche alcune best practice per efficienza ed esperienza utente.

- **API Asincrone**:
  Nel campione del workshop, sia il Servizio Agente Foundry che PostgreSQL utilizzano API asincrone, ottimizzando l'efficienza delle risorse e la scalabilità. Questa scelta di design diventa particolarmente vantaggiosa quando si distribuisce l'applicazione con framework web asincroni come FastAPI, ASP.NET o Streamlit.

- **Token Streaming**:
  Il token streaming è implementato per migliorare l'esperienza utente riducendo i tempi di risposta percepiti per l'app agente alimentata da LLM.

- **Osservabilità**:
  L'app include [tracing](https://learn.microsoft.com/azure/ai-foundry/agents/concepts/tracing){:target="_blank"} e [metriche](https://learn.microsoft.com/azure/ai-foundry/agents/how-to/metrics){:target="_blank"} integrati per monitorare le prestazioni dell'agente, i pattern di utilizzo e la latenza. Questo ti consente di identificare problemi e ottimizzare l'agente nel tempo.

*Tradotto utilizzando GitHub Copilot e GPT-4o.*
