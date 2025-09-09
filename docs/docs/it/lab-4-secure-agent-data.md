## Cosa Imparerai

In questo lab, proteggerai i dati dell'agente usando il Model Context Protocol (MCP) e PostgreSQL Row Level Security (RLS). L'agente ha accesso di sola lettura al database e i dati sono protetti da ruoli utente (sede centrale e store manager) per assicurare che solo utenti autorizzati possano accedere a informazioni specifiche.

## Introduzione

Il database PostgreSQL usa Row Level Security (RLS) per controllare l'accesso ai dati per ruolo utente. Il client web chat predefinito al ruolo `Sede centrale` (accesso completo ai dati), ma passare al ruolo `Store Manager` limita l'accesso solo ai dati specifici del ruolo.

Il Server MCP fornisce all'agente l'accesso al database Zava. Quando il servizio agenti elabora le richieste degli utenti, il ruolo utente (UUID) viene passato al server MCP tramite MCP Tools Resource Headers per assicurare che la sicurezza basata sui ruoli sia applicata.

In operazioni normali, uno store manager si autenticherebbe con l'agente e il suo ruolo utente sarebbe impostato di conseguenza. Ma questo è un workshop, e selezioneremo manualmente un ruolo.

??? info "Per Sviluppatori: Come funziona PostgreSQL Row Level Security?"

    ### Panoramica Sicurezza PostgreSQL RLS

    Row Level Security (RLS) filtra automaticamente le righe del database basandosi sui permessi utente. Questo permette a più utenti di condividere le stesse tabelle del database vedendo solo i dati che sono autorizzati ad accedere. 
    
    In questo sistema, gli utenti della sede centrale vedono tutti i dati di tutti i negozi, mentre gli store manager sono limitati a visualizzare solo le informazioni del proprio negozio. L'esempio sotto mostra come le policy RLS sono implementate per la tabella `retail.orders`, con policy identiche applicate alle tabelle `retail.order_items`, `retail.inventory`, e `retail.customers`.

    ```sql
    CREATE POLICY store_manager_orders ON retail.orders
    FOR ALL TO PUBLIC
    USING (
        -- La sede centrale vede tutti i dati
        current_setting('app.current_rls_user_id', true) = '00000000-0000-0000-0000-000000000000'
        OR
        -- Gli store manager vedono solo i dati del loro negozio
        EXISTS (SELECT 1 FROM retail.stores s WHERE s.store_id = retail.orders.store_id 
                AND s.rls_user_id::text = current_setting('app.current_rls_user_id', true))
    );
    ```

    **Risultato:** Gli store manager vedono solo i dati del loro negozio, mentre la sede centrale vede tutto - tutto usando lo stesso database e tabelle.

    === "Python"

        Troverai il codice responsabile per impostare il ruolo utente nel file `workshop/chat_manager.py`.

        ```python
        if request.rls_user_id:
            # Crea risorse strumenti dinamiche con header RLS user ID
            mcp_tool_resource = MCPToolResource(
                server_label="ZavaSalesAnalysisMcpServer",
                headers={"x-rls-user-id": request.rls_user_id},
                require_approval="never",
            )
            tool_resources.mcp = [mcp_tool_resource]
        ```

        Il codice per recuperare l'RLS User ID è in `mcp_server/sales_analysis/sales_analysis.py`. Se il server non rileva l'header RLS, predefinisce al ruolo Sede Centrale. Questo fallback è inteso solo per l'uso del workshop e non dovrebbe essere applicato in produzione.

        ```python
        def get_rls_user_id(ctx: Context) -> str:
            """Ottiene l'ID Utente Row Level Security dal contesto della richiesta."""

            rls_user_id = get_header(ctx, "x-rls-user-id")
            if rls_user_id is None:
                # Predefinisce a un placeholder se non fornito
                rls_user_id = "00000000-0000-0000-0000-000000000000"
            return rls_user_id
        ```

    === "C#"

        Troverai il codice responsabile per impostare il ruolo utente sulle richieste al Server MCP nella classe `AgentService`.

        ```csharp
        var mcpToolResource = new MCPToolResource(ZavaMcpToolLabel, new Dictionary<string, string>
        {
            { "x-rls-user-id", request.RlsUserId }
        });
        var toolResources = new ToolResources();
        toolResources.Mcp.Add(mcpToolResource);
        ```

        Il `MCPToolResource` viene poi aggiunto alla collezione `ToolResources`, che viene fornita al run streaming usando la proprietà `CreateRunStreamingOptions.ToolResources`, questo perché l'RLS user ID è un valore dinamico dal client (diversi utenti "loggati" possono avere ID diversi), dobbiamo assicurarci che sia impostato sul _run_ del thread piuttosto che quando l'agente viene creato.

        Poiché l'RLS user ID è impostato come header per l'agente da inoltrare al Server MCP, questo è accessibile dall'`HttpContext` sulla richiesta, che può essere accessibile da un `IHttpContextAccessor`, che viene iniettato nei metodi degli strumenti MCP. È stato creato un metodo di estensione, `HttpContextAccessorExtensions.GetRequestUserId`, che può essere usato all'interno di uno strumento:

        ```csharp
        public async Task<string> ExecuteSalesQueryAsync(
            NpgsqlConnection connection,
            ILogger<SalesTools> logger,
            IHttpContextAccessor httpContextAccessor,
            [Description("Una query PostgreSQL ben formata.")] string query
        )
        {
            ...

            var rlsUserId = httpContextAccessor.GetRequestUserId();

            ...
        }
        ```

    ### Impostazione dell'ID Utente Postgres RLS

    Ora che il Server MCP ha l'RLS User ID, deve essere impostato sulla connessione PostgreSQL.

    === "Python"

        La soluzione Python imposta l'RLS User ID su ogni connessione PostgreSQL chiamando `set_config()` all'interno del metodo `execute_query` in `mcp_server/sales_analysis/sales_analysis_postgres.py`.

        ```python
        ...
        conn = await self.get_connection()
        await conn.execute("SELECT set_config('app.current_rls_user_id', $1, false)", rls_user_id)

        rows = await conn.fetch(sql_query)
        ...
        ```

    === "C#"

        La soluzione C# imposta l'RLS User ID sulla connessione PostgreSQL eseguendo un comando SQL per impostare la variabile di contesto RLS immediatamente dopo l'apertura della connessione nel metodo `ExecuteSalesQueryAsync` in `SalesTools.cs`.

        ```csharp
        ...
        await using var cmd = new NpgsqlCommand("SELECT set_config('app.current_rls_user_id', @rlsUserId, false)", connection);
        cmd.Parameters.AddWithValue("rlsUserId", rlsUserId ?? string.Empty);
        await cmd.ExecuteNonQueryAsync();

        await using var queryCmd = new NpgsqlCommand(query, connection);
        await using var reader = await queryCmd.ExecuteReaderAsync();
        ...
        ```

