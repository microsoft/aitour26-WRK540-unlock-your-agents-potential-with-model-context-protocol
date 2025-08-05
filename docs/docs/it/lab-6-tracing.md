**TBC: Questa etichetta farà sì che l'utente aggiorni il file delle istruzioni dell'agente per rimuovere gli emoji fastidiosi che l'agente usa nelle sue risposte.**

## Introduzione

Il tracing ti aiuta a comprendere e fare debug del comportamento del tuo agente mostrando la sequenza di passaggi, input e output durante l'esecuzione. In Azure AI Foundry, il tracing ti permette di osservare come il tuo agente elabora le richieste, chiama strumenti e genera risposte. Puoi usare il portale Azure AI Foundry o integrare con OpenTelemetry e Application Insights per raccogliere e analizzare dati di trace, rendendo più facile il troubleshooting e l'ottimizzazione del tuo agente.

<!-- ## Lab Exercise

=== "Python"

      1. Open the `app.py` file.
      2. Change the `AZURE_TELEMETRY_ENABLED` variable to `True` to enable tracing:

         ```python
         AZURE_TELEMETRY_ENABLED = True
         ```

        !!! info "Note"
            This setting enables telemetry for your agent. In the `initialize` function in `app.py`, the telemetry client is configured to send data to Azure Monitor.

            ```python
             if AZURE_TELEMETRY_ENABLED:
                 configure_azure_monitor(connection_string=await self.project_client.telemetry.get_connection_string())
            ```         

=== "C#"

      tbd -->

## Esegui l'App Agente

1. Premi <kbd>F5</kbd> per eseguire l'app.
2. Seleziona **Preview in Editor** per aprire l'app agente in una nuova scheda dell'editor.

### Avvia una Conversazione con l'Agente

Copia e incolla il seguente prompt nell'app agente per iniziare una conversazione:

```plaintext
Scrivi un rapporto esecutivo che analizza le prime 5 categorie di prodotti e confronta le prestazioni del negozio online rispetto alla media dei negozi fisici.
```

## Visualizza Traces

Puoi visualizzare le trace dell'esecuzione del tuo agente nel portale Azure AI Foundry o usando OpenTelemetry. Le trace mostreranno la sequenza di passaggi, chiamate di strumenti e dati scambiati durante l'esecuzione dell'agente. Queste informazioni sono cruciali per il debug e l'ottimizzazione delle prestazioni del tuo agente.

### Usando il Portale Azure AI Foundry

Per visualizzare le trace nel portale Azure AI Foundry, segui questi passaggi:

1. Naviga al portale **[Azure AI Foundry](https://ai.azure.com/)**.
2. Seleziona il tuo progetto.
3. Seleziona la scheda **Tracing** nel menu di sinistra.
4. Qui, puoi vedere le trace generate dal tuo agente.

   ![](media/ai-foundry-tracing.png)

### Approfondimento delle Trace

1. Potresti dover cliccare sul pulsante **Refresh** per vedere le trace più recenti poiché le trace potrebbero impiegare alcuni momenti per apparire.
2. Seleziona la trace chiamata `Zava Agent Initialization` per visualizzare i dettagli.
   ![](media/ai-foundry-trace-agent-init.png)
3. Seleziona la trace `creare_agent Zava DIY Sales Agent` per visualizzare i dettagli del processo di creazione dell'agente. Nella sezione `Input & outputs`, vedrai le istruzioni dell'Agente.
4. Successivamente, seleziona la trace `Zava Agent Chat Request: Write an executive...` per visualizzare i dettagli della richiesta di chat. Nella sezione `Input & outputs`, vedrai l'input dell'utente e la risposta dell'agente.

<!-- https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/continuous-evaluation-agents -->

*Tradotto utilizzando GitHub Copilot e GPT-4o.*
