## Introduzione

Il tracciamento ti aiuta a comprendere e debuggare il comportamento del tuo agente mostrando la sequenza di passi, input e output durante l'esecuzione. In Azure AI Foundry, il tracciamento ti permette di osservare come il tuo agente elabora le richieste, chiama strumenti e genera risposte. Puoi usare il portale Azure AI Foundry o integrare con OpenTelemetry e Application Insights per raccogliere e analizzare i dati di tracciamento, rendendo più facile il troubleshooting e l'ottimizzazione del tuo agente.

<!-- ## Esercizio del Lab

=== "Python"

      1. Apri il file `app.py`.
      2. Cambia la variabile `AZURE_TELEMETRY_ENABLED` a `True` per abilitare il tracciamento:

         ```python
         AZURE_TELEMETRY_ENABLED = True
         ```

        !!! info "Nota"
            Questa impostazione abilita la telemetria per il tuo agente. Nella funzione `initialize` in `app.py`, il client di telemetria è configurato per inviare dati ad Azure Monitor.

            ```python
             if AZURE_TELEMETRY_ENABLED:
                 configure_azure_monitor(connection_string=await self.project_client.telemetry.get_connection_string())
            ```         

=== "C#"

      da fare -->

<!-- ## Esegui l'App Agente

1. Premi <kbd>F5</kbd> per eseguire l'app.
2. Seleziona **Preview in Editor** per aprire l'app dell'agente in una nuova scheda dell'editor.

### Inizia una Conversazione con l'Agente

Copia e incolla il seguente prompt nell'app dell'agente per iniziare una conversazione:

```plaintext
Scrivi un report esecutivo che analizza le prime 5 categorie di prodotti e confronta le performance del negozio online versus la media dei negozi fisici.
``` -->

## Visualizza Tracce

Puoi visualizzare le tracce dell'esecuzione del tuo agente nel portale Azure AI Foundry o usando OpenTelemetry. Le tracce mostreranno la sequenza di passi, chiamate agli strumenti e dati scambiati durante l'esecuzione dell'agente. Queste informazioni sono cruciali per il debug e l'ottimizzazione delle performance del tuo agente.

### Usando il Portale Azure AI Foundry

Per visualizzare le tracce nel portale Azure AI Foundry, segui questi passi:

1. Naviga al portale [Azure AI Foundry](https://ai.azure.com/).
2. Seleziona il tuo progetto.
3. Seleziona la scheda **Tracing** nel menu a sinistra.
4. Qui puoi vedere le tracce generate dal tuo agente.

   ![](media/ai-foundry-tracing.png)

### Approfondire le Tracce

1. Potresti dover cliccare sul pulsante **Refresh** per vedere le tracce più recenti poiché le tracce potrebbero impiegare qualche momento per apparire.
2. Seleziona la traccia chiamata `Zava Agent Initialization` per visualizzare i dettagli.
   ![](media/ai-foundry-trace-agent-init.png)
3. Seleziona la traccia `create_agent Zava DIY Sales Agent` per visualizzare i dettagli del processo di creazione dell'agente. Nella sezione `Input & outputs`, vedrai le istruzioni dell'Agente.
4. Successivamente, seleziona la traccia `Zava Agent Chat Request: Write an executive...` per visualizzare i dettagli della richiesta chat. Nella sezione `Input & outputs`, vedrai l'input dell'utente e la risposta dell'agente.

<!-- https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/continuous-evaluation-agents -->

*Tradotto usando GitHub Copilot.*
