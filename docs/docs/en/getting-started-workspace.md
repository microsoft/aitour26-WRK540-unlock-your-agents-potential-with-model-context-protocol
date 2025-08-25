There are two VS Code workspaces in the workshop, one for Python and one for C#. The workspace contains the source code and all the files needed to complete the labs for each language. Choose the workspace that matches the language you want to work with.

=== "Python"

    1. **Copy** the following path to the clipboard:

        ```text
        /workspace/.vscode/python-workspace.code-workspace
        ```
    1. From the VS Code menu, select **File** then **Open Workspace from File**.
    3. Replace and **paste** the copied path name and select **OK**.


    ## Project Structure

    Familiarize yourself with the key **folders** and **files** in the workspace you’ll be working with throughout the workshop.

    ### The "workshop" folder

    - The **app.py** file: The entry point for the app, containing its main logic.

    Note the **INSTRUCTIONS_FILE** variable—it sets which instructions file the agent uses. You will update this variable in a later lab.

    - The **resources.txt** file: Contains the resources used by the agent app.
    - The **.env** file: Contains the environment variables used by the agent app.

    ### The "mcp_server" folder

    - The **sales_analysis.py** file: The MCP Server with tools for sales analysis.

    ### The "shared/instructions" folder

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

    The project uses [Aspire](http://aka.ms/dotnet-aspire) to simplify building the agent application, managing the MCP server, and orchestrating all the external dependencies. The solution is comproised for four projects, all prefixed with `McpAgentWorkshop`:

    * `AppHost`: The Aspire orchestrator, and launch project for the workshop.
    * `McpServer`: The MCP server project.
    * `ServiceDefaults`: Default configuration for services, such as logging and telemetry.
    * `WorkshopApi`: The Agent API for the workshop. The core application logic is in the `AgentService` class.

    In addition to the .NET projects in the solution, there is a `shared` folder (visible as a Solution Folder, and via the file explorer), which contains:

    * `instructions`: The instructions passed to the LLM.
    * `scripts`: Helper shell scripts for various tasks, these will be referred to when required.
    * `webapp`: The front-end client application. Note: This is a Python application, which Aspire will manage the lifecycle of.

    ![Lab folder structure](media/project-structure-self-guided-csharp.png)
