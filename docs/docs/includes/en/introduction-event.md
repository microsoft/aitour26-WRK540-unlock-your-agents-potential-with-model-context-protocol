## Microsoft Build Attendees

The instructions on this page assume you are attending an event and have access to a pre-configured lab environment. This environment provides an Azure subscription with all the tools and resources needed to complete the workshop.

## Introduction

This workshop is designed to teach you about the Azure AI Agents Service and the associated [SDK](https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme?context=%2Fazure%2Fai-services%2Fagents%2Fcontext%2Fcontext){:target="_blank"}. It consists of multiple labs, each highlighting a specific feature of the Azure AI Agents Service. The labs are meant to be completed in order, as each one builds on the knowledge and work from the previous lab.

## Select Workshop Programming Language

The workshop is available in both Python and C#. Please make sure to select the language that fits the lab room or preference by using the language selector tabs. Note, don't switch languages mid-workshop.

**Select the language tab that matches your lab room:**

=== "Python"
    The default language for the workshop is set to **Python**.
=== "C#"
    The default language for the workshop is set to **C#**.

## Authenticate with Azure

You need to authenticate with Azure so the agent app can access the Azure AI Agents Service and models. Follow these steps:

1. Open a terminal window. The terminal app is **pinned** to the Windows 11 taskbar.

    ![Open the terminal window](../media/windows-taskbar.png){ width="300" }

2. Run the following command to authenticate with Azure:

    ```powershell
    az login
    ```

    !!! note
        You'll be prompted to open a browser link and log in to your Azure account.

        1. A browser window will open automatically, select **Work or school account** and click **Next**.

        1. Use the **Username** and **Password** found in the **top section** of the **Resources** tab in the lab environment.

        2. Select **OK**, then **Done**.

3. Then select the **Default** subscription from the command line, by clicking on **Enter**.

4. Once you've logged in, run the following command to assign the **user** role to the resource group:

    <!-- ```powershell
    $subId = $(az account show --query id --output tsv) `
    ;$objectId = $(az ad signed-in-user show --query id -o tsv) `
    ; az role assignment create --role "Azure AI Developer" --assignee-object-id $objectId --scope /subscriptions/$subId/resourceGroups/"rg-zava-agent-wks" --assignee-principal-type 'User'
    ``` -->

    ```powershell
    ; $username = Read-Host "Enter your user name” `
    ; $subId = $(az account show --query id --output tsv) `
    ; New-AzRoleAssignment -SignInName $username -RoleDefinitionName "Cognitive Services User" -Scope "/subscriptions/$subId" `
    ; New-AzRoleAssignment -SignInName $username -RoleDefinitionName "Azure AI Developer" -Scope "/subscriptions/$subId/resourceGroups/rg-zava-agent-wks"
    ```

5. Leave the terminal window open for the next steps.

## Authenticate with the DevTunnel Service

```powershell
devtunnel login
```

Authenticate with the Skillable Username and TAP.

## Restore the Database

```powershell
; $UniqueSuffix = Read-Host "Enter your unique suffix" `
; cd $HOME\aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol\infra\skillable `
; .\init-db-azure-action.ps1 -UniqueSuffix $UniqueSuffix -AzurePgPassword "SecurePassword123!"
```

## Open the Workshop

Follow these steps to open the workshop in Visual Studio Code:

=== "Python"

      1. From the terminal window, execute the following commands to clone the workshop repository, navigate to the relevant folder, set up a virtual environment, activate it, and install the required packages:

          ```powershell
          ; cd $HOME\aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol `
          ; git pull `
          ; src\python\workshop\.venv\Scripts\activate `
          ; code .vscode\python-workspace.code-workspace
          ```

        !!! warning "When the project opens in VS Code, two notifications appear in the bottom right corner. Click ✖ to close both notifications."

