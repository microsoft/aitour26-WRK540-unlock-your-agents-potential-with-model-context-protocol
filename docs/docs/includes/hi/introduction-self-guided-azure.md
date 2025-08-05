## Codespace Build पूरा होने की प्रतीक्षा करें

आगे बढ़ने से पहले, सुनिश्चित करें कि आपका Codespace या Dev Container पूरी तरह से बनाया गया है और तैयार है। यह आपके इंटरनेट कनेक्शन और डाउनलोड किए जा रहे संसाधनों के आधार पर कई मिनट लग सकते हैं।

## Azure के साथ प्रमाणीकरण

एजेंट ऐप को Azure AI Agents Service और models तक पहुंच की अनुमति देने के लिए Azure के साथ प्रमाणीकरण करें। इन चरणों का पालन करें:

1. पुष्टि करें कि कार्यशाला वातावरण तैयार है और VS Code में खुला है।
2. VS Code से, VS Code में **Terminal** > **New Terminal** के माध्यम से एक टर्मिनल खोलें, फिर चलाएं:

    ```shell
    az login --use-device-code
    ```

    !!! note
        आपको एक ब्राउज़र खोलने और Azure में लॉग इन करने के लिए कहा जाएगा। authentication code कॉपी करें और:

        1. अपने account type का चयन करें और **Next** पर क्लिक करें।
        2. अपने Azure credentials के साथ sign in करें।
        3. Code पेस्ट करें।
        4. **OK**, फिर **Done** पर क्लिक करें।

    !!! warning
        यदि आपके पास कई Azure tenants हैं, तो सही वाले को निर्दिष्ट करने के लिए उपयोग करें:

        ```shell
        az login --use-device-code --tenant <tenant_id>
        ```

3. इसके बाद, command line से उपयुक्त subscription का चयन करें।
4. अगले चरणों के लिए टर्मिनल विंडो खुली छोड़ें।

## Azure Resources तैनात करें

यह deployment आपकी Azure subscription में **rg-zava-agent-wks-nnnn** resource group के तहत निम्नलिखित संसाधन बनाती है:

- **fdy-zava-agent-wks-nnnn** नाम का एक **Azure AI Foundry hub**
- **prj-zava-agent-wks-nnnn** नाम का एक **Azure AI Foundry project**
- दो models तैनात किए गए हैं: **gpt-4o-mini** और **text-embedding-3-small**। [मूल्य निर्धारण देखें।](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/){:target="_blank"}

!!! warning "सुनिश्चित करें कि आपके पास gpt-4o-mini Global Standard SKU के लिए कम से कम 120K TPM quota है, क्योंकि एजेंट बार-बार model calls करता है। [AI Foundry Management Center](https://ai.azure.com/managementCenter/quota){:target="_blank"} में अपना quota जांचें।"

हमने कार्यशाला के लिए आवश्यक संसाधनों की तैनाती को automate करने के लिए एक bash script प्रदान की है।

### स्वचालित तैनाती

`deploy.sh` script डिफ़ॉल्ट रूप से `westus` region में resources तैनात करती है। script चलाने के लिए:

```bash
cd infra && ./deploy.sh
```

<!-- !!! note "Windows पर, `deploy.sh` के बजाय `deploy.ps1` चलाएं" -->

### कार्यशाला कॉन्फ़िगरेशन

=== "Python"

    #### Azure Resource कॉन्फ़िगरेशन

    Deploy script **.env** फाइल जेनरेट करती है, जिसमें project और model endpoints, model deployment names, और Application Insights connection string शामिल हैं। .env फाइल स्वचालित रूप से `src/python/workshop` फोल्डर में सेव हो जाएगी। 
    
    आपकी **.env** फाइल निम्नलिखित के समान दिखेगी, आपकी values के साथ अपडेट की गई:

    ```python
    PROJECT_ENDPOINT="<your_project_endpoint>"
    GPT_MODEL_DEPLOYMENT_NAME="<your_model_deployment_name>"
    EMBEDDING_MODEL_DEPLOYMENT_NAME="<your_embedding_model_deployment_name>"
    APPLICATIONINSIGHTS_CONNECTION_STRING="<your_application_insights_connection_string>"
    DEV_TUNNEL_URL="<your_dev_tunnel_url>"
    AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED="true"
    AZURE_OPENAI_ENDPOINT="<your_azure_openai_endpoint>"
    ```

    #### Azure Resource नाम

    आपको `workshop` फोल्डर में `resources.txt` नाम की एक फाइल भी मिलेगी। इस फाइल में deployment के दौरान बनाए गए Azure resources के नाम हैं। 

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

    VS Code में C# workspace खोलने के बाद आप निम्नलिखित कमांड चलाकर secrets देख सकते हैं:

    ```bash
    dotnet user-secrets list
    ```

*GitHub Copilot और GPT-4o का उपयोग करके अनुवादित।*
