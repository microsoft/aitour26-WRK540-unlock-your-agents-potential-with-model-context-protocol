## Introduzione

!!! note "Il tracing con la Dashboard di Aspire è supportato solo nella versione C# del workshop."

Fino ad ora per il nostro tracing, ci siamo concentrati su come visualizzare questo tramite le dashboard di Azure AI Foundry, che può essere un'interruzione nel flusso di lavoro quando si sviluppa localmente. Inoltre, possiamo sfruttare la Dashboard di Aspire per visualizzare le tracce generate dalla nostra applicazione in tempo reale e come un'azione si estende attraverso più risorse all'interno del nostro sistema.

## Eseguire l'App Agent

Lancia l'applicazione premendo <kbd>F5</kbd> e attendi che la Dashboard di Aspire appaia nel tuo browser. Questo mostrerà un elenco completo delle risorse nel workshop.

![Dashboard di Aspire](../media/lab-7-dashboard.png)

Come nei passaggi precedenti del lab, apri il **Workshop Frontend** e inserisci un prompt nella chat, come:

```plaintext
Scrivi un report esecutivo che analizza le prime 5 categorie di prodotti e confronta le prestazioni del negozio online rispetto alla media dei negozi fisici.
```

## Visualizzazione delle Tracce

Per visualizzare le tracce generate dalla tua applicazione, naviga alla scheda **Traces** nella Dashboard di Aspire. Qui puoi vedere un elenco di tutte le tracce che sono state catturate, iniziando con il loro iniziatore.

![Panoramica delle tracce](../media/lab-7-trace-overview.png)

L'ultima voce nello screenshot sopra mostra l'evento dal **dotnet-front-end** che esegue un `GET` a `/chat/stream`. La colonna **Span** mostra poi le risorse attraverso cui questa traccia si estende: `dotnet-front-end`, `dotnet-agent-app`, `ai-foundry`, `dotnet-mcp-server` e `pg`.

Ogni risorsa ha un numero associato, che è il numero di _span_ che sono occorsi per quella risorsa. Possiamo anche notare un indicatore di errore sulle risorse `dotnet-mcp-server` e `pg`, che indicherebbe che si è verificato un errore su quelle risorse.

Cliccando sulla traccia ti mostrerà una vista dettagliata della timeline della traccia:

![Timeline della traccia](../media/lab-7-trace-timeline.png)

Da qui, possiamo visualizzare i singoli span, l'ordine in cui sono occorsi, la loro durata e come gli eventi sono accaduti attraverso le risorse all'interno della nostra applicazione.

Cliccando su un singolo span ti mostrerà maggiori dettagli su quello specifico span:

![Dettagli dello span](../media/lab-7-span-details.png)

Prova a sperimentare con prompt diversi e a simulare errori, per osservare come le tracce cambiano nella Dashboard di Aspire.

## Letture Aggiuntive

- [Documentazione di Aspire](https://aka.ms/aspire-docs)
- [Documentazione di Telemetria di Aspire](https://learn.microsoft.com/dotnet/aspire/fundamentals/telemetry)
