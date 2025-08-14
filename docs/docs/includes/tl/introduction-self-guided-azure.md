!!! danger 
    Bago magpatuloy, tiyaking ang inyong Codespace o Dev Container ay fully built at ready na.

## Mag-authenticate sa Azure

Mag-authenticate sa Azure upang payagan ang agent app na ma-access ang Azure AI Agents Service at models. Sundin ang mga steps na ito:

1. Mula sa VS Code, **pindutin** ang <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>`</kbd> upang buksan ang bagong terminal window. Pagkatapos patakbuhin ang sumusunod na command:

    ```shell
    az login --use-device-code
    ```

    !!! warning
        Kung mayroon kayong multiple Azure tenants, tukuyin ang tamang tenant gamit ang:

        ```shell
        az login --use-device-code --tenant <tenant_id>
        ```

2. Sundin ang mga steps na ito upang mag-authenticate:

    1. **I-copy** ang **Authentication Code** sa clipboard.
    2. **I-press at hold** ang <kbd>ctrl</kbd> o <kbd>cmd</kbd> key.
    3. **Piliin** ang authentication URL upang buksan ito sa inyong browser.
    4. **I-paste** ang code at i-click ang **Next**.
    5. **Pumili ng account** at mag-sign in.
    6. Piliin ang **Continue**
    7. **Bumalik** sa terminal window sa VS Code.
    8. Kung may prompt, **piliin** ang subscription.

3. Iwanang bukas ang terminal window para sa susunod na steps.

## I-deploy ang Azure Resources

Lumilikha ang deployment na ito ng mga sumusunod na resources sa inyong Azure subscription.

- Isang resource group na nagngangalang **rg-zava-agent-wks-nnnn**
- Isang **Azure AI Foundry hub** na nagngangalang **fdy-zava-agent-wks-nnnn**
- Isang **Azure AI Foundry project** na nagngangalang **prj-zava-agent-wks-nnnn**
- Dalawang models ang na-deploy: **gpt-4o-mini** at **text-embedding-3-small**. [Tingnan ang pricing.](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/){:target="_blank"}

!!! warning "Tiyaking mayroon kayo ng hindi bababa sa sumusunod na model quotas"
    - 120K TPM quota para sa gpt-4o-mini Global Standard SKU, dahil madalas na tumatawag ang agent sa model.
    - 50K TPM para sa text-embedding-3-small model Global Standard SKU.
    - Suriin ang inyong quota sa [AI Foundry Management Center](https://ai.azure.com/managementCenter/quota){:target="_blank"}."

### Automated Deployment

Patakbuhin ang sumusunod na bash script upang i-automate ang deployment ng mga resources na kailangan para sa workshop. Ang `deploy.sh` script ay nag-deploy ng resources sa `westus` region by default. Upang patakbuhin ang script:

```bash
cd infra && ./deploy.sh
```

<!-- !!! note "On Windows, run `deploy.ps1` instead of `deploy.sh`" -->

### Workshop Configuration

=== "Python"

    #### Azure Resource Configuration

    Ginagawa ng deploy script ang **.env** file, na naglalaman ng project at model endpoints, model deployment names, at Application Insights connection string. Awtomatikong ma-save ang .env file sa `src/python/workshop` folder. 
    
    Ang inyong **.env** file ay magiging katulad ng sumusunod, na updated na may inyong values:

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

    Makakakita rin kayo ng file na nagngangalang `resources.txt` sa `workshop` folder. Naglalaman ang file na ito ng mga pangalan ng Azure resources na ginawa sa panahon ng deployment. 

    Magiging katulad ito ng sumusunod:

    ```plaintext
    Azure AI Foundry Resources:
    - Resource Group Name: rg-zava-agent-wks-nnnn
    - AI Project Name: prj-zava-agent-wks-nnnn
    - Foundry Resource Name: fdy-zava-agent-wks-nnnn
    - Application Insights Name: appi-zava-agent-wks-nnnn
    ```

=== "C#"

    Secure na nagtitimbak ang script ng project variables gamit ang Secret Manager para sa [ASP.NET Core development secrets](https://learn.microsoft.com/aspnet/core/security/app-secrets){:target="_blank"}.

    Maaari ninyong tingnan ang secrets sa pamamagitan ng pagpapatakbo ng sumusunod na command pagkatapos ninyong buksan ang C# workspace sa VS Code:

    ```bash
    dotnet user-secrets list
    ```

*Isinalin gamit ang GitHub Copilot.*