## Esercizio del Lab

### Ruolo Sede Centrale

Per impostazione predefinita, il client web opera con il ruolo `Sede Centrale`, che ha accesso completo a tutti i dati.

1. Inserisci la seguente query nella chat:

   ```text
   Mostra vendite per negozio
   ```

   Vedrai che vengono restituiti i dati per tutti i negozi. Perfetto.

### Seleziona un Ruolo Store Manager

1. Torna alla scheda Web Chat degli Agenti nel tuo browser.
2. Seleziona l'icona `impostazioni` nell'angolo in alto a destra della pagina.
3. Seleziona una `Posizione negozio` dal menu a discesa.
4. Seleziona `Salva` e ora l'agente opererà con i permessi di accesso ai dati della posizione negozio selezionata.

   ![](../media/select_store_manager_role.png)

Ora l'agente avrà accesso solo ai dati per la posizione negozio selezionata.

!!! info "Nota"
    Cambiare l'utente resetterà la sessione di chat, poiché il contesto è legato all'utente.

Prova la seguente query:

```text
Mostra vendite per negozio
```

Noterai che l'agente restituisce solo dati per la posizione negozio selezionata. Questo dimostra come l'accesso ai dati dell'agente è limitato basandosi sul ruolo store manager selezionato.

![](../media/select_seattle_store_role.png)

*Tradotto usando GitHub Copilot.*
