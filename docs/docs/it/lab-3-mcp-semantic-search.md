## Cosa Imparerai

In questo lab, abiliti capacità di ricerca semantica nell'Agente Azure AI usando il Server MCP e il database PostgreSQL con l'estensione [PostgreSQL Vector](https://github.com/pgvector/pgvector){:target="\_blank"} abilitata.

## Introduzione

Questo lab aggiorna l'Agente Azure AI con ricerca semantica usando il Server MCP e PostgreSQL. 

Tutti i nomi e le descrizioni dei prodotti di Zava sono stati convertiti in vettori con il modello di embedding OpenAI (text-embedding-3-small) e memorizzati nel database. Questo permette all'agente di comprendere l'intento dell'utente e fornire risposte più accurate.

??? info "Per Sviluppatori: Come funziona la Ricerca Semantica PostgreSQL?"

    ### Vettorizzazione delle Descrizioni e Nomi Prodotti

    Per saperne di più su come i nomi e le descrizioni dei prodotti Zava sono stati vettorizzati, vedi il [README del Generatore Database PostgreSQL Zava DIY](https://github.com/microsoft/aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol/tree/main/data/database){:target="_blank"}.

    === "Python"

        ### L'LLM chiama lo Strumento Server MCP

        Basandosi sulla query dell'utente e sulle istruzioni fornite, l'LLM decide di chiamare lo strumento Server MCP `semantic_search_products` per trovare prodotti rilevanti.

        Succede la seguente sequenza di eventi:

        1. Lo strumento MCP `semantic_search_products` viene invocato con la descrizione della query dell'utente.
        1. Il server MCP genera un vettore per la query usando il modello di embedding OpenAI (text-embedding-3-small). Vedi il codice per vettorizzare la query nel metodo `generate_query_embedding`.
        1. Il server MCP esegue poi una ricerca semantica contro il database PostgreSQL per trovare prodotti con vettori simili.

        ### Panoramica Ricerca Semantica PostgreSQL

        Lo strumento Server MCP `semantic_search_products` esegue poi una query SQL che usa la query vettorizzata per trovare i vettori di prodotti più simili nel database. La query SQL usa l'operatore `<->` fornito dall'estensione pgvector per calcolare la distanza tra vettori.

        ```python
        async def search_products_by_similarity(
            self, query_embedding: list[float], 
                rls_user_id: str, 
                max_rows: int = 20, 
                similarity_threshold: float = 30.0
        ) -> str:
                ...
                query = f"""
                    SELECT 
                        p.*,
                        (pde.description_embedding <=> $1::vector) as similarity_distance
                    FROM {SCHEMA_NAME}.product_description_embeddings pde
                    JOIN {SCHEMA_NAME}.products p ON pde.product_id = p.product_id
                    WHERE (pde.description_embedding <=> $1::vector) <= $3
                    ORDER BY similarity_distance
                    LIMIT $2
                """

                rows = await conn.fetch(query, embedding_str, max_rows, distance_threshold)
                ...
        ```

    === "C#"

        ### L'LLM chiama lo Strumento Server MCP

        Basandosi sulla query dell'utente e sulle istruzioni fornite, l'LLM decide di chiamare lo strumento Server MCP `semantic_search_products` per trovare prodotti rilevanti.

        Succede la seguente sequenza di eventi:

        1. Lo strumento MCP `semantic_search_products` viene invocato con la descrizione della query dell'utente.
        2. Il server MCP genera un vettore per la query usando il modello di embedding OpenAI (text-embedding-3-small). Vedi il metodo `GenerateVectorAsync` nel file `EmbeddingGeneratorExtensions.cs`.
        3. Il server MCP esegue poi una ricerca semantica contro il database PostgreSQL per trovare prodotti con vettori simili.

        ### Panoramica Ricerca Semantica PostgreSQL

        Lo strumento Server MCP `semantic_search_products` esegue poi una query SQL che usa la query vettorizzata per trovare i vettori di prodotti più simili nel database. La query SQL usa l'operatore `<->` fornito dall'estensione pgvector per calcolare la distanza tra vettori.

        ```csharp
        public async Task<IEnumerable<SemanticSearchResult>> SemanticSearchProductsAsync(
        ...
            await using var searchCmd = new NpgsqlCommand("""
            SELECT 
                p.*,
                (pde.description_embedding <=> $1::vector) as similarity_distance
            FROM retail.product_description_embeddings pde
            JOIN retail.products p ON pde.product_id = p.product_id
            WHERE (pde.description_embedding <=> $1::vector) <= $3
            ORDER BY similarity_distance
            LIMIT $2
            """, connection);
            searchCmd.Parameters.AddWithValue(new Vector(embeddings));
            searchCmd.Parameters.AddWithValue(maxRows);
            searchCmd.Parameters.AddWithValue(distanceThreshold);

            await using var reader = await searchCmd.ExecuteReaderAsync();
            var results = new List<SemanticSearchResult>();
        ```

## Esercizio del Lab

Dal lab precedente puoi fare domande all'agente sui dati di vendita, ma era limitato a corrispondenze esatte. In questo lab, estendi le capacità dell'agente implementando la ricerca semantica usando il Model Context Protocol (MCP). Questo permetterà all'agente di comprendere e rispondere a query che non sono corrispondenze esatte, migliorando la sua capacità di assistere gli utenti con domande più complesse.

1. Incolla la seguente domanda nella scheda Web Chat nel tuo browser:

   ```text
   Che interruttori automatici da 18 amp vendiamo?
   ```

   L'agente risponde con qualcosa di simile a questo messaggio:

   _"Non sono riuscito a trovare interruttori automatici da 18 amp specifici nel nostro inventario. Tuttavia, potremmo avere altri tipi di interruttori automatici disponibili. Vorresti che cerchi interruttori automatici generici o altri prodotti correlati? 😊"_

## Ferma l'App Agente

Da VS Code, ferma l'app dell'agente premendo <kbd>Shift + F5</kbd>.

=== "Python"

    ## Implementa Ricerca Semantica

    In questa sezione, implementerai la ricerca semantica usando il Model Context Protocol (MCP) per migliorare le capacità dell'agente.

    1. Premi <kbd>F1</kbd> per **aprire** la Palette Comandi di VS Code.
    2. Digita **Open File** e seleziona **File: Open File...**.
    3. **Incolla** il seguente percorso nel selettore file e premi <kbd>Enter</kbd>:

        ```text
        /workspace/src/python/mcp_server/sales_analysis/sales_analysis.py
        ```

    4. Scorri fino alla riga 70 circa e cerca il metodo `semantic_search_products`. Questo metodo è responsabile per eseguire la ricerca semantica sui dati di vendita. Noterai che il decorator **@mcp.tool()** è commentato. Questo decorator è usato per registrare il metodo come strumento MCP, permettendo di essere chiamato dall'agente.

    5. Decommenta il decorator `@mcp.tool()` rimuovendo il `#` all'inizio della riga. Questo abiliterà lo strumento di ricerca semantica.

        ```python
        # @mcp.tool()
        async def semantic_search_products(
            ctx: Context,
            query_description: Annotated[str, Field(
            ...
        ```

    6. Successivamente, devi abilitare le istruzioni dell'Agente per usare lo strumento di ricerca semantica. Torna al file `app.py`.
    7. Scorri fino alla riga 30 circa e trova la riga `# INSTRUCTIONS_FILE = "instructions/mcp_server_tools_with_semantic_search.txt"`.
    8. Decommenta la riga rimuovendo il `#` all'inizio. Questo abiliterà l'agente a usare lo strumento di ricerca semantica.

        ```python
        INSTRUCTIONS_FILE = "instructions/mcp_server_tools_with_semantic_search.txt"
        ```

=== "C#"

    ## Implementa Ricerca Semantica

    In questa sezione, implementerai la ricerca semantica usando il Model Context Protocol (MCP) per migliorare le capacità dell'agente.

    1. Apri il file `McpHost.cs` dal progetto `McpAgentWorkshop.WorkshopApi`.
    1. Localizza dove gli altri strumenti MCP sono registrati con il server MCP, e registra la classe `SemanticSearchTools` come strumento MCP.

        ```csharp
        builder.Services.AddMcpTool<SemanticSearchTools>();
        ```

        !!! info "Nota"
            Leggi l'implementazione di `SemanticSearchTools` per imparare come il server MCP eseguirà la ricerca.

    1. Successivamente, devi abilitare le istruzioni dell'Agente per usare lo strumento di ricerca semantica. Torna alla classe `AgentService` e cambia la const `InstructionsFile` in `mcp_server_tools_with_semantic_search.txt`.

## Rivedi le Istruzioni dell'Agente

1. Premi <kbd>F1</kbd> per aprire la Palette Comandi di VS Code.
2. Digita **Open File** e seleziona **File: Open File...**.
3. Incolla il seguente percorso nel selettore file e premi <kbd>Enter</kbd>:

   ```text
   /workspace/src/shared/instructions/mcp_server_tools_with_semantic_search.txt
   ```

4. Rivedi le istruzioni nel file. Queste istruzioni istruiscono l'agente a usare lo strumento di ricerca semantica per rispondere a domande sui dati di vendita.

## Avvia l'App Agente con lo Strumento di Ricerca Semantica

1. **Avvia** l'app dell'agente premendo <kbd>F5</kbd>. Questo avvierà l'agente con le istruzioni aggiornate e lo strumento di ricerca semantica abilitato.
2. Apri la **Web Chat** nel tuo browser.
3. Inserisci la seguente domanda nella chat:

    ```text
    Che interruttori automatici da 18 amp vendiamo?
    ```

    L'agente ora comprende il significato semantico della domanda e risponde di conseguenza con dati di vendita rilevanti.

    !!! info "Nota"
        Lo strumento MCP Ricerca Semantica funziona come segue:

        1. La domanda viene convertita in un vettore usando lo stesso modello di embedding OpenAI (text-embedding-3-small) delle descrizioni dei prodotti.
        2. Questo vettore viene usato per cercare vettori di prodotti simili nel database PostgreSQL.
        3. L'agente riceve i risultati e li usa per generare una risposta.

## Scrivi un Report Esecutivo

Il prompt finale per questo workshop è il seguente:

```plaintext
Scrivi un report esecutivo sulle prestazioni di vendita dei diversi negozi per questi interruttori automatici.
```

## Lascia l'App Agente in Esecuzione

Lascia l'app dell'agente in esecuzione perché la userai nel prossimo lab per esplorare l'accesso sicuro ai dati dell'agente.

*Tradotto usando GitHub Copilot.*
