## Cosa imparerai

In questo laboratorio, abiliterai l'Interprete di Codice per analizzare i dati di vendita e creare grafici usando il linguaggio naturale.

## Introduzione

In questo laboratorio, estenderai l'Agente IA di Azure con due strumenti:

- **Interprete di Codice:** Permette all'agente di generare ed eseguire codice Python per l'analisi dei dati e la visualizzazione.
- **Strumenti del Server MCP:** Permettono all'agente di accedere a fonti di dati esterne usando gli Strumenti MCP, nel nostro caso dati in un database PostgreSQL.

## Esercizio di Laboratorio

### Abilitare l'Interprete di Codice e il Server MCP

In questo laboratorio, abiliterai due potenti strumenti che lavorano insieme: l'Interprete di Codice (che esegue codice Python generato dall'IA per l'analisi dei dati e la visualizzazione) e il Server MCP (che fornisce accesso sicuro ai dati di vendita di Zava memorizzati in PostgreSQL).

=== "Python"

    1. **Apri** il file `app.py`.
    2. **Scorri fino alla riga 67** e trova le righe che aggiungono lo strumento Interprete di Codice e gli strumenti del Server MCP al set di strumenti dell'agente. Queste righe sono attualmente commentate con caratteri **# più spazio** all'inizio.
    3. **Decommenta** le seguenti righe:

        !!! warning "L'indentazione è importante in Python!"
            Quando decommentai, elimina sia il simbolo `#` CHE lo spazio che lo segue. Questo assicura che il codice mantenga la corretta indentazione Python e si allinei correttamente con il codice circostante.

        ```python
        # self.toolset.add(code_interpreter_tool)
        # self.toolset.add(mcp_server_tools)
        ```

        !!! info "Cosa fa questo codice?"
            - **Strumento Interprete di Codice**: Permette all'agente di eseguire codice Python per l'analisi dei dati e la visualizzazione.
            - **Strumenti del Server MCP**: Fornisce accesso a fonti di dati esterne con strumenti specifici consentiti e nessuna approvazione umana richiesta. Per le applicazioni di produzione, considera l'abilitazione dell'autorizzazione umana nel loop per operazioni sensibili.

    4. **Rivedi** il codice che hai decommentato. Il codice dovrebbe apparire esattamente così:

        Dopo aver decommentato, il tuo codice dovrebbe apparire così:

        ```python
        async def _setup_agent_tools(self) -> None:
            """Setup MCP tools and code interpreter."""
            logger.info("Setting up Agent tools...")
            self.toolset = AsyncToolSet()

            code_interpreter_tool = CodeInterpreterTool()

            mcp_server_tools = McpTool(
                server_label="ZavaSalesAnalysisMcpServer",
                server_url=Config.DEV_TUNNEL_URL,
                allowed_tools=[
                    "get_multiple_table_schemas",
                    "execute_sales_query",
                    "get_current_utc_date",
                    "semantic_search_products",
                ],
            )
            mcp_server_tools.set_approval_mode("never")  # No human in the loop

            self.toolset.add(code_interpreter_tool)
            self.toolset.add(mcp_server_tools)
        ```

    ## Avviare l'Applicazione dell'Agente

    1. Copia il testo sottostante negli appunti:

    ```text
    Debug: Select and Start Debugging
    ```

    1. Premi <kbd>F1</kbd> per aprire la Palette dei Comandi di VS Code.
    1. Incolla il testo nella Palette dei Comandi e seleziona **Debug: Select and Start Debugging**.
    1. Seleziona **🌎🤖Debug Compound: Agent and MCP (http)** dalla lista. Questo avvierà l'applicazione dell'agente e il client di chat web.

    Questo avvia i seguenti processi:

    1.  DevTunnel (workshop) Task
    2.  Web Chat (workshop)
    3.  Agent Manager (workshop)
    4.  MCP Server (workshop)

    In VS Code vedrai questi in esecuzione nel pannello TERMINAL.

    ![L'immagine mostra i processi in esecuzione nel pannello TERMINAL di VS Code](../media/vs-code-processes.png)

    ## Aprire il Client di Chat Web dell'Agente

    === "@Partecipanti all'Evento"

        Seleziona il seguente link per aprire l'applicazione di Chat Web nel browser.

        [Apri Chat Web](http://localhost:8005){:target="_blank"}

    === "Studenti Autodidatti"

        ## Rendere Pubblico il Porto 8005

        Devi rendere pubblico il porto 8005 per poter accedere al client di chat web nel tuo browser.

        1. Seleziona la scheda **Ports** nel pannello inferiore di VS Code.
        2. Fai clic destro sul porto **Web Chat App (8005)** e seleziona **Port Visibility**.
        3. Seleziona **Public**.

        ![](../media/make-port-public.png)


        ## Aprire il Client di Chat Web nel Browser

        1.  Copia il testo sottostante negli appunti:

        ```text
        Open Port in Browser
        ```

        2.  Premi <kbd>F1</kbd> per aprire la Palette dei Comandi di VS Code.
        3.  Incolla il testo nella Palette dei Comandi e seleziona **Open Port in Browser**.
        4.  Seleziona **8005** dalla lista. Questo aprirà il client di chat web dell'agente nel tuo browser.

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

    ## Avviare l'Applicazione dell'Agente

    4. Premi <kbd>F1</kbd> per aprire la Palette dei Comandi di VS Code.
    5. Seleziona **Debug Aspire** come configurazione di avvio.

    Una volta avviato il debugger, si aprirà una finestra del browser con il dashboard Aspire. Una volta che tutte le risorse sono state avviate, puoi lanciare l'applicazione web del workshop cliccando sul link **Workshop Frontend**.

    ![Dashboard Aspire](../media//lab-2-start-agent-aspire-dashboard.png)

    !!! tip "Risoluzione dei problemi"
        Se il browser non si carica, prova a fare un aggiornamento forzato della pagina (Ctrl + F5 o Cmd + Shift + R). Se ancora non si carica, fai riferimento alla [guida alla risoluzione dei problemi](./dotnet-troubleshooting.md).

## Iniziare una Conversazione con l'Agente

Dal client di chat web, puoi iniziare una conversazione con l'agente. L'agente è progettato per rispondere a domande sui dati di vendita di Zava e generare visualizzazioni usando l'Interprete di Codice.

1.  Analisi delle vendite dei prodotti. Copia e incolla la seguente domanda nella chat:

    ```text
    Show the top 10 products by revenue by store for the last quarter
    ```

    Dopo un momento, l'agente risponderà con una tabella che mostra i 10 prodotti principali per ricavi per ogni negozio.

    !!! info
        L'agente usa l'LLM che chiama tre strumenti del Server MCP per recuperare i dati e visualizzarli in una tabella:

        1. **get_current_utc_date()**: Ottiene la data e l'ora correnti così l'agente può determinare l'ultimo trimestre relativo alla data corrente.
        2. **get_multiple_table_schemas()**: Ottiene gli schemi delle tabelle nel database richiesti dall'LLM per generare SQL valido.
        3. **execute_sales_query**: Esegue una query SQL per recuperare i 10 prodotti principali per ricavi per l'ultimo trimestre dal database PostgreSQL.

    !!! tip
        === "Python"

            Torna a VS Code e seleziona **MCP Server (workspace)** dal pannello TERMINAL e vedrai le chiamate fatte al Server MCP dal Servizio Agente di Azure AI Foundry.

            ![](../media/mcp-server-in-action.png)

        === "C#"

            Nel dashboard Aspire, puoi selezionare i log per la risorsa `dotnet-mcp-server` per vedere le chiamate fatte al Server MCP dal Servizio Agente di Azure AI Foundry.

            Puoi anche aprire la vista delle tracce e trovare la traccia end-to-end dell'applicazione, dall'input dell'utente nella chat web, alle chiamate dell'agente e alle chiamate degli strumenti MCP.

            ![Panoramica della traccia](../media/lab-7-trace-overview.png)

2.  Generare un grafico a torta. Copia e incolla la seguente domanda nella chat:

    ```text
    Show sales by store as a pie chart for this financial year
    ```

    L'agente risponderà con un grafico a torta che mostra la distribuzione delle vendite per negozio per l'anno finanziario corrente.

    !!! info
        Questo potrebbe sembrare magico, quindi cosa succede dietro le quinte per far funzionare tutto?

        Il Servizio Agente Foundry orchestra i seguenti passaggi:

        1. Come per la domanda precedente, l'agente determina se ha gli schemi delle tabelle richiesti per la query. Se non li ha, usa gli strumenti **get_multiple_table_schemas()** per ottenere la data corrente e lo schema del database.
        2. L'agente quindi usa lo strumento **execute_sales_query** per recuperare le vendite
        3. Usando i dati restituiti, l'LLM scrive codice Python per creare un Grafico a Torta.
        4. Infine, l'Interprete di Codice esegue il codice Python per generare il grafico.

3.  Continua a fare domande sui dati di vendita di Zava per vedere l'Interprete di Codice in azione. Ecco alcune domande di follow-up che potresti voler provare:

    - `Determine which products or categories drive sales. Show as a Bar Chart.`
    - `What would be the impact of a shock event (e.g., 20% sales drop in one region) on global sales distribution? Show as a Grouped Bar Chart.`
      - Seguito da `What if the shock event was 50%?`
    - `Which regions have sales above or below the average? Show as a Bar Chart with Deviation from Average.`
    - `Which regions have discounts above or below the average? Show as a Bar Chart with Deviation from Average.`
    - `Simulate future sales by region using a Monte Carlo simulation to estimate confidence intervals. Show as a Line with Confidence Bands using vivid colors.`

<!-- ## Stop the Agent App

1. Switch back to the VS Code editor.
1. Press <kbd>Shift + F5</kbd> to stop the agent app. -->

## Lasciare l'Applicazione dell'Agente in Esecuzione

Lascia l'applicazione dell'agente in esecuzione poiché la userai nel prossimo laboratorio per estendere l'agente con più strumenti e capacità.

*Tradotto usando GitHub Copilot.*
