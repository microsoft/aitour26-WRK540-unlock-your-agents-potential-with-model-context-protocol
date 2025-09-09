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

    ![Struttura delle cartelle del lab](media/project-structure-self-guided-python.png)

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

    ![Struttura delle cartelle del lab](media/project-structure-self-guided-csharp.png)
