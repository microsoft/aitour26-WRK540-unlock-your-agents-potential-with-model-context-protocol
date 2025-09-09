## Introduzione

Il monitoraggio mantiene il tuo Servizio Agenti Azure AI Foundry disponibile, performante e affidabile. Azure Monitor raccoglie metriche e log, fornisce insight in tempo reale e invia avvisi. Usa dashboard e avvisi personalizzati per tracciare metriche chiave, analizzare tendenze e rispondere proattivamente. Accedi al monitoraggio tramite il portale Azure, CLI, REST API o librerie client.

## Esercizio del Lab

1. Dall'explorer file di VS Code, apri il file `resources.txt` nella cartella `workshop`.
1. **Copia** il valore per la chiave `AI Project Name` negli appunti.
1. Naviga alla pagina del [Portale Azure AI Foundry](https://ai.azure.com){:target="_blank"}.
1. Seleziona il tuo progetto dalla lista dei progetti foundry.

## Apri la dashboard di Monitoraggio

1. Dal file `resources.txt`, copia il valore per `Application Insights Name` negli appunti.
1. Torna al portale AI Foundry, seleziona la sezione **Monitoring** nel menu a sinistra.
1. Incolla il `Application Insights Name` copiato nel dropdown `Application Insights resource name`.
1. Seleziona la risorsa **Application Insights** dal dropdown.
1. Seleziona **Connect**.

### Esplora la dashboard di Monitoraggio

Familiarizza con le informazioni disponibili sulla dashboard `Application analytics`.

!!!tip "Puoi selezionare intervalli di date per filtrare i dati mostrati negli strumenti di monitoraggio."

![L'immagine mostra la dashboard di monitoraggio dell'applicazione](../media/monitor_usage.png)

### Monitora l'Uso delle Risorse

Puoi approfondire, seleziona `Resource Usage` per visualizzare metriche dettagliate sul consumo delle risorse del tuo Progetto AI. Anche qui puoi filtrare i dati per intervallo temporale.

![L'immagine mostra la dashboard di monitoraggio dell'uso delle risorse](../media/monitor_resource_usage.png)

*Tradotto usando GitHub Copilot.*
