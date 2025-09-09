## Partecipanti all'Evento Microsoft

Le istruzioni in questa pagina presuppongono che tu stia partecipando all'[Evento Microsoft 2025](https://build.microsoft.com/){:target="_blank"} e abbia accesso a un ambiente lab preconfigurato. Questo ambiente fornisce una sottoscrizione Azure con tutti gli strumenti e le risorse necessari per completare il workshop.

## Introduzione

Questo workshop è progettato per insegnarti il Servizio Agenti Azure AI e l'[SDK](https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme?context=%2Fazure%2Fai-services%2Fagents%2Fcontext%2Fcontext){:target="_blank"} associato. È composto da più lab, ognuno che evidenzia una caratteristica specifica del Servizio Agenti Azure AI. I lab sono pensati per essere completati in ordine, poiché ognuno si basa sulla conoscenza e il lavoro del lab precedente.

## Selezionare il Linguaggio di Programmazione del Workshop

Il workshop è disponibile sia in Python che in C#. Assicurati di selezionare il linguaggio che si adatta alla stanza lab in cui ti trovi, utilizzando le schede del selettore di linguaggio. Nota, non cambiare linguaggio a metà workshop.

**Seleziona la scheda del linguaggio che corrisponde alla tua stanza lab:**

=== "Python"
    Il linguaggio predefinito per il workshop è impostato su **Python**.
=== "C#"
    Il linguaggio predefinito per il workshop è impostato su **C#**.

## Autenticazione con Azure

Devi autenticarti con Azure in modo che l'app agent possa accedere al Servizio Agenti Azure AI e ai modelli. Segui questi passaggi:

1. Apri una finestra terminale. L'app terminale è **fissata** alla barra delle applicazioni di Windows 11.

    ![Apri la finestra terminale](../media/windows-taskbar.png){ width="300" }

2. Esegui il seguente comando per autenticarti con Azure:

    ```powershell
    az login
    ```

    !!! note
        Ti verrà richiesto di aprire un link del browser e accedere al tuo account Azure.

        1. Una finestra del browser si aprirà automaticamente, seleziona **Account di lavoro o scuola** e poi seleziona **Continua**.

        1. Utilizza il **Nome utente** e la **Password** trovati nella **sezione superiore** della scheda **Risorse** nell'ambiente lab.

        2. Seleziona **Sì, tutte le app**

3. Quindi seleziona la sottoscrizione **Predefinita** dalla riga di comando, selezionando **Invio**.

4. Una volta effettuato l'accesso, esegui il seguente comando per assegnare il ruolo **utente** al gruppo di risorse:

    ```powershell
    $subId = $(az account show --query id --output tsv) `
    ;$objectId = $(az ad signed-in-user show --query id -o tsv) `
    ; az role assignment create --role "f6c7c914-8db3-469d-8ca1-694a8f32e121" --assignee-object-id $objectId --scope /subscriptions/$subId/resourceGroups/"rg-agent-workshop" --assignee-principal-type 'User'
    ```

5. Lascia aperta la finestra terminale per i prossimi passaggi.

## Aprire il Workshop

Segui questi passaggi per aprire il workshop in Visual Studio Code:

