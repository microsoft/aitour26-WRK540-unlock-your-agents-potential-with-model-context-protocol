!!! danger 
    आगे बढ़ने से पहले सुनिश्चित करें आपका Codespace या Dev Container पूरी तरह बना है।

## Azure के साथ प्रमाणन

Azure AI Agents Service और मॉडल तक पहुँच हेतु लॉगिन:

1. VS Code में नया टर्मिनल (<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>`</kbd>) और चलाएँ:

    ```shell
    az login --use-device-code
    ```

    !!! warning
        कई टेनेंट हों तो:

        ```shell
        az login --use-device-code --tenant <tenant_id>
        ```

2. चरण:
    1. **Authentication Code** कॉपी।
    2. <kbd>ctrl/cmd</kbd> दबाए रखें।
    3. URL खोलें।
    4. कोड पेस्ट → **Next**।
    5. खाता चुनें, साइन इन।
    6. **Continue**।
    7. टर्मिनल पर लौटें।
    8. सब्सक्रिप्शन चुनें (यदि पूछा जाए)।

3. टर्मिनल खुला छोड़ें।

## Azure संसाधन परिनियोजन

यह स्क्रिप्ट बनाएगी:

- Resource group **rg-zava-agent-wks-nnnn**
- **Azure AI Foundry hub** fdy-zava-agent-wks-nnnn
- **Azure AI Foundry project** prj-zava-agent-wks-nnnn
- मॉडल: **gpt-4o-mini**, **text-embedding-3-small** ([Pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/){:target="_blank"})

!!! warning "न्यूनतम कोटा"
    - gpt-4o-mini: 120K TPM
    - text-embedding-3-small: 50K TPM
    - कोटा देखें: [AI Foundry Management Center](https://ai.azure.com/managementCenter/quota){:target="_blank"}

### स्वचालित परिनियोजन

=== "Linux/Mac OS"

    ```bash
    cd infra && ./deploy.sh
    ```

=== "Windows"

    ```powershell
    cd infra && .\deploy.ps1
    ```

### वर्कशॉप कॉन्फ़िगरेशन

=== "Python"

    #### Azure संसाधन कॉन्फ़िगरेशन

    स्क्रिप्ट `.env` फ़ाइल बनाती है (प्रोजेक्ट एंडपॉइंट, मॉडल डिप्लॉयमेंट, App Insights, आदि)। उदाहरण:

    ```python
    PROJECT_ENDPOINT="<your_project_endpoint>"
    GPT_MODEL_DEPLOYMENT_NAME="<your_model_deployment_name>"
    EMBEDDING_MODEL_DEPLOYMENT_NAME="<your_embedding_model_deployment_name>"
    APPLICATIONINSIGHTS_CONNECTION_STRING="<your_application_insights_connection_string>"
    DEV_TUNNEL_URL="<your_dev_tunnel_url>"
    AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED="true"
    AZURE_OPENAI_ENDPOINT="<your_azure_openai_endpoint>"
    ```

    #### Azure संसाधन नाम

    `resources.txt` में नाम सूचीबद्ध:

    ```plaintext
    - Resource Group Name: rg-zava-agent-wks-nnnn
    - AI Project Name: prj-zava-agent-wks-nnnn
    - Foundry Resource Name: fdy-zava-agent-wks-nnnn
    - Application Insights Name: appi-zava-agent-wks-nnnn
    ```

=== "C#"

    Secret Manager द्वारा कॉन्फ़िग मान सुरक्षित।

    देखने हेतु:

    ```bash
    dotnet user-secrets list
    ```

*GitHub Copilot द्वारा अनुवादित.*
