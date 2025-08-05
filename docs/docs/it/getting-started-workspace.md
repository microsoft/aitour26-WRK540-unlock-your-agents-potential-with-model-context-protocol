## Apertura del Workspace del Linguaggio

Ci sono due workspace nel workshop, uno per Python e uno per C#. Il workspace contiene il codice sorgente e tutti i file necessari per completare i lab per ogni linguaggio. Scegli il workspace che corrisponde al linguaggio con cui vuoi lavorare.

=== "Python"

    1. Copia il seguente comando nei tuoi appunti:

        ```text
        File: Open Workspace from File...
        ```
    2. Passa a Visual Studio Code, premi <kbd>F1</kbd> per aprire la Command Palette.
    3. Incolla il comando nella Command Palette e seleziona **Open Workspace from File...**.
    4. Copia e incolla il seguente percorso nel selettore file e premi <kbd>Enter</kbd>:

        ```text
        /workspace/.vscode/python-workspace.code-workspace
        ```

    ## Struttura del Progetto

    Assicurati di familiarizzare con le **cartelle** e i **file** chiave con cui lavorerai durante tutto il workshop.

    ### La cartella workshop

    - Il file **app.py**: Il punto di ingresso per l'app, contenente la sua logica principale.
  
    Nota la variabile **INSTRUCTIONS_FILE**—imposta quale file di istruzioni usa l'agente. Aggiornerai questa variabile in un lab successivo.

    - Il file **resources.txt**: Contiene le risorse utilizzate dall'app agente.
    - Il file **.env**: Contiene le variabili d'ambiente utilizzate dall'app agente.

    ### La cartella mcp_server

    - Il file **sales_analysis.py**: Il Server MCP con strumenti per l'analisi delle vendite.

    ### La cartella shared

    - La cartella **instructions**: Contiene le istruzioni passate al LLM.

    ![Struttura cartelle Lab](media/project-structure-self-guided-python.png)

=== "C#"

    1. In Visual Studio Code, vai a **File** > **Open Workspace from File**.
    2. Sostituisci il percorso predefinito con il seguente:

        ```text
        /workspace/.vscode/csharp-workspace.code-workspace
        ```

    3. Seleziona **OK** per aprire il workspace.

    ## Struttura del Progetto

    Assicurati di familiarizzare con le **cartelle** e i **file** chiave con cui lavorerai durante tutto il workshop.

    ### La cartella workshop

    - I file **Lab1.cs, Lab2.cs, Lab3.cs**: Il punto di ingresso per ogni lab, contenente la sua logica agente.
    - Il file **Program.cs**: Il punto di ingresso per l'app, contenente la sua logica principale.
    - Il file **SalesData.cs**: La logica della funzione per eseguire query SQL dinamiche contro il database SQLite.

    ### La cartella shared

    - La cartella **files**: Contiene i file creati dall'app agente.
    - La cartella **fonts**: Contiene i font multilingue utilizzati da Code Interpreter.
    - La cartella **instructions**: Contiene le istruzioni passate al LLM.

    ![Struttura cartelle Lab](media/project-structure-self-guided-csharp.png)

*Tradotto utilizzando GitHub Copilot e GPT-4o.*
