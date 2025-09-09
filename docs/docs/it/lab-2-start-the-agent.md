## Cosa Imparerai

In questo lab, abiliterai il Code Interpreter per analizzare i dati di vendita e creare grafici usando il linguaggio naturale.

## Introduzione

In questo lab, estenderai l'Agente Azure AI con due strumenti:

- **Code Interpreter:** Permette all'agente di generare ed eseguire codice Python per analisi e visualizzazione dei dati.
- **Strumenti Server MCP:** Permettono all'agente di accedere a fonti di dati esterne usando Strumenti MCP, nel nostro caso dati in un database PostgreSQL.

## Esercizio del Lab

### Abilita il Code Interpreter e il Server MCP

In questo lab, abiliterai due potenti strumenti che lavorano insieme: il Code Interpreter (che esegue codice Python generato dall'AI per analisi e visualizzazione dei dati) e il Server MCP (che fornisce accesso sicuro ai dati di vendita di Zava memorizzati in PostgreSQL).

=== "Python"

    1. **Apri** il file `app.py`.
    2. **Scorri fino alla riga 50 circa** e trova la riga che aggiunge il Code Interpreter e gli strumenti MCP al toolset dell'agente. Queste righe sono attualmente commentate con un `#` all'inizio.
    3. **Decommenta** le seguenti righe:

        ```python
        
        # code_interpreter = CodeInterpreterTool()
        # self.toolset.add(code_interpreter)
        
        # mcp_tools = McpTool(
        #     server_label="ZavaSalesAnalysisMcpServer",
        #     server_url=Config.DEV_TUNNEL_URL,
        #     allowed_tools=[
        #         "get_multiple_table_schemas",
        #         "execute_sales_query",
        #         "get_current_utc_date",
        #         "semantic_search_products",
        #     ],
        # )

        # mcp_tools.set_approval_mode("never")  # No human in the loop
        # self.toolset.add(mcp_tools)
        ```

        !!! info "Cosa fa questo codice?"
            - **Code Interpreter**: Abilita l'agente ad eseguire codice Python per analisi e visualizzazione dei dati.
            - **Strumenti Server MCP**: Fornisce accesso a fonti di dati esterne con strumenti specifici consentiti e nessuna approvazione umana richiesta. Per applicazioni di produzione, considera l'abilitazione dell'autorizzazione human-in-the-loop per operazioni sensibili.

    4. **Rivedi** il codice che hai decommentato. Il codice dovrebbe apparire esattamente così:

        ```python

        Dopo aver decommentato, il tuo codice dovrebbe apparire così:

        ```python
        class AgentManager:
            """Gestisce il ciclo di vita dell'Agente Azure AI e le dipendenze."""

            async def _setup_agent_tools(self) -> None:
                """Configura strumenti MCP e code interpreter."""
                logger.info("Configurazione strumenti Agente...")
                self.toolset = AsyncToolSet()

                code_interpreter = CodeInterpreterTool()
                self.toolset.add(code_interpreter)

                mcp_tools = McpTool(
                    server_label="ZavaSalesAnalysisMcpServer",
                    server_url=Config.DEV_TUNNEL_URL,
                    allowed_tools=[
                        "get_multiple_table_schemas",
                        "execute_sales_query",
                        "get_current_utc_date",
                        "semantic_search_products",
                    ],
                )

                mcp_tools.set_approval_mode("never")  # Nessun umano nel loop
                self.toolset.add(mcp_tools)
        ```

    ## Avvia l'App Agente

    1. Copia il testo sottostante negli appunti:

    ```text
    Debug: Select and Start Debugging
    ```

    1. Premi <kbd>F1</kbd> per aprire la Palette Comandi di VS Code.
    1. Incolla il testo nella Palette Comandi e seleziona **Debug: Select and Start Debugging**.
    1. Seleziona **🌎🤖Debug Compound: Agent and MCP (http)** dalla lista. Questo avvierà l'app dell'agente e il client web chat.

    Questo avvia i seguenti processi:

    1.  Task DevTunnel (workshop)
    2.  Web Chat (workshop)
    3.  Agent Manager (workshop)
    4.  Server MCP (workshop)

    In VS Code vedrai questi in esecuzione nel pannello TERMINAL.

    ![L'immagine mostra i processi in esecuzione nel pannello TERMINAL di VS Code](../media/vs-code-processes.png)

    ## Apri il Client Web Chat dell'Agente

    === "@Partecipanti all'Evento"

        Seleziona il seguente link per aprire l'app Web Chat nel browser.

        [Apri Web Chat](http://localhost:8005){:target="_blank"}

    === "Studenti Autogestiti"

        ## Rendi la Porta 8005 Pubblica

        Devi rendere la porta 8005 pubblica per accedere al client web chat nel tuo browser.

        1. Seleziona la scheda **Ports** nel pannello inferiore di VS Code.
        2. Fai clic destro sulla porta **Web Chat App (8005)** e seleziona **Port Visibility**.
        3. Seleziona **Public**.

        ![](../media/make-port-public.png)


        ## Apri il Client Web Chat nel Browser

        1.  Copia il testo sottostante negli appunti:

        ```text
        Open Port in Browser
        ```

        2.  Premi <kbd>F1</kbd> per aprire la Palette Comandi di VS Code.
        3.  Incolla il testo nella Palette Comandi e seleziona **Open Port in Browser**.
        4.  Seleziona **8005** dalla lista. Questo aprirà il client web chat dell'agente nel tuo browser.

    ![](../media/agent_web_chat.png)

=== "C#"

    1. **Apri** `AgentService.cs` dalla cartella `Services` del progetto `McpAgentWorkshop.WorkshopApi`.
    2. Naviga al metodo `InitialiseAgentAsync`.
    3. **Decommenta** le seguenti righe:

        ```csharp
        // var mcpTool = new MCPToolDefinition(
        //     ZavaMcpToolLabel,
        //     devtunnelUrl + "mcp");

        // var codeInterpreterTool = new CodeInterpreterToolDefinition();

        // IEnumerable<ToolDefinition> tools = [mcpTool, codeInterpreterTool];

        // persistentAgent = await persistentAgentsClient.Administration.CreateAgentAsync(
        //         name: AgentName,
        //         model: configuration.GetValue<string>("MODEL_DEPLOYMENT_NAME"),
        //         instructions: instructionsContent,
        //         temperature: modelTemperature,
        //         tools: tools);

        // logger.LogInformation("Agent created with ID: {AgentId}", persistentAgent.Id);
        ```

    ## Avvia l'App Agente

    4. Premi <kbd>F1</kbd> per aprire la Palette Comandi di VS Code.
    5. Seleziona **Debug Aspire** come configurazione di lancio.

    Una volta lanciato il debugger, si aprirà una finestra del browser con la dashboard Aspire. Una volta avviati tutti i resources, puoi lanciare l'applicazione web del workshop cliccando il link **Workshop Frontend**.

    ![Dashboard Aspire](../media//lab-2-start-agent-aspire-dashboard.png)

    !!! tip "Risoluzione Problemi"
        Se il browser non si carica, prova a fare un hard-refresh della pagina (Ctrl + F5 o Cmd + Shift + R). Se ancora non si carica, consulta la [guida alla risoluzione problemi](./dotnet-troubleshooting.md).

## Inizia una Conversazione con l'Agente

Dal client web chat, puoi iniziare una conversazione con l'agente. L'agente è progettato per rispondere a domande sui dati di vendita di Zava e generare visualizzazioni usando il Code Interpreter.

1.  Analisi vendite prodotti. Copia e incolla la seguente domanda nella chat:

    ```text
    Mostra i primi 10 prodotti per ricavi per negozio per l'ultimo trimestre
    ```

    Dopo un momento, l'agente risponderà con una tabella che mostra i primi 10 prodotti per ricavi per ogni negozio.

    !!! info
        L'agente usa l'LLM che chiama tre strumenti Server MCP per recuperare i dati e mostrarli in una tabella:

        1. **get_current_utc_date()**: Ottiene data e ora correnti così l'agente può determinare l'ultimo trimestre relativo alla data corrente.
        2. **get_multiple_table_schemas()**: Ottiene gli schemi delle tabelle nel database richiesti dall'LLM per generare SQL valido.
        3. **execute_sales_query**: Esegue una query SQL per recuperare i primi 10 prodotti per ricavi per l'ultimo trimestre dal database PostgreSQL.

    !!! tip
        === "Python"

            Torna a VS Code e seleziona **MCP Server (workspace)** dal pannello TERMINAL e vedrai le chiamate fatte al Server MCP dal Servizio Agenti Azure AI Foundry.

            ![](../media/mcp-server-in-action.png)

        === "C#"

            Nella dashboard Aspire, puoi selezionare i log per il resource `dotnet-mcp-server` per vedere le chiamate fatte al Server MCP dal Servizio Agenti Azure AI Foundry.

            Puoi anche aprire la vista trace e trovare il trace end-to-end dell'applicazione, dall'input utente nella web chat, attraverso le chiamate dell'agente e le chiamate agli strumenti MCP.

            ![Panoramica Trace](../media/lab-7-trace-overview.png)

2.  Genera un grafico a torta. Copia e incolla la seguente domanda nella chat:

    ```text
    Mostra le vendite per negozio come grafico a torta per questo anno finanziario
    ```

    L'agente risponderà con un grafico a torta che mostra la distribuzione delle vendite per negozio per l'anno finanziario corrente.

    !!! info
        Questo potrebbe sembrare magia, quindi cosa succede dietro le quinte per far funzionare tutto?

        Il Servizio Agenti Foundry orchestra i seguenti passi:

        1. Come la domanda precedente, l'agente determina se ha gli schemi di tabella richiesti per la query. Se non li ha, usa gli strumenti **get_multiple_table_schemas()** per ottenere la data corrente e lo schema del database.
        2. L'agente usa poi lo strumento **execute_sales_query** per recuperare le vendite
        3. Usando i dati restituiti, l'LLM scrive codice Python per creare un Grafico a Torta.
        4. Infine, il Code Interpreter esegue il codice Python per generare il grafico.

3.  Continua a fare domande sui dati di vendita Zava per vedere il Code Interpreter in azione. Ecco alcune domande di follow-up che potresti voler provare:

    - `Determina quali prodotti o categorie guidano le vendite. Mostra come Grafico a Barre.`
    - `Quale sarebbe l'impatto di un evento shock (es. calo vendite del 20% in una regione) sulla distribuzione vendite globale? Mostra come Grafico a Barre Raggruppato.`
      - Fai seguito con `E se l'evento shock fosse del 50%?`
    - `Quali regioni hanno vendite sopra o sotto la media? Mostra come Grafico a Barre con Deviazione dalla Media.`
    - `Quali regioni hanno sconti sopra o sotto la media? Mostra come Grafico a Barre con Deviazione dalla Media.`
    - `Simula vendite future per regione usando una simulazione Monte Carlo per stimare intervalli di confidenza. Mostra come Linea con Bande di Confidenza usando colori vividi.`

<!-- ## Ferma l'App Agente

1. Torna all'editor VS Code.
1. Premi <kbd>Shift + F5</kbd> per fermare l'app dell'agente. -->

## Lascia l'App Agente in Esecuzione

Lascia l'app dell'agente in esecuzione perché la userai nel prossimo lab per estendere l'agente con più strumenti e capacità.

*Tradotto usando GitHub Copilot.*
