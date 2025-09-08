## Self-Guided Learners

These instructions are for self-guided learners who do not have access to a pre-configured lab environment. Follow these steps to set up your environment and begin the workshop.

## Introduction

This workshop is designed to teach you about the Azure AI Agents Service and the associated SDK. It consists of multiple labs, each highlighting a specific feature of the Azure AI Agents Service. The labs are meant to be completed in order, as each one builds on the knowledge and work from the previous lab.

## Prerequisites

1. Access to an Azure subscription. If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/free/){:target="_blank"} before you begin.
1. You need a GitHub account. If you don’t have one, create it at [GitHub](https://github.com/join){:target="_blank"}.

## Select Workshop Programming Language

The workshop is available in both Python and C#. Use the language selector tabs to choose your preferred language. Note, don't switch languages mid-workshop.

**Select the tab for your preferred language:**

=== "Python"
    The default language for the workshop is set to **Python**.
=== "C#"
    The default language for the workshop is set to **C#**.

    !!! warning "The C#/.NET version of this workshop is in beta and has known stability issues."

    Ensure you read the [troubleshooting guide](../../en/dotnet-troubleshooting.md) section **BEFORE** starting the workshop. Else, select the **Python** version of the workshop.

## Open the Workshop

Preferred: **GitHub Codespaces**, which provides a preconfigured environment with all required tools. Alternatively, run locally with a Visual Studio Code **Dev Container** and **Docker**. Use the tabs below to choose.

!!! Tip
    Codespaces or Dev Container builds take about 5 minutes. Start the build, then **continue reading** while it completes.

=== "GitHub Codespaces"

    Select **Open in GitHub Codespaces** to open the project in GitHub Codespaces.

    [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/microsoft/aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol){:target="_blank"}

=== "VS Code Dev Container"

    1. Ensure you have the following installed on your local machine:

        - [Docker](https://docs.docker.com/get-docker/){:target="\_blank"}
        - [Visual Studio Code](https://code.visualstudio.com/download){:target="\_blank"}
        - The [Remote - Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers){:target="\_blank"}
    1. Clone the repository to your local machine:

        ```bash
        git clone https://github.com/microsoft/aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol.git
        ```

    1. Open the cloned repository in Visual Studio Code.
    1. When prompted, select **Reopen in Container** to open the project in a Dev Container.

---

## Authenticate Azure Services

!!! danger
Before proceeding, ensure that your Codespace or Dev Container is fully built and ready.

### Authenticate with DevTunnel

DevTunnel provides a port forwarding service that will be used in the workshop to allow the Azure AI Agents Service to access the MCP Server you'll be running on your local development environment. Follow these steps to authenticate:

1. From VS Code, **press** <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>`</kbd> to open a new terminal window. Then run the following command:
1. **Run the following command** to authenticate with DevTunnel:

   ```shell
   devtunnel login
   ```

1. Follow these steps to authenticate:

   1. Copy the **Authentication Code** to the clipboard.
   2. **Press and hold** the <kbd>ctrl</kbd> or <kbd>cmd</kbd> key.
   3. **Select** the authentication URL to open it in your browser.
   4. **Paste** the code and click **Next**.
   5. **Pick an account** and sign in.
   6. Select **Continue**
   7. **Return** to the terminal window in VS Code.

1. Leave the terminal window **open** for the next steps.

### Authenticate with Azure

Authenticate with Azure to allow the agent app access to the Azure AI Agents Service and models. Follow these steps:

1. Then run the following command:

    ```shell
    az login --use-device-code
    ```

    !!! warning
    If you have multiple Azure tenants, specify the correct one using:

    ```shell
    az login --use-device-code --tenant <tenant_id>
    ```

2. Follow these steps to authenticate:

    1. **Copy** the **Authentication Code** to the clipboard.
    2. **Press and hold** the <kbd>ctrl</kbd> or <kbd>cmd</kbd> key.
    3. **Select** the authentication URL to open it in your browser.
    4. **Paste** the code and click **Next**.
    5. **Pick an account** and sign in.
    6. Select **Continue**
    7. **Return** to the terminal window in VS Code.
    8. If prompted, **select** a subscription.

3. Leave the terminal window open for the next steps.

---

## Deploy the Azure Resources

This deployment creates the following resources in your Azure subscription.

- A resource group named **rg-zava-agent-wks-nnnnnnnn**
- An **Azure AI Foundry hub** named **fdy-zava-agent-wks-nnnnnnnn**
- An **Azure AI Foundry project** named **prj-zava-agent-wks-nnnnnnnn**
- Two models are deployed: **gpt-4o-mini** and **text-embedding-3-small**. [See pricing.](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/){:target="\_blank"}
- Azure Database for PostgreSQL Flexible Server (B1ms Burstable 32GB) database named **pg-zava-agent-wks-nnnnnnnn**. [See pricing](https://azure.microsoft.com/pricing/details/postgresql/flexible-server){:target="\_blank"}
- Application Insights resource named **appi-zava-agent-wks-nnnnnnnn**. [See pricing](https://azure.microsoft.com/pricing/calculator/?service=monitor){:target="\_blank"}

!!! warning "Ensure you have at least the following model quotas" - 120K TPM quota for the gpt-4o-mini Global Standard SKU, as the agent makes frequent model calls. - 50K TPM for the text-embedding-3-small model Global Standard SKU. - Check your quota in the [AI Foundry Management Center](https://ai.azure.com/managementCenter/quota){:target="\_blank"}."

### Automated Deployment

Run the following bash script to automate the deployment of the resources required for the workshop. The `deploy.sh` script deploys resources to the `westus` region by default. To run the script:

```bash
cd infra && ./deploy.sh
```

### Workshop Configuration

=== "Python"

    #### Azure Resource Configuration

    The deploy script generates the **.env** file, which contains the project and model endpoints, model deployment names, and Application Insights connection string. The .env file will automatically be saved in the `src/python/workshop` folder.

    Your **.env** file will look similar to the following, updated with your values:

    ```python
    PROJECT_ENDPOINT="<your_project_endpoint>"
    GPT_MODEL_DEPLOYMENT_NAME="<your_model_deployment_name>"
    EMBEDDING_MODEL_DEPLOYMENT_NAME="<your_embedding_model_deployment_name>"
    APPLICATIONINSIGHTS_CONNECTION_STRING="<your_application_insights_connection_string>"
    AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED="true"
    AZURE_OPENAI_ENDPOINT="<your_azure_openai_endpoint>"
    POSTGRES_URL="<your_postgres_connection_string>"
    ```

    #### Azure Resource Names

    You'll also find a file named `resources.txt` in the `workshop` folder. This file contains the names of the Azure resources created during the deployment.

    I'll look similar to the following:

    ```plaintext
    Azure AI Foundry Resources:
    - Resource Group Name: rg-zava-agent-wks-nnnnnnnn
    - AI Project Name: prj-zava-agent-wks-nnnnnnnn
    - Foundry Resource Name: fdy-zava-agent-wks-nnnnnnnn
    - Application Insights Name: appi-zava-agent-wks-nnnnnnnn
    - Postgres Flexible Server Name: pg-zava-agent-wrk-nnnnnnnn
    ```

=== "C#"

    The script securely stores project variables using the Secret Manager for [ASP.NET Core development secrets](https://learn.microsoft.com/aspnet/core/security/app-secrets){:target="_blank"}.

    You can view the secrets by running the following command after you have opened the C# workspace in VS Code:

    ```bash
    dotnet user-secrets list
    ```

---

## Open the VS Code Workspace

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

    ![Lab folder structure](../../media/project-structure-self-guided-python.png)

=== "C#"

    1. In Visual Studio Code, go to **File** > **Open Workspace from File**.
    2. Replace the default path with the following:

        ```text
        /workspace/.vscode/csharp-workspace.code-workspace
        ```

    3. Select **OK** to open the workspace.

    ## Project Structure

    The project uses [Aspire](http://aka.ms/dotnet-aspire) to simplify building the agent application, managing the MCP server, and orchestrating all the external dependencies. The solution is comprised for four projects, all prefixed with `McpAgentWorkshop`:

    * `AppHost`: The Aspire orchestrator, and launch project for the workshop.
    * `McpServer`: The MCP server project.
    * `ServiceDefaults`: Default configuration for services, such as logging and telemetry.
    * `WorkshopApi`: The Agent API for the workshop. The core application logic is in the `AgentService` class.

    In addition to the .NET projects in the solution, there is a `shared` folder (visible as a Solution Folder, and via the file explorer), which contains:

    * `instructions`: The instructions passed to the LLM.
    * `scripts`: Helper shell scripts for various tasks, these will be referred to when required.
    * `webapp`: The front-end client application. Note: This is a Python application, which Aspire will manage the lifecycle of.

    ![Lab folder structure](../../media/project-structure-self-guided-csharp.png)
