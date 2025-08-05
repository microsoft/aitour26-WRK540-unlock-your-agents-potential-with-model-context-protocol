## De Taal Workspace Openen

Er zijn twee workspaces in de workshop, één voor Python en één voor C#. De workspace bevat de broncode en alle bestanden die nodig zijn om de labs voor elke taal te voltooien. Kies de workspace die overeenkomt met de taal waarmee je wilt werken.

=== "Python"

    1. Kopieer het volgende commando naar je klembord:

        ```text
        File: Open Workspace from File...
        ```
    2. Ga naar Visual Studio Code, druk op <kbd>F1</kbd> om het Command Palette te openen.
    3. Plak het commando in het Command Palette en selecteer **Open Workspace from File...**.
    4. Kopieer en plak het volgende pad in de bestandskiezer en druk op <kbd>Enter</kbd>:

        ```text
        /workspace/.vscode/python-workspace.code-workspace
        ```

    ## Projectstructuur

    Zorg ervoor dat je vertrouwd raakt met de belangrijkste **mappen** en **bestanden** waarmee je tijdens de workshop zult werken.

    ### De workshop map

    - Het **app.py** bestand: Het toegangspunt voor de app, met de hoofdlogica.
  
    Let op de **INSTRUCTIONS_FILE** variabele—deze bepaalt welk instructiebestand de agent gebruikt. Je zult deze variabele bijwerken in een latere lab.

    - Het **resources.txt** bestand: Bevat de resources die door de agent app worden gebruikt.
    - Het **.env** bestand: Bevat de omgevingsvariabelen die door de agent app worden gebruikt.

    ### De mcp_server map

    - Het **sales_analysis.py** bestand: De MCP Server met tools voor verkoopanalyse.

    ### De shared map

    - De **instructions** map: Bevat de instructies die worden doorgegeven aan het LLM.

    ![Lab mapstructuur](media/project-structure-self-guided-python.png)

=== "C#"

    1. Ga in Visual Studio Code naar **File** > **Open Workspace from File**.
    2. Vervang het standaardpad door het volgende:

        ```text
        /workspace/.vscode/csharp-workspace.code-workspace
        ```

    3. Selecteer **OK** om de workspace te openen.

    ## Projectstructuur

    Zorg ervoor dat je vertrouwd raakt met de belangrijkste **mappen** en **bestanden** waarmee je tijdens de workshop zult werken.

    ### De workshop map

    - De **Lab1.cs, Lab2.cs, Lab3.cs** bestanden: Het toegangspunt voor elke lab, met de agentlogica.
    - Het **Program.cs** bestand: Het toegangspunt voor de app, met de hoofdlogica.
    - Het **SalesData.cs** bestand: De functielogica om dynamische SQL queries uit te voeren tegen de SQLite database.

    ### De shared map

    - De **files** map: Bevat de bestanden die door de agent app zijn gemaakt.
    - De **fonts** map: Bevat de meertalige lettertypen die door Code Interpreter worden gebruikt.
    - De **instructions** map: Bevat de instructies die worden doorgegeven aan het LLM.

    ![Lab mapstructuur](media/project-structure-self-guided-csharp.png)

*Vertaald met behulp van GitHub Copilot.*
