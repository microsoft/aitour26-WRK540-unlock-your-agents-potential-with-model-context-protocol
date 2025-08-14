May dalawang VS Code workspaces sa workshop, isa para sa Python at isa para sa C#. Naglalaman ang workspace ng source code at lahat ng files na kailangan upang makumpleto ang mga lab para sa bawat wika. Piliin ang workspace na tumugma sa wikang gusto ninyong gamitin.

=== "Python"

    1. **I-copy** ang sumusunod na path sa clipboard:

        ```text
        /workspace/.vscode/python-workspace.code-workspace
        ```
    1. Mula sa VS Code menu, piliin ang **File** pagkatapos ang **Open Workspace from File**.
    3. Palitan at **i-paste** ang copied path name at piliin ang **OK**.


    ## Project Structure

    Pamilyaruhin ang sarili sa mga mahalagang **folders** at **files** sa workspace na gagamitin ninyo sa buong workshop.

    ### Ang "workshop" folder

    - Ang **app.py** file: Ang entry point para sa app, na naglalaman ng main logic nito.
  
    Mapansin ang **INSTRUCTIONS_FILE** variable—nagtatakda ito kung aling instructions file ang gagamitin ng agent. I-update ninyo ang variable na ito sa susunod na lab.

    - Ang **resources.txt** file: Naglalaman ng mga resources na ginagamit ng agent app.
    - Ang **.env** file: Naglalaman ng mga environment variables na ginagamit ng agent app.

    ### Ang "mcp_server" folder

    - Ang **sales_analysis.py** file: Ang MCP Server na may tools para sa sales analysis.

    ### Ang "shared/instructions" folder

    - Ang **instructions** folder: Naglalaman ng mga instructions na ipinasa sa LLM.

    ![Lab folder structure](media/project-structure-self-guided-python.png)

=== "C#"

    1. Sa Visual Studio Code, pumunta sa **File** > **Open Workspace from File**.
    2. Palitan ang default path ng sumusunod:

        ```text
        /workspace/.vscode/csharp-workspace.code-workspace
        ```

    3. Piliin ang **OK** upang buksan ang workspace.

    ## Project Structure

    Siguraduhing pamilyaruhin ang sarili sa mga mahalagang **folders** at **files** na gagamitin ninyo sa buong workshop.

    ### Ang workshop folder

    - Ang **Lab1.cs, Lab2.cs, Lab3.cs** files: Ang entry point para sa bawat lab, na naglalaman ng agent logic nito.
    - Ang **Program.cs** file: Ang entry point para sa app, na naglalaman ng main logic nito.
    - Ang **SalesData.cs** file: Ang function logic upang mag-execute ng dynamic SQL queries laban sa SQLite database.

    ### Ang shared folder

    - Ang **files** folder: Naglalaman ng mga files na ginawa ng agent app.
    - Ang **fonts** folder: Naglalaman ng mga multilingual fonts na ginagamit ng Code Interpreter.
    - Ang **instructions** folder: Naglalaman ng mga instructions na ipinasa sa LLM.

    ![Lab folder structure](media/project-structure-self-guided-csharp.png)

*Isinalin gamit ang GitHub Copilot.*