=== "C#"

    1. From a terminal window, execute the following commands to clone the workshop repository:

        ```powershell
        git clone https://github.com/microsoft/build-your-first-agent-with-azure-ai-agent-service-workshop.git
        ```

    === "VS Code"

        1. Open the workshop in Visual Studio Code. From the terminal window, run the following command:

            ```powershell
            code build-your-first-agent-with-azure-ai-agent-service-workshop\.vscode\csharp-workspace.code-workspace
            ```

        !!! note "When the project opens in VS Code, a notification will appear in the bottom right corner to install the C# extension. Click **Install** to install the C# extension, as this will provide the necessary features for C# development."

    === "Visual Studio 2022"

        2. Open the workshop in Visual Studio 2022. From the terminal window, run the following command:

            ```powershell
            start build-your-first-agent-with-azure-ai-agent-service-workshop\src\csharp\workshop\AgentWorkshop.sln
            ```

            !!! note "You may be asked what program to open the solution with. Select **Visual Studio 2022**."

## Project Structure

=== "Python"

    Be sure to familiarize yourself with the key **subfolders** and **files** you’ll be working with throughout the workshop.

    5. The **main.py** file: The entry point for the app, containing its main logic.
    6. The **sales_data.py** file: The function logic to execute dynamic SQL queries against the SQLite database.
    7. The **stream_event_handler.py** file: Contains the event handler logic for token streaming.
    8. The **shared/files** folder: Contains the files created by the agent app.
    9. The **shared/instructions** folder: Contains the instructions passed to the LLM.

    ![Lab folder structure](../media/project-structure-self-guided-python.png)

=== "C#"

    ## Configure the Workshop

    1. Open a terminal and navigate to the **src/csharp/workshop/AgentWorkshop.Client** folder.

        ```powershell
        cd build-your-first-agent-with-azure-ai-agent-service-workshop\src\csharp\workshop\AgentWorkshop.Client
        ```

    2. Add the **Project endpoint** you copied from Azure AI Foundry to the user secrets.

        ```powershell
        dotnet user-secrets set "ConnectionStrings:AiAgentService" "<your_project_endpoint>"
        ```

    3. Add the **Model deployment name** to the user secrets.

        ```powershell
        dotnet user-secrets set "Azure:ModelName" "gpt-4o"
        ```

    4. Add the **Bing connection ID** to the user secrets for grounding with Bing search.

        ```powershell
        $subId = $(az account show --query id --output tsv)
        $rgName = "rg-agent-workshop"
        $aiAccount = "<ai_account_name>" # Replace with the actual AI account name
        $aiProject = "<ai_project_name>" # Replace with the actual AI project name
        $bingConnectionId = "/subscriptions/$subId/resourceGroups/$rgName/providers/Microsoft.CognitiveServices/accounts/$aiAccount/projects/$aiProject/connections/groundingwithbingsearch"
        dotnet user-secrets set "Azure:BingConnectionId" "$bingConnectionId"
        ```

    ## Project Structure

    Be sure to familiarize yourself with the key **subfolders** and **files** you’ll be working with throughout the workshop.

    ### The workshop folder

    - The **Lab1.cs, Lab2.cs, Lab3.cs** files: The entry point for each lab, containing its agent logic.
    - The **Program.cs** file: The entry point for the app, containing its main logic.
    - The **SalesData.cs** file: The function logic to execute dynamic SQL queries against the SQLite database.

    ### The shared folder

    - The **files** folder: Contains the files created by the agent app.
    - The **fonts** folder: Contains the multilingual fonts used by Code Interpreter.
    - The **instructions** folder: Contains the instructions passed to the LLM.

    ![Lab folder structure](../media/project-structure-self-guided-csharp.png)

## Pro Tips

!!! tips
    1. The **Burger Menu** in the right-hand panel of the lab environment offers additional features, including the **Split Window View** and the option to end the lab. The **Split Window View** allows you to maximize the lab environment to full screen, optimizing screen space. The lab's **Instructions** and **Resources** panel will open in a separate window.
    2. If the lab instructions are slow to scroll in the lab environment, try copying the instructions’ URL and opening it in **your computer’s local browser** for a smoother experience.
    3. If you have trouble viewing an image, simply **click the image to enlarge it**.
