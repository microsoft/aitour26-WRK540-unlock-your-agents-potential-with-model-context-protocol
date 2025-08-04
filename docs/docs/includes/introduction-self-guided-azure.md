## Wait for Codespace Build to Complete

Before proceeding, ensure that your Codespace or Dev Container is fully built and ready. This may take several minutes, depending on your internet connection and the resources being downloaded.

## Authenticate with Azure

Authenticate with Azure to allow the agent app access to the Azure AI Agents Service and models. Follow these steps:

1. Confirm the workshop environment is ready and open in VS Code.
2. From VS Code, open a terminal via **Terminal** > **New Terminal** in VS Code, then run:

    ```shell
    az login --use-device-code
    ```

    !!! note
        You'll be prompted to open a browser and log in to Azure. Copy the authentication code and:

        1. Choose your account type and click **Next**.
        2. Sign in with your Azure credentials.
        3. Paste the code.
        4. Click **OK**, then **Done**.

    !!! warning
        If you have multiple Azure tenants, specify the correct one using:

        ```shell
        az login --use-device-code --tenant <tenant_id>
        ```

3. Next, select the appropriate subscription from the command line.
4. Leave the terminal window open for the next steps.

## Deploy the Azure Resources

This deployment creates the following resources in your Azure subscription under the **rg-zava-agent-wks-nnnn** resource group:

- An **Azure AI Foundry hub** named **fdy-zava-agent-wks-nnnn**
- An **Azure AI Foundry project** named **prj-zava-agent-wks-nnnn**
- Two models are deployed: **gpt-4o-mini** and **text-embedding-3-small**. [See pricing.](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/){:target="_blank"}

!!! warning "Ensure you have at least 120K TPM quota for the gpt-4o-mini Global Standard SKU, as the agent makes frequent model calls. Check your quota in the [AI Foundry Management Center](https://ai.azure.com/managementCenter/quota){:target="_blank"}."

We have provided a bash script to automate the deployment of the resources required for the workshop.

### Automated Deployment

The `deploy.sh` script deploys resources to the `westus` region by default. To run the script:

```bash
cd infra && ./deploy.sh
```

<!-- !!! note "On Windows, run `deploy.ps1` instead of `deploy.sh`" -->

### Workshop Configuration

=== "Python"

    The deploy script generates the **.env** file, which contains the project and model endpoints, model deployment names, and Application Insights connection string. The .env file will automatically be saved in the `src/python/workshop` folder. 
    
    Your **.env** file will look similar to the following, updated with your values:

    ```python
    PROJECT_ENDPOINT="<your_project_endpoint>"
    GPT_MODEL_DEPLOYMENT_NAME="<your_model_deployment_name>"
    EMBEDDING_MODEL_DEPLOYMENT_NAME="<your_embedding_model_deployment_name>"
    APPLICATIONINSIGHTS_CONNECTION_STRING="<your_application_insights_connection_string>"
    DEV_TUNNEL_URL="<your_dev_tunnel_url>"
    AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED="true"
    AZURE_OPENAI_ENDPOINT="<your_azure_openai_endpoint>"
    ```
=== "C#"

    The script securely stores project variables using the Secret Manager for [ASP.NET Core development secrets](https://learn.microsoft.com/aspnet/core/security/app-secrets){:target="_blank"}.

    You can view the secrets by running the following command after you have opened the C# workspace in VS Code:

    ```bash
    dotnet user-secrets list
    ```
