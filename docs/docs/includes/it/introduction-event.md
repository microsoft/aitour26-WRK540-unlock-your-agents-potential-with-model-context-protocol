## Partecipanti all'Evento Microsoft

Le istruzioni in questa pagina presuppongono che tu stia partecipando a un evento e abbia accesso a un ambiente lab preconfigurato. Questo ambiente fornisce una sottoscrizione Azure con tutti gli strumenti e le risorse necessari per completare il workshop.

## Introduzione

Questo workshop è progettato per insegnarti il Servizio Agenti Azure AI e l'[SDK](https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme?context=%2Fazure%2Fai-services%2Fagents%2Fcontext%2Fcontext){:target="_blank"} associato. È composto da più lab, ognuno che evidenzia una caratteristica specifica del Servizio Agenti Azure AI. I lab sono pensati per essere completati in ordine, poiché ognuno si basa sulla conoscenza e il lavoro del lab precedente.

## Risorse Cloud del Workshop

Le seguenti risorse sono pre-fornite nella tua sottoscrizione Azure del lab:

- Un gruppo di risorse chiamato **rg-zava-agent-wks-nnnnnnnn**
- Un **hub Azure AI Foundry** chiamato **fdy-zava-agent-wks-nnnnnnnn**
- Un **progetto Azure AI Foundry** chiamato **prj-zava-agent-wks-nnnnnnnn**
- Due modelli sono distribuiti: **gpt-4o-mini** e **text-embedding-3-small**. [Vedi prezzi.](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/){:target="\_blank"}
- Database Azure Database for PostgreSQL Flexible Server (B1ms Burstable 32GB) chiamato **pg-zava-agent-wks-nnnnnnnn**. [Vedi prezzi](https://azure.microsoft.com/pricing/details/postgresql/flexible-server){:target="\_blank"}
- Risorsa Application Insights chiamata **appi-zava-agent-wks-nnnnnnnn**. [Vedi prezzi](https://azure.microsoft.com/pricing/calculator/?service=monitor){:target="\_blank"}

## Selezionare il Linguaggio di Programmazione del Workshop

Il workshop è disponibile sia in Python che in C#. Assicurati di selezionare il linguaggio che si adatta alla stanza lab o alla preferenza utilizzando le schede del selettore di linguaggio. Nota, non cambiare linguaggio a metà workshop.

**Seleziona la scheda del linguaggio che corrisponde alla tua stanza lab:**

=== "Python"
    Il linguaggio predefinito per il workshop è impostato su **Python**.
=== "C#"
    Il linguaggio predefinito per il workshop è impostato su **C#**.

    !!! warning "La versione C#/.NET di questo workshop è in beta e ha problemi di stabilità noti."

    Assicurati di leggere la sezione della [guida alla risoluzione dei problemi](../../en/dotnet-troubleshooting.md) **PRIMA** di iniziare il workshop. Altrimenti, seleziona la versione **Python** del workshop.

## Autenticazione con Azure

Devi autenticarti con Azure in modo che l'app agent possa accedere al Servizio Agenti Azure AI e ai modelli. Segui questi passaggi:

1. Apri una finestra terminale. L'app terminale è **fissata** alla barra delle applicazioni di Windows 11.

    ![Apri la finestra terminale](../../media/windows-taskbar.png){ width="300" }

2. Esegui il seguente comando per autenticarti con Azure:

    ```powershell
    az login
    ```

    !!! note
        Ti verrà richiesto di aprire un link del browser e accedere al tuo account Azure.

        1. Una finestra del browser si aprirà automaticamente, seleziona **Account di lavoro o scuola** e poi seleziona **Continua**.
        2. Utilizza il **Nome utente** e il **TAP (Temporary Access Pass)** trovati nella **sezione superiore** della scheda **Risorse** nell'ambiente lab.
        3. Seleziona **Sì, tutte le app**
        4. Seleziona **Fatto**

3. Quindi seleziona la sottoscrizione **Predefinita** dalla riga di comando, selezionando **Invio**.

4. Lascia aperta la finestra terminale per i prossimi passaggi.

## Autenticazione con il Servizio DevTunnel

DevTunnel consente al Servizio Agenti Azure AI di accedere al tuo Server MCP locale durante il workshop.

```powershell
devtunnel login
```

!!! note
    Ti verrà richiesto di utilizzare l'account che hai utilizzato per `az login`. Seleziona l'account e continua.

Lascia aperta la finestra terminale per i prossimi passaggi.

## Aprire il Workshop

Segui questi passaggi per aprire il workshop in Visual Studio Code:

=== "Python"

    Il seguente blocco di comandi aggiorna il repository del workshop, attiva l'ambiente virtuale Python e apre il progetto in VS Code.

    Copia e incolla il seguente blocco di comandi nel terminale e premi **Invio**.

    ```powershell
    ; cd $HOME\aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol `
    ; git pull `
    ; .\src\python\workshop\.venv\Scripts\activate `
    ; code .vscode\python-workspace.code-workspace
    ```

    !!! warning "Quando il progetto si apre in VS Code, appaiono due notifiche nell'angolo in basso a destra. Clicca ✖ per chiudere entrambe le notifiche."

=== "C#"

    === "VS Code"

        1. Apri il workshop in Visual Studio Code. Dalla finestra terminale, esegui il seguente comando:

            ```powershell
            ; cd $HOME\aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol `
            ; git pull `
            ;code .vscode\csharp-workspace.code-workspace
            ```

        !!! note "Quando il progetto si apre in VS Code, apparirà una notifica nell'angolo in basso a destra per installare l'estensione C#. Clicca **Installa** per installare l'estensione C#, in quanto fornirà le funzionalità necessarie per lo sviluppo C#."

    === "Visual Studio 2022"

        2. Apri il workshop in Visual Studio 2022. Dalla finestra terminale, esegui il seguente comando:

            ```powershell
            ; git pull `
            ;cd $HOME; start .\aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol\src\csharp\McpAgentWorkshop.slnx
            ```

            !!! note "Potresti essere chiesto con quale programma aprire la solution. Seleziona **Visual Studio 2022**."

## Struttura del Progetto

=== "Python"

    Assicurati di familiarizzare con le **sottocartelle** e i **file** chiave con cui lavorerai durante tutto il workshop.

    5. Il file **main.py**: Il punto di ingresso per l'app, contenente la sua logica principale.
    6. Il file **sales_data.py**: La logica di funzione per eseguire query SQL dinamiche contro il database SQLite.
    7. Il file **stream_event_handler.py**: Contiene la logica del gestore di eventi per lo streaming di token.
    8. La cartella **shared/files**: Contiene i file creati dall'app agent.
    9. La cartella **shared/instructions**: Contiene le istruzioni passate all'LLM.

    ![Struttura delle cartelle del lab](../../media/project-structure-self-guided-python.png)

=== "C#"

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

## Suggerimenti Pro

!!! tips
    1. Il **Menu Hamburger** nel pannello destro dell'ambiente lab offre funzionalità aggiuntive, inclusa la **Vista Finestra Divisa** e l'opzione per terminare il lab. La **Vista Finestra Divisa** ti consente di massimizzare l'ambiente lab a schermo intero, ottimizzando lo spazio dello schermo. Le **Istruzioni** del lab e il pannello **Risorse** si apriranno in una finestra separata.
