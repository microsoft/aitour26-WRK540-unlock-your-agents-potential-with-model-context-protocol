## Opening the Language Workspace

There are two workspaces in the workshop, one for Python and one for C#. The workspace contains the source code and all the files needed to complete the labs for each language. Choose the workspace that matches the language you want to work with.

=== "Python"

    1. In Visual Studio Code, go to **File** > **Open Workspace from File**.
    2. Replace the default path with the following:

        ```text
        /workspace/.vscode/python-workspace.code-workspace
        ```

    3. Select **OK** to open the workspace.

    ## Project Structure

    Be sure to familiarize yourself with the key **folders** and **files** you’ll be working with throughout the workshop.

    ### The workshop folder

    - The **app.py** file: The entry point for the app, containing its main logic.
    - The **sales_data.py** file: The function logic to execute dynamic SQL queries against the SQLite database.
    - The **stream_event_handler.py** file: Contains the event handler logic for token streaming.

    ### The shared folder

    - The **files** folder: Contains the files created by the agent app.
    - The **fonts** folder: Contains the multilingual fonts used by Code Interpreter.
    - The **instructions** folder: Contains the instructions passed to the LLM.

    ![Lab folder structure](media/project-structure-self-guided-python.png)

=== "C#"

    1. In Visual Studio Code, go to **File** > **Open Workspace from File**.
    2. Replace the default path with the following:

        ```text
        /workspace/.vscode/csharp-workspace.code-workspace
        ```

    3. Select **OK** to open the workspace.

    ## Project Structure

    Be sure to familiarize yourself with the key **folders** and **files** you’ll be working with throughout the workshop.

    ### The workshop folder

    - The **Lab1.cs, Lab2.cs, Lab3.cs** files: The entry point for each lab, containing its agent logic.
    - The **Program.cs** file: The entry point for the app, containing its main logic.
    - The **SalesData.cs** file: The function logic to execute dynamic SQL queries against the SQLite database.

    ### The shared folder

    - The **files** folder: Contains the files created by the agent app.
    - The **fonts** folder: Contains the multilingual fonts used by Code Interpreter.
    - The **instructions** folder: Contains the instructions passed to the LLM.

    ![Lab folder structure](media/project-structure-self-guided-csharp.png)
