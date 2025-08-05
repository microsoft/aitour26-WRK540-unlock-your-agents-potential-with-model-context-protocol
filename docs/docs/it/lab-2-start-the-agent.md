## Cosa Imparerai

In questo lab, abiliterai il Code Interpreter per analizzare i dati di vendita e creare grafici usando il linguaggio naturale.

## Introduzione

In questo lab, estenderai l'Agente Azure AI con due strumenti:

- **Code Interpreter:** Permette all'agente di generare ed eseguire codice Python per analisi dei dati e visualizzazione.
- **Strumenti Server MCP:** Permettono all'agente di accedere a fonti di dati esterne usando Strumenti MCP, nel nostro caso dati in un database PostgreSQL.

## Esercizio del Lab

### Abilita il Code Interpreter

In questo lab, abiliterai il Code Interpreter per eseguire codice Python generato dal LLM per analizzare i dati di vendita retail di Zava.

=== "Python"

    1. **Apri** il file `app.py`.
    2. **Decommenta** la riga che aggiunge lo strumento Code Interpreter al toolset dell'agente nel metodo `_setup_agent_tools` della classe `AgentManager`. Questa riga è attualmente commentata con un `#` all'inizio.:

        ```python
        # code_interpreter = CodeInterpreterTool()
        # self.toolset.add(code_interpreter)
        ```

    3. **Rivedi** il codice nel file `app.py`. Noterai che il Code Interpreter e gli strumenti Server MCP sono aggiunti al toolset dell'agente nel metodo `_setup_agent_tools` della classe `AgentManager`.

        ```python

        Dopo aver decommentato, il tuo codice dovrebbe apparire così:

        ```python
        class AgentManager:
            """Manages Azure AI Agent lifecycle and dependencies."""

            async def _setup_agent_tools(self) -> None:
                """Setup MCP tools and code interpreter."""

                # Enable the code interpreter tool
                code_interpreter = CodeInterpreterTool()
                self.toolset.add(code_interpreter)

                print("Setting up Agent tools...")
                ...
        ```

=== "C#"

    TBD

## Avvia l'App Agente

1. Copia il testo qui sotto negli appunti:

    ```text
    Debug: Select and Start Debugging
    ```

2. Premi <kbd>F1</kbd> per aprire la Command Palette di VS Code.
3. Incolla il testo nella Command Palette e seleziona **Debug: Select and Start Debugging**.
4. Seleziona **🔁🤖Debug Compound: Agent and MCP (stdio)** dalla lista. Questo avvierà l'app agente e il client di chat web.

## Apri il Client Web Chat dell'Agente

1. Copia il testo qui sotto negli appunti:

    ```text
    Open Port in Browser
    ```

2. Premi <kbd>F1</kbd> per aprire la Command Palette di VS Code.
3. Incolla il testo nella Command Palette e seleziona **Open Port in Browser**.
4. Seleziona **8005** dalla lista. Questo aprirà il client web chat dell'agente nel tuo browser.

### Avvia una Conversazione con l'Agente

Dal client web chat, puoi iniziare una conversazione con l'agente. L'agente è progettato per rispondere a domande sui dati di vendita di Zava e generare visualizzazioni usando il Code Interpreter.

1. Analisi delle vendite dei prodotti. Copia e incolla la seguente domanda nella chat:

    ```text
    Mostra i 10 prodotti migliori per fatturato per negozio per l'ultimo trimestre
    ```

    Dopo un momento, l'agente risponderà con una tabella che mostra i 10 prodotti migliori per fatturato per ogni negozio.

    !!! info
        L'agente usa il LLM chiama tre strumenti Server MCP per recuperare i dati e visualizzarli in una tabella:

           1. **get_current_utc_date()**: Ottiene la data e l'ora correnti così l'agente può determinare l'ultimo trimestre relativo alla data corrente.
           2. **get_multiple_table_schemas()**: Ottiene gli schemi delle tabelle nel database richiesti dal LLM per generare SQL valido.
           3. **execute_sales_query**: Esegue una query SQL per recuperare i 10 prodotti migliori per fatturato per l'ultimo trimestre dal database PostgreSQL.

2. Genera un grafico a torta. Copia e incolla la seguente domanda nella chat:

    ```text
    Mostra le vendite per negozio come grafico a torta per questo anno finanziario
    ```

    L'agente risponderà con un grafico a torta che mostra la distribuzione delle vendite per negozio per l'anno finanziario corrente.

    !!! info
        Questo potrebbe sembrare magico, quindi cosa sta succedendo dietro le quinte per far funzionare tutto?

        Il Servizio Agente Foundry orchestra i seguenti passaggi:

        1. Come la domanda precedente, l'agente determina se ha gli schemi delle tabelle richiesti per la query. Se no, usa gli strumenti **get_multiple_table_schemas()** per ottenere la data corrente e lo schema del database.
        2. L'agente quindi usa lo strumento **execute_sales_query** per recuperare le vendite
        3. Usando i dati restituiti, il LLM scrive codice Python per creare un Grafico a Torta.
        4. Infine, il Code Interpreter esegue il codice Python per generare il grafico.

3. Continua a fare domande sui dati di vendita Zava per vedere il Code Interpreter in azione. Ecco alcune domande di follow-up che potresti voler provare:

    - ```Determina quali prodotti o categorie guidano le vendite. Mostra come Grafico a Barre.```
    - ```Quale sarebbe l'impatto di un evento shock (es., 20% di calo delle vendite in una regione) sulla distribuzione globale delle vendite? Mostra come Grafico a Barre Raggruppate.```
        - Fai seguito con ```E se l'evento shock fosse del 50%?```
    - ```Quali regioni hanno vendite sopra o sotto la media? Mostra come Grafico a Barre con Deviazione dalla Media.```
    - ```Quali regioni hanno sconti sopra o sotto la media? Mostra come Grafico a Barre con Deviazione dalla Media.```
    - ```Simula vendite future per regione usando una simulazione Monte Carlo per stimare intervalli di confidenza. Mostra come Linea con Bande di Confidenza usando colori vividi.```

<!-- ## Stop the Agent App

1. Switch back to the VS Code editor.
1. Press <kbd>Shift + F5</kbd> to stop the agent app. -->

## Lascia l'App Agente in Esecuzione

Lascia l'app agente in esecuzione poiché la userai nel prossimo lab per estendere l'agente con più strumenti e capacità.

*Tradotto utilizzando GitHub Copilot e GPT-4o.*
