## Cosa Imparerai

In questo lab, abiliti le capacità di ricerca semantica nell'Agente Azure AI usando il Model Context Protocol (MCP) e il database PostgreSQL.

## Introduzione

Questo lab aggiorna l'Agente Azure AI con ricerca semantica usando Model Context Protocol (MCP) e PostgreSQL. I nomi e le descrizioni dei prodotti sono stati convertiti in vettori con il modello di embedding OpenAI (text-embedding-3-small) e memorizzati nel database. Questo consente all'agente di comprendere l'intento dell'utente e fornire risposte più accurate.

## Esercizio del Lab

Dal lab precedente puoi fare domande all'agente sui dati di vendita, ma era limitato a corrispondenze esatte. In questo lab, estendi le capacità dell'agente implementando la ricerca semantica usando il Model Context Protocol (MCP). Questo permetterà all'agente di comprendere e rispondere a query che non sono corrispondenze esatte, migliorando la sua capacità di assistere gli utenti con domande più complesse.

1. Incolla la seguente domanda nella scheda Web Chat nel tuo browser:

    ```text
    Come hanno performato i diversi negozi con interruttori 18A?
    ```

    L'agente risponde: "Non sono riuscito a trovare dati di vendita per interruttori 18A nei nostri record. 😱 Tuttavia, ecco alcuni suggerimenti per prodotti simili che potresti voler esplorare." Questo accade perché l'agente si basa solo sulla corrispondenza di query per parole chiave e non comprende il significato semantico della tua domanda. Il LLM potrebbe comunque fare suggerimenti di prodotti educati da qualsiasi contesto di prodotto che potrebbe già avere.

## Implementa Ricerca Semantica

In questa sezione, implementerai la ricerca semantica usando il Model Context Protocol (MCP) per migliorare le capacità dell'agente.

1. Premi <kbd>F1</kbd> per **aprire** la Command Palette di VS Code.
2. Digita **Open File** e seleziona **File: Open File...**.
3. **Incolla** il seguente percorso nel selettore file e premi <kbd>Enter</kbd>:

    ```text
    /workspace/src/python/mcp_server/sales_analysis/sales_analysis.py
    ```

4. Scorri verso il basso fino alla riga 100 circa e cerca il metodo `semantic_search_products`. Questo metodo è responsabile di eseguire la ricerca semantica sui dati di vendita. Noterai che il decoratore **@mcp.tool()** è commentato. Questo decoratore è usato per registrare il metodo come strumento MCP, permettendo che sia chiamato dall'agente.

5. Decommenta il decoratore `@mcp.tool()` rimuovendo il `#` all'inizio della riga. Questo abiliterà lo strumento di ricerca semantica.

    ```python
    # @mcp.tool()
    async def semantic_search_products(
        ctx: Context,
        query_description: Annotated[str, Field(
        ...
    ```

6. Successivamente, devi abilitare le istruzioni dell'Agente per usare lo strumento di ricerca semantica. Torna al file `app.py`.
7. Scorri verso il basso fino alla riga 30 circa e trova la riga `# INSTRUCTIONS_FILE = "instructions/mcp_server_tools_with_semantic_search.txt".
8. Decommenta la riga rimuovendo il `#` all'inizio. Questo abiliterà l'agente a usare lo strumento di ricerca semantica.

    ```python
    INSTRUCTIONS_FILE = "instructions/mcp_server_tools_with_semantic_search.txt"
    ```

## Rivedi le Istruzioni dell'Agente

1. Premi <kbd>F1</kbd> per aprire la Command Palette di VS Code.
2. Digita **Open File** e seleziona **File: Open File...**.
3. Incolla il seguente percorso nel selettore file e premi <kbd>Enter</kbd>:

    ```text
    /workspace/src/shared/instructions/mcp_server_tools_with_semantic_search.txt
    ```

4. Rivedi le istruzioni nel file. Queste istruzioni istruiscono l'agente a usare lo strumento di ricerca semantica per rispondere a domande sui dati di vendita.

## Avvia l'App Agente con lo Strumento di Ricerca Semantica

1. **Ferma** l'app agente corrente premendo <kbd>Shift + F5</kbd>.
2. **Riavvia** l'app agente premendo <kbd>F5</kbd>. Questo avvierà l'agente con le istruzioni aggiornate e lo strumento di ricerca semantica abilitato.
3. Torna alla scheda **Web Chat** nel tuo browser.
4. Inserisci la seguente domanda nella chat:

    ```text
    Come hanno performato i diversi negozi con interruttori 18A?
    ```

    L'agente ora comprende il significato semantico della domanda e risponde di conseguenza con dati di vendita rilevanti.

    !!! info "Nota"
        Lo strumento MCP Semantic Search funziona come segue:

        1. La domanda è convertita in un vettore usando lo stesso modello di embedding OpenAI (text-embedding-3-small) delle descrizioni dei prodotti.
        2. Questo vettore è usato per cercare vettori di prodotto simili nel database PostgreSQL.
        3. L'agente riceve i risultati e li usa per generare una risposta.

*Tradotto utilizzando GitHub Copilot e GPT-4o.*