=== "Python"

      1. Dalla finestra terminale, esegui i seguenti comandi per clonare il repository del workshop, navigare alla cartella pertinente, configurare un ambiente virtuale, attivarlo e installare i pacchetti richiesti:

          ```powershell
          git clone https://github.com/microsoft/build-your-first-agent-with-azure-ai-agent-service-workshop.git `
          ; cd build-your-first-agent-with-azure-ai-agent-service-workshop `
          ; python -m venv src/python/workshop/.venv `
          ; src\python\workshop\.venv\Scripts\activate `
          ; pip install -r src/python/workshop/requirements.txt `
          ; code --install-extension tomoki1207.pdf
          ```

      2. Apri in VS Code. Dalla finestra terminale, esegui il seguente comando:

          ```powershell
          code .vscode\python-workspace.code-workspace
          ```

        !!! warning "Quando il progetto si apre in VS Code, appaiono due notifiche nell'angolo in basso a destra. Clicca ✖ per chiudere entrambe le notifiche."

=== "C#"

    1. Da una finestra terminale, esegui i seguenti comandi per clonare il repository del workshop:

        ```powershell
        git clone https://github.com/microsoft/build-your-first-agent-with-azure-ai-agent-service-workshop.git
        ```

    === "VS Code"

        1. Apri il workshop in Visual Studio Code. Dalla finestra terminale, esegui il seguente comando:

            ```powershell
            code build-your-first-agent-with-azure-ai-agent-service-workshop\.vscode\csharp-workspace.code-workspace
            ```

        !!! note "Quando il progetto si apre in VS Code, apparirà una notifica nell'angolo in basso a destra per installare l'estensione C#. Clicca **Installa** per installare l'estensione C#, in quanto fornirà le funzionalità necessarie per lo sviluppo C#."

    === "Visual Studio 2022"

        1. Apri il workshop in Visual Studio 2022. Dalla finestra terminale, esegui il seguente comando:

            ```powershell
            start build-your-first-agent-with-azure-ai-agent-service-workshop\src\csharp\workshop\AgentWorkshop.sln
            ```

            !!! note "Potresti essere chiesto con quale programma aprire la solution. Seleziona **Visual Studio 2022**."

## Endpoint del Progetto Azure AI Foundry

Successivamente, accediamo ad Azure AI Foundry per recuperare l'endpoint del progetto, che l'app agent utilizza per connettersi al Servizio Agenti Azure AI.

1. Naviga al sito web [Azure AI Foundry](https://ai.azure.com){:target="_blank"}.
2. Seleziona **Accedi** e utilizza il **Nome utente** e la **Password** trovati nella **sezione superiore** della scheda **Risorse** nell'ambiente lab. Clicca sui campi **Nome utente** e **Password** per compilare automaticamente i dettagli di accesso.
    ![Credenziali Azure](../media/azure-credentials.png){:width="500"}
3. Leggi l'introduzione ad Azure AI Foundry e clicca **Capito**.
4. Naviga a [Tutte le Risorse](https://ai.azure.com/AllResources){:target="_blank"} per visualizzare l'elenco delle risorse AI che sono state pre-fornite per te.
5. Seleziona il nome della risorsa che inizia con **aip-** di tipo **Progetto**.

    ![Seleziona progetto](../media/ai-foundry-project.png){:width="500"}

6. Rivedi la guida introduttiva e clicca **Chiudi**.
7. Dal menu laterale **Panoramica**, individua la sezione **Endpoint e chiavi** -> **Librerie** -> **Azure AI Foundry**, clicca l'icona **Copia** per copiare l'**endpoint del progetto Azure AI Foundry**.

    ![Copia stringa di connessione](../media/project-connection-string.png){:width="500"}

=== "Python"

    ## Configurare il Workshop

    1. Torna al workshop che hai aperto in VS Code.
    2. **Rinomina** il file `.env.sample` in `.env`.

        - Seleziona il file **.env.sample** nel pannello **Esplora** di VS Code.
        - Clicca destro sul file e seleziona **Rinomina**, o premi <kbd>F2</kbd>.
        - Cambia il nome del file in `.env` e premi <kbd>Invio</kbd>.

    3. Incolla l'**Endpoint del progetto** che hai copiato da Azure AI Foundry nel file `.env`.

        ```python
        PROJECT_ENDPOINT="<your_project_endpoint>"
        ```

        Il tuo file `.env` dovrebbe assomigliare a questo ma con il tuo endpoint del progetto.

        ```python
        PROJECT_ENDPOINT="<your_project_endpoint>"
        MODEL_DEPLOYMENT_NAME="<your_model_deployment_name>"
        DEV_TUNNEL_URL="<your_dev_tunnel_url>"
        ```

    4. Salva il file `.env`.

    ## Struttura del Progetto

    Assicurati di familiarizzare con le **sottocartelle** e i **file** chiave con cui lavorerai durante tutto il workshop.

    5. Il file **app.py**: Il punto di ingresso per l'app, contenente la sua logica principale.
    6. Il file **sales_data.py**: La logica di funzione per eseguire query SQL dinamiche contro il database SQLite.
    7. Il file **stream_event_handler.py**: Contiene la logica del gestore di eventi per lo streaming di token.
    8. La cartella **shared/files**: Contiene i file creati dall'app agent.
    9. La cartella **shared/instructions**: Contiene le istruzioni passate all'LLM.

    ![Struttura delle cartelle del lab](../media/project-structure-self-guided-python.png)

=== "C#"

    ## Configurare il Workshop

    1. Apri un terminale e naviga alla cartella **src/csharp/workshop/AgentWorkshop.Client**.

        ```powershell
        cd build-your-first-agent-with-azure-ai-agent-service-workshop\src\csharp\workshop\AgentWorkshop.Client
        ```

    2. Aggiungi l'**Endpoint del progetto** che hai copiato da Azure AI Foundry ai segreti utente.

        ```powershell
        dotnet user-secrets set "ConnectionStrings:AiAgentService" "<your_project_endpoint>"
        ```

    3. Aggiungi il **Nome del deployment del modello** ai segreti utente.

        ```powershell
        dotnet user-secrets set "Azure:ModelName" "gpt-4o"
        ```

    4. Aggiungi l'**ID connessione Bing** ai segreti utente per il grounding con la ricerca Bing.

        ```powershell
        $subId = $(az account show --query id --output tsv)
        $rgName = "rg-agent-workshop"
        $aiAccount = "<ai_account_name>" # Sostituisci con il nome dell'account AI effettivo
        $aiProject = "<ai_project_name>" # Sostituisci con il nome del progetto AI effettivo
        $bingConnectionId = "/subscriptions/$subId/resourceGroups/$rgName/providers/Microsoft.CognitiveServices/accounts/$aiAccount/projects/$aiProject/connections/groundingwithbingsearch"
        dotnet user-secrets set "Azure:BingConnectionId" "$bingConnectionId"
        ```

    ## Struttura del Progetto

    Assicurati di familiarizzare con le **sottocartelle** e i **file** chiave con cui lavorerai durante tutto il workshop.

    ### La cartella workshop

    - I file **Lab1.cs, Lab2.cs, Lab3.cs**: Il punto di ingresso per ogni lab, contenente la sua logica agent.
    - Il file **Program.cs**: Il punto di ingresso per l'app, contenente la sua logica principale.
    - Il file **SalesData.cs**: La logica di funzione per eseguire query SQL dinamiche contro il database SQLite.

    ### La cartella shared

    - La cartella **files**: Contiene i file creati dall'app agent.
    - La cartella **fonts**: Contiene i font multilingue utilizzati da Code Interpreter.
    - La cartella **instructions**: Contiene le istruzioni passate all'LLM.

    ![Struttura delle cartelle del lab](../media/project-structure-self-guided-csharp.png)

## Suggerimenti Pro

!!! tips
    1. Il **Menu Hamburger** nel pannello destro dell'ambiente lab offre funzionalità aggiuntive, inclusa la **Vista Finestra Divisa** e l'opzione per terminare il lab. La **Vista Finestra Divisa** ti consente di massimizzare l'ambiente lab a schermo intero, ottimizzando lo spazio dello schermo. Le **Istruzioni** del lab e il pannello **Risorse** si apriranno in una finestra separata.
    2. Se le istruzioni del lab sono lente a scorrere nell'ambiente lab, prova a copiare l'URL delle istruzioni e aprirlo nel **browser locale del tuo computer** per un'esperienza più fluida.
    3. Se hai difficoltà a visualizzare un'immagine, semplicemente **clicca sull'immagine per ingrandirla**.
