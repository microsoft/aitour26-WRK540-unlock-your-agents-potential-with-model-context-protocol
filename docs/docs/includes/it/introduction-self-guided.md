## Studenti Autoguideati

Queste istruzioni sono per studenti autoguideati che non hanno accesso a un ambiente lab preconfigurato. Segui questi passaggi per configurare il tuo ambiente e iniziare il workshop.

## Introduzione

Questo workshop è progettato per insegnarti il Servizio Agenti Azure AI e l'SDK associato. È composto da più lab, ognuno che evidenzia una caratteristica specifica del Servizio Agenti Azure AI. I lab sono pensati per essere completati in ordine, poiché ognuno si basa sulla conoscenza e il lavoro del lab precedente.

## Prerequisiti

1. Accesso a una sottoscrizione Azure. Se non hai una sottoscrizione Azure, crea un [account gratuito](https://azure.microsoft.com/free/){:target="_blank"} prima di iniziare.
2. Hai bisogno di un account GitHub. Se non ne hai uno, crealo su [GitHub](https://github.com/join){:target="_blank"}.

## Selezionare il Linguaggio di Programmazione del Workshop

Il workshop è disponibile sia in Python che in C#. Usa le schede del selettore di linguaggio per scegliere il tuo linguaggio preferito. Nota, non cambiare linguaggio a metà workshop.

**Seleziona la scheda per il tuo linguaggio preferito:**

=== "Python"
    Il linguaggio predefinito per il workshop è impostato su **Python**.
=== "C#"
    Il linguaggio predefinito per il workshop è impostato su **C#**.

    !!! warning "La versione C#/.NET di questo workshop è in beta e ha problemi di stabilità noti."

    Assicurati di leggere la sezione della [guida alla risoluzione dei problemi](../../en/dotnet-troubleshooting.md) **PRIMA** di iniziare il workshop. Altrimenti, seleziona la versione **Python** del workshop.

## Aprire il Workshop

Preferito: **GitHub Codespaces**, che fornisce un ambiente preconfigurato con tutti gli strumenti richiesti. In alternativa, esegui localmente con un **Dev Container** di Visual Studio Code e **Docker**. Usa le schede sottostanti per scegliere.

!!! Tip
    La costruzione di Codespaces o Dev Container richiede circa 5 minuti. Avvia la costruzione, poi **continua a leggere** mentre si completa.

=== "GitHub Codespaces"

    Seleziona **Open in GitHub Codespaces** per aprire il progetto in GitHub Codespaces.

    [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/microsoft/aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol){:target="_blank"}

=== "VS Code Dev Container"

    1. Assicurati di avere quanto segue installato sulla tua macchina locale:

        - [Docker](https://docs.docker.com/get-docker/){:target="\_blank"}
        - [Visual Studio Code](https://code.visualstudio.com/download){:target="\_blank"}
        - L'estensione [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers){:target="\_blank"}
    2. Clona il repository sulla tua macchina locale:

        ```bash
        git clone https://github.com/microsoft/aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol.git
        ```

    3. Apri il repository clonato in Visual Studio Code.
    4. Quando richiesto, seleziona **Reopen in Container** per aprire il progetto in un Dev Container.

---

## Autenticare i Servizi Azure

!!! danger
Prima di procedere, assicurati che il tuo Codespace o Dev Container sia completamente costruito e pronto.

### Autenticazione con DevTunnel

DevTunnel fornisce un servizio di port forwarding che verrà utilizzato nel workshop per consentire al Servizio Agenti Azure AI di accedere al Server MCP che eseguirai nel tuo ambiente di sviluppo locale. Segui questi passaggi per autenticarti:

1. Da VS Code, **premi** <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>`</kbd> per aprire una nuova finestra terminale. Quindi esegui il seguente comando:
2. **Esegui il seguente comando** per autenticarti con DevTunnel:

   ```shell
   devtunnel login
   ```

3. Segui questi passaggi per autenticarti:

   1. Copia il **Codice di Autenticazione** negli appunti.
   2. **Tieni premuto** il tasto <kbd>ctrl</kbd> o <kbd>cmd</kbd>.
   3. **Seleziona** l'URL di autenticazione per aprirlo nel tuo browser.
   4. **Incolla** il codice e clicca **Avanti**.
   5. **Scegli un account** e accedi.
   6. Seleziona **Continua**
   7. **Torna** alla finestra terminale in VS Code.

4. Lascia la finestra terminale **aperta** per i prossimi passaggi.

### Autenticazione con Azure

Autenticati con Azure per consentire all'app agent di accedere al Servizio Agenti Azure AI e ai modelli. Segui questi passaggi:

1. Quindi esegui il seguente comando:

    ```shell
    az login --use-device-code
    ```

    !!! warning
    Se hai più tenant Azure, specifica quello corretto usando:

    ```shell
    az login --use-device-code --tenant <tenant_id>
    ```

2. Segui questi passaggi per autenticarti:

    1. **Copia** il **Codice di Autenticazione** negli appunti.
    2. **Tieni premuto** il tasto <kbd>ctrl</kbd> o <kbd>cmd</kbd>.
    3. **Seleziona** l'URL di autenticazione per aprirlo nel tuo browser.
    4. **Incolla** il codice e clicca **Avanti**.
    5. **Scegli un account** e accedi.
    6. Seleziona **Continua**
    7. **Torna** alla finestra terminale in VS Code.
    8. Se richiesto, **seleziona** una sottoscrizione.

3. Lascia aperta la finestra terminale per i prossimi passaggi.

---

## Distribuire le Risorse Azure

Questa distribuzione crea le seguenti risorse nella tua sottoscrizione Azure.

- Un gruppo di risorse chiamato **rg-zava-agent-wks-nnnnnnnn**
- Un **hub Azure AI Foundry** chiamato **fdy-zava-agent-wks-nnnnnnnn**
- Un **progetto Azure AI Foundry** chiamato **prj-zava-agent-wks-nnnnnnnn**
- Due modelli sono distribuiti: **gpt-4o-mini** e **text-embedding-3-small**. [Vedi prezzi.](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/){:target="\_blank"}
- Risorsa Application Insights chiamata **appi-zava-agent-wks-nnnnnnnn**. [Vedi prezzi](https://azure.microsoft.com/pricing/calculator/?service=monitor){:target="\_blank"}
- Per mantenere bassi i costi del workshop, PostgreSQL funziona in un container locale all'interno del tuo Codespace o Dev Container piuttosto che come servizio cloud. Vedi [Azure Database for PostgreSQL Flexible Server](https://azure.microsoft.com/en-us/products/postgresql){:target="\_blank"} per saperne di più sulle opzioni per un servizio PostgreSQL gestito.

!!! warning "Assicurati di avere almeno le seguenti quote di modelli" - 120K TPM di quota per il SKU gpt-4o-mini Global Standard, poiché l'agent effettua frequenti chiamate al modello. - 50K TPM per il modello text-embedding-3-small Global Standard SKU. - Controlla la tua quota nel [Centro di Gestione AI Foundry](https://ai.azure.com/managementCenter/quota){:target="\_blank"}."

### Distribuzione Automatizzata

Esegui il seguente script bash per automatizzare la distribuzione delle risorse richieste per il workshop. Lo script `deploy.sh` distribuisce le risorse nella regione `westus` per default. Per eseguire lo script:

```bash
cd infra && ./deploy.sh
```

### Configurazione del Workshop

=== "Python"

    #### Configurazione Risorse Azure

    Lo script di distribuzione genera il file **.env**, che contiene gli endpoint del progetto e del modello, i nomi dei deployment del modello e la stringa di connessione di Application Insights. Il file .env verrà salvato automaticamente nella cartella `src/python/workshop`.

    Il tuo file **.env** sembrerà simile al seguente, aggiornato con i tuoi valori:

    ```python
    PROJECT_ENDPOINT="<your_project_endpoint>"
    GPT_MODEL_DEPLOYMENT_NAME="<your_model_deployment_name>"
    EMBEDDING_MODEL_DEPLOYMENT_NAME="<your_embedding_model_deployment_name>"
    APPLICATIONINSIGHTS_CONNECTION_STRING="<your_application_insights_connection_string>"
    AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED="true"
    AZURE_OPENAI_ENDPOINT="<your_azure_openai_endpoint>"
    ```

    #### Nomi delle Risorse Azure

    Troverai anche un file chiamato `resources.txt` nella cartella `workshop`. Questo file contiene i nomi delle risorse Azure create durante la distribuzione.

    Assomiglierà al seguente:

    ```plaintext
    Azure AI Foundry Resources:
    - Resource Group Name: rg-zava-agent-wks-nnnnnnnn
    - AI Project Name: prj-zava-agent-wks-nnnnnnnn
    - Foundry Resource Name: fdy-zava-agent-wks-nnnnnnnn
    - Application Insights Name: appi-zava-agent-wks-nnnnnnnn
    ```

=== "C#"

    Lo script memorizza in modo sicuro le variabili del progetto utilizzando il Secret Manager per i [segreti di sviluppo ASP.NET Core](https://learn.microsoft.com/aspnet/core/security/app-secrets){:target="_blank"}.

    Puoi visualizzare i segreti eseguendo il seguente comando dopo aver aperto il workspace C# in VS Code:

    ```bash
    dotnet user-secrets list
    ```

---

## Aprire il Workspace di VS Code

Ci sono due workspace di VS Code nel workshop, uno per Python e uno per C#. Il workspace contiene il codice sorgente e tutti i file necessari per completare i lab per ogni linguaggio. Scegli il workspace che corrisponde al linguaggio con cui vuoi lavorare.

=== "Python"

    1. **Copia** il seguente percorso negli appunti:

        ```text
        /workspace/.vscode/python-workspace.code-workspace
        ```
    2. Dal menu di VS Code, seleziona **File** quindi **Open Workspace from File**.
    3. Sostituisci e **incolla** il nome del percorso copiato e seleziona **OK**.


    ## Struttura del Progetto

    Familiarizza con le **cartelle** e i **file** chiave del workspace con cui lavorerai durante tutto il workshop.

    ### La cartella "workshop"

    - Il file **app.py**: Il punto di ingresso per l'app, contenente la sua logica principale.

    Nota la variabile **INSTRUCTIONS_FILE**—imposta quale file di istruzioni usa l'agent. Aggiornerai questa variabile in un lab successivo.

    - Il file **resources.txt**: Contiene le risorse utilizzate dall'app agent.
    - Il file **.env**: Contiene le variabili d'ambiente utilizzate dall'app agent.

    ### La cartella "mcp_server"

    - Il file **sales_analysis.py**: Il Server MCP con strumenti per l'analisi delle vendite.

    ### La cartella "shared/instructions"

    - La cartella **instructions**: Contiene le istruzioni passate all'LLM.

    ![Struttura delle cartelle del lab](../../media/project-structure-self-guided-python.png)

=== "C#"

    1. In Visual Studio Code, vai a **File** > **Open Workspace from File**.
    2. Sostituisci il percorso predefinito con il seguente:

        ```text
        /workspace/.vscode/csharp-workspace.code-workspace
        ```

    3. Seleziona **OK** per aprire il workspace.

    ## Struttura del Progetto

    Il progetto utilizza [Aspire](http://aka.ms/dotnet-aspire) per semplificare la costruzione dell'applicazione agent, gestire il server MCP e orchestrare tutte le dipendenze esterne. La solution è composta da quattro progetti, tutti con il prefisso `McpAgentWorkshop`:

    * `AppHost`: L'orchestratore Aspire e progetto di avvio per il workshop.
    * `McpServer`: Il progetto del server MCP.
    * `ServiceDefaults`: Configurazione predefinita per i servizi, come logging e telemetria.
    * `WorkshopApi`: L'API Agent per il workshop. La logica dell'applicazione principale è nella classe `AgentService`.

    Oltre ai progetti .NET nella solution, c'è una cartella `shared` (visibile come Solution Folder e tramite il file explorer), che contiene:

    * `instructions`: Le istruzioni passate all'LLM.
    * `scripts`: Script shell helper per varie attività, verranno riferiti quando necessario.
    * `webapp`: L'applicazione client front-end. Nota: Questa è un'applicazione Python, di cui Aspire gestirà il ciclo di vita.

    ![Struttura delle cartelle del lab](../../media/project-structure-self-guided-csharp.png)
