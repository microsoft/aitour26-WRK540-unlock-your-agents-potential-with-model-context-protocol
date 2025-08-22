!!! danger
    Before proceeding, ensure that your Codespace or Dev Container is fully built and ready.

## Authenticate with DevTunnel

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

## Authenticate with Azure

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

## Deploy the Azure Resources

This deployment creates the following resources in your Azure subscription.

- A resource group named **rg-zava-agent-wks-nnnnnnnn**
- An **Azure AI Foundry hub** named **fdy-zava-agent-wks-nnnnnnnn**
- An **Azure AI Foundry project** named **prj-zava-agent-wks-nnnnnnnn**
- Two models are deployed: **gpt-4o-mini** and **text-embedding-3-small**. [See pricing.](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/){:target="_blank"}
- Azure Database for PostgreSQL Flexible Server (B1ms Burstable 32GB) database named **pg-zava-agent-wks-nnnnnnnn**. [See pricing](https://azure.microsoft.com/pricing/details/postgresql/flexible-server){:target="_blank"}
- Application Insights resource named **appi-zava-agent-wks-nnnnnnnn**. [See pricing](https://azure.microsoft.com/pricing/calculator/?service=monitor){:target="_blank"}

!!! warning "Ensure you have at least the following model quotas"
    - 120K TPM quota for the gpt-4o-mini Global Standard SKU, as the agent makes frequent model calls.
    - 50K TPM for the text-embedding-3-small model Global Standard SKU.
    - Check your quota in the [AI Foundry Management Center](https://ai.azure.com/managementCenter/quota){:target="_blank"}."

### Automated Deployment

Run the following bash script to automate the deployment of the resources required for the workshop. The `deploy.sh` script deploys resources to the `westus` region by default. To run the script:

```bash
cd infra && ./deploy.sh
```

<!-- !!! note "On Windows, run `deploy.ps1` instead of `deploy.sh`" -->

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
