## What You'll Learn

In this section, you'll learn how to:

- Authenticate with Azure
- Deploy Azure resources for the workshop
- Configure the workshop environment

## Authenticate with Azure

You need to authenticate with Azure so the agent app can access the Azure AI Agents Service and models. Follow these steps:

1. Ensure the Codespace has been created.
1. In the Codespace, open a new terminal window by selecting **Terminal** > **New Terminal** from the **VS Code menu**.
1. Run the following command to authenticate with Azure:

    ```shell
    az login --use-device-code
    ```

    !!! note
        You'll be prompted to open a browser link and log in to your Azure account. Be sure to copy the authentication code first.

        1. A browser window will open automatically, select your account type and click **Next**.
        2. Sign in with your Azure subscription **Username** and **Password**.
        3. **Paste** the authentication code.
        4. Select **OK**, then **Done**.

    !!! warning
        If you have multiple Azure tenants, then you will need to select the appropriate tenant when authenticating.

        ```shell
        az login --use-device-code --tenant <tenant_id>
        ```

1. Next, select the appropriate subscription from the command line.
1. Leave the terminal window open for the next steps.

## Deploy the Azure Resources

The following resources will be created in the **rg-zava-agent-wks-nnnn** resource group in your Azure subscription.

- An **Azure AI Foundry hub** named **fdy-zava-agent-wks-nnnn**
- An **Azure AI Foundry project** named **prj-zava-agent-wks-nnnn**
- **Serverless (pay-as-you-go) Models**:
    - GPT-4o Mini model deployment named **gpt-4o-mini**. 
    - Text-embedding-3-small model named **text-embedding-3-small**.
    - See pricing details [here](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/){:target="_blank"}.

!!! warning "You will need 120K TPM quota availability for the gpt-4o Global Standard SKU, due to the frequency of calls made by the agent to the model. Review your quota availability in the [AI Foundry Management Center](https://ai.azure.com/managementCenter/quota){:target="_blank"}."

We have provided a bash script to automate the deployment of the resources required for the workshop. Alternatively, you may deploy resources manually using Azure AI Foundry studio. Select the desired tab.

### Automated Deployment

The `deploy.sh` script deploys resources to the `westus` region by default. To run the script, open the VS Code terminal and run the following command:

```bash
cd infra && ./deploy.sh
```

<!-- !!! note "On Windows, run `deploy.ps1` instead of `deploy.sh`" -->

### Workshop Configuration

=== "Python"

    The deploy script generates the **.env** file, which contains the project endpoint, model deployment name, and Bing connection name. 
    
    You'll see this file when you open the Python workspace in VS Code. Your **.env** file will look similar to this but with your project endpoint.

    ```python
    PROJECT_ENDPOINT="<your_project_endpoint>"
    GPT_MODEL_DEPLOYMENT_NAME="<your_model_deployment_name>"
    EMBEDDING_MODEL_DEPLOYMENT_NAME="<your_embedding_model_deployment_name>"
    APPLICATIONINSIGHTS_CONNECTION_STRING="<your_application_insights_connection_string>"
    DEV_TUNNEL_URL="<your_dev_tunnel_url>"
    ```
=== "C#"

    The automated deployment script stores project variables securely by using the Secret Manager feature for [safe storage of app secrets in development in ASP.NET Core](https://learn.microsoft.com/aspnet/core/security/app-secrets){:target="_blank"}.

    You can view the secrets by running the following command after you have opened the C# workspace in VS Code:

    ```bash
    dotnet user-secrets list
    ```

