## Codespace Build पूरा होने का इंतज़ार करें

आगे बढ़ने से पहले, सुनिश्चित करें कि आपका Codespace या Dev Container पूरी तरह से built और ready है। यह आपके internet connection और download होने वाले resources के आधार पर कई minutes ले सकता है।

## Azure के साथ Authenticate करना

Agent app को Azure AI Agents Service और models तक पहुंच देने के लिए Azure के साथ authenticate करें। इन steps को follow करें:

1. Confirm करें कि workshop environment ready है और VS Code में खुला है।
2. VS Code से, VS Code में **Terminal** > **New Terminal** के माध्यम से terminal खोलें, फिर चलाएं:

    ```shell
    az login --use-device-code
    ```

    !!! note
        आपको browser खोलने और Azure में log in करने के लिए कहा जाएगा। Authentication code copy करें और:

        1. अपना account type चुनें और **Next** पर click करें।
        2. अपनी Azure credentials के साथ sign in करें।
        3. Code को paste करें।
        4. **OK**, फिर **Done** पर click करें।

    !!! warning
        यदि आपके पास multiple Azure tenants हैं, तो सही tenant specify करें:

        ```shell
        az login --use-device-code --tenant <tenant_id>
        ```

3. इसके बाद, command line से appropriate subscription सेलेक्ट करें।
4. अगले steps के लिए terminal window को खुला छोड़ दें।

## Azure Resources Deploy करना

यह deployment आपकी Azure subscription में **rg-zava-agent-wks-nnnn** resource group के under निम्नलिखित resources create करती है:

- **fdy-zava-agent-wks-nnnn** नाम का एक **Azure AI Foundry hub**
- **prj-zava-agent-wks-nnnn** नाम का एक **Azure AI Foundry project**
- दो models deploy किए जाते हैं: **gpt-4o-mini** और **text-embedding-3-small**। [Pricing देखें।](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/){:target="_blank"}

!!! warning "सुनिश्चित करें कि आपके पास gpt-4o-mini Global Standard SKU के लिए कम से कम 120K TPM quota है, क्योंकि agent frequent model calls करता है। [AI Foundry Management Center](https://ai.azure.com/managementCenter/quota){:target="_blank"} में अपना quota check करें।"

हमने workshop के लिए आवश्यक resources की deployment को automate करने के लिए bash script प्रदान की है।

### Automated Deployment

`deploy.sh` script default रूप से `westus` region में resources deploy करती है। Script चलाने के लिए:

```bash
cd infra && ./deploy.sh
```

<!-- !!! note "Windows पर, `deploy.sh` के बजाय `deploy.ps1` चलाएं" -->

### Workshop Configuration

=== "Python"

    #### Azure Resource Configuration

    Deploy script **.env** file generate करती है, जिसमें project और model endpoints, model deployment names, और Application Insights connection string शामिल है। .env file automatically `src/python/workshop` folder में save हो जाएगी।
    
    आपकी **.env** file निम्नलिखित के समान दिखेगी, आपकी values के साथ updated:

    ```python
    PROJECT_ENDPOINT="<your_project_endpoint>"
    GPT_MODEL_DEPLOYMENT_NAME="<your_model_deployment_name>"
    EMBEDDING_MODEL_DEPLOYMENT_NAME="<your_embedding_model_deployment_name>"
    APPLICATIONINSIGHTS_CONNECTION_STRING="<your_application_insights_connection_string>"
    DEV_TUNNEL_URL="<your_dev_tunnel_url>"
    AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED="true"
    AZURE_OPENAI_ENDPOINT="<your_azure_openai_endpoint>"
    ```

    #### Azure Resource Names

    आपको `workshop` folder में `resources.txt` नाम की file भी मिलेगी। इस file में deployment के दौरान create किए गए Azure resources के names शामिल हैं।

    यह निम्नलिखित के समान दिखेगी:

    ```plaintext
    Azure AI Foundry Resources:
    - Resource Group Name: rg-zava-agent-wks-nnnn
    - AI Project Name: prj-zava-agent-wks-nnnn
    - Foundry Resource Name: fdy-zava-agent-wks-nnnn
    - Application Insights Name: appi-zava-agent-wks-nnnn
    ```

=== "C#"

    Script [ASP.NET Core development secrets](https://learn.microsoft.com/aspnet/core/security/app-secrets){:target="_blank"} के लिए Secret Manager का उपयोग करके project variables को securely store करती है।

    VS Code में C# workspace खोलने के बाद आप निम्नलिखित command चलाकर secrets देख सकते हैं:

    ```bash
    dotnet user-secrets list
    ```

*GitHub Copilot का उपयोग करके अनुवादित।*
