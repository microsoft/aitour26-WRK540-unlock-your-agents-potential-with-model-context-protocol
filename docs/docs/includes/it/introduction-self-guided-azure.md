## Attendi il Completamento della Build del Codespace

Prima di procedere, assicurati che il tuo Codespace o Dev Container sia completamente costruito e pronto. Questo potrebbe richiedere diversi minuti, a seconda della tua connessione internet e delle risorse che vengono scaricate.

## Autentica con Azure

Autentica con Azure per permettere all'app agente di accedere al Servizio Agenti Azure AI e ai modelli. Segui questi passaggi:

1. Conferma che l'ambiente workshop sia pronto e aperto in VS Code.
2. Da VS Code, apri un terminale tramite **Terminal** > **New Terminal** in VS Code, poi esegui:

    ```shell
    az login --use-device-code
    ```

    !!! note
        Ti verrà chiesto di aprire un browser e accedere ad Azure. Copia il codice di autenticazione e:

        1. Scegli il tuo tipo di account e clicca **Next**.
        2. Accedi con le tue credenziali Azure.
        3. Incolla il codice.
        4. Clicca **OK**, poi **Done**.

    !!! warning
        Se hai multipli tenant Azure, specifica quello corretto usando:

        ```shell
        az login --use-device-code --tenant <tenant_id>
        ```

3. Successivamente, seleziona l'abbonamento appropriato dalla riga di comando.
4. Lascia la finestra del terminale aperta per i prossimi passaggi.

## Distribuisci le Risorse Azure

Questa distribuzione crea le seguenti risorse nel tuo abbonamento Azure sotto il gruppo di risorse **rg-zava-agent-wks-nnnn**:

- Un **hub Azure AI Foundry** chiamato **fdy-zava-agent-wks-nnnn**
- Un **progetto Azure AI Foundry** chiamato **prj-zava-agent-wks-nnnn**
- Due modelli sono distribuiti: **gpt-4o-mini** e **text-embedding-3-small**. [Vedi prezzi.](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/){:target="_blank"}

!!! warning "Assicurati di avere almeno 120K TPM quota per lo SKU gpt-4o-mini Global Standard, poiché l'agente fa frequenti chiamate al modello. Controlla la tua quota nel [Centro di Gestione AI Foundry](https://ai.azure.com/managementCenter/quota){:target="_blank"}."

Abbiamo fornito uno script bash per automatizzare la distribuzione delle risorse richieste per il workshop.

### Distribuzione Automatizzata

Lo script `deploy.sh` distribuisce le risorse nella regione `westus` per default. Per eseguire lo script:

```bash
cd infra && ./deploy.sh
```

<!-- !!! note "Su Windows, esegui `deploy.ps1` invece di `deploy.sh`" -->

### Configurazione Workshop

=== "Python"

    #### Configurazione Risorsa Azure

    Lo script di distribuzione genera il file **.env**, che contiene il progetto e gli endpoint del modello, i nomi di distribuzione del modello e la stringa di connessione Application Insights. Il file .env sarà automaticamente salvato nella cartella `src/python/workshop`. 
    
    Il tuo file **.env** apparirà simile al seguente, aggiornato con i tuoi valori:

    ```python
    PROJECT_ENDPOINT="<your_project_endpoint>"
    GPT_MODEL_DEPLOYMENT_NAME="<your_model_deployment_name>"
    EMBEDDING_MODEL_DEPLOYMENT_NAME="<your_embedding_model_deployment_name>"
    APPLICATIONINSIGHTS_CONNECTION_STRING="<your_application_insights_connection_string>"
    DEV_TUNNEL_URL="<your_dev_tunnel_url>"
    AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED="true"
    AZURE_OPENAI_ENDPOINT="<your_azure_openai_endpoint>"
    ```

    #### Nomi Risorse Azure

    Troverai anche un file chiamato `resources.txt` nella cartella `workshop`. Questo file contiene i nomi delle risorse Azure create durante la distribuzione. 

    Apparirà simile al seguente:

    ```plaintext
    Azure AI Foundry Resources:
    - Resource Group Name: rg-zava-agent-wks-nnnn
    - AI Project Name: prj-zava-agent-wks-nnnn
    - Foundry Resource Name: fdy-zava-agent-wks-nnnn
    - Application Insights Name: appi-zava-agent-wks-nnnn
    ```


=== "C#"

    Lo script memorizza in modo sicuro le variabili del progetto usando il Secret Manager per [i secrets di sviluppo ASP.NET Core](https://learn.microsoft.com/aspnet/core/security/app-secrets){:target="_blank"}.

    Puoi visualizzare i secrets eseguendo il seguente comando dopo aver aperto il workspace C# in VS Code:

    ```bash
    dotnet user-secrets list
    ```

*Tradotto utilizzando GitHub Copilot e GPT-4o.*
