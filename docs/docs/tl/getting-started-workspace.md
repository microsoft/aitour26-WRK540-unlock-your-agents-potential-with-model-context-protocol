May dalawang VS Code workspace sa workshop, isa para sa Python at isa para sa C#. Ang workspace ay naglalaman ng source code at lahat ng file na kailangan upang kumpletuhin ang mga lab para sa bawat wika. Piliin ang workspace na tumutugma sa wikang nais mong gamitin.

=== "Python"

    1. **Kopyahin** ang sumusunod na path sa clipboard:

        ```text
        /workspace/.vscode/python-workspace.code-workspace
        ```
    1. Mula sa VS Code menu, piliin ang **File** pagkatapos **Open Workspace from File**.
    3. Palitan at **i-paste** ang kinopyang path name at piliin ang **OK**.


    ## Istruktura ng Proyekto

    Pamilyarhin ang iyong sarili sa mga pangunahing **folder** at **file** sa workspace na gagamitin mo sa buong workshop.

    ### Ang "workshop" folder

    - Ang **app.py** file: Ang entry point para sa app, naglalaman ng pangunahing lohika nito.
  
    Tandaan ang **INSTRUCTIONS_FILE** variable—ito ang nagtatakda kung aling instructions file ang ginagamit ng agent. Ia-update mo ang variable na ito sa susunod na lab.

    - Ang **resources.txt** file: Naglalaman ng mga resource na ginagamit ng agent app.
    - Ang **.env** file: Naglalaman ng environment variables na ginagamit ng agent app.

    ### Ang "mcp_server" folder

    - Ang **sales_analysis.py** file: Ang MCP Server na may tool para sa sales analysis.

    ### Ang "shared/instructions" folder

    - Ang **instructions** folder: Naglalaman ng instructions na ipinapasa sa LLM.

    ![Istruktura ng Lab folder](media/project-structure-self-guided-python.png)

=== "C#"

    1. Sa Visual Studio Code, pumunta sa **File** > **Open Workspace from File**.
    2. Palitan ang default path ng sumusunod:

        ```text
        /workspace/.vscode/csharp-workspace.code-workspace
        ```

    3. Piliin ang **OK** upang buksan ang workspace.

    ## Istruktura ng Proyekto

    Tiyaking pamilyar ka sa mga pangunahing **folder** at **file** na gagamitin mo sa buong workshop.

    ### Ang workshop folder

    - Ang **Lab1.cs, Lab2.cs, Lab3.cs** files: Mga entry point para sa bawat lab, naglalaman ng agent logic nito.
    - Ang **Program.cs** file: Ang entry point para sa app, naglalaman ng pangunahing lohika nito.
    - Ang **SalesData.cs** file: Ang function logic para magpatupad ng dynamic SQL queries laban sa SQLite database.

    ### Ang shared folder

    - Ang **files** folder: Naglalaman ng mga file na ginawa ng agent app.
    - Ang **fonts** folder: Naglalaman ng multilingual fonts na ginagamit ng Code Interpreter.
    - Ang **instructions** folder: Naglalaman ng instructions na ipinapasa sa LLM.

    ![Istruktura ng Lab folder](media/project-structure-self-guided-csharp.png)

*Isinalin gamit ang GitHub Copilot.*
