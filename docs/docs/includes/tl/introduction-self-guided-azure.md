!!! danger 
    Bago magpatuloy, tiyaking ang iyong Codespace o Dev Container ay ganap na na-build at handa na.

## Mag-authenticate sa Azure

Mag-authenticate sa Azure upang payagan ang agent app na ma-access ang Azure AI Agents Service at mga model. Sundin ang mga hakbang na ito:

1. Mula sa VS Code, **pindutin** ang <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>`</kbd> upang magbukas ng bagong terminal window. Pagkatapos patakbuhin ang sumusunod na command:

    ```shell
    az login --use-device-code
    ```

    !!! warning
        Kung mayroon kang maraming Azure tenants, tukuyin ang tamang isa gamit:

        ```shell
        az login --use-device-code --tenant <tenant_id>
        ```

2. Sundin ang mga hakbang na ito upang mag-authenticate:

    1. **Kopyahin** ang **Authentication Code** sa clipboard.
    2. **Pindutin at hawakan** ang <kbd>ctrl</kbd> o <kbd>cmd</kbd> key.
    3. **Piliin** ang authentication URL upang buksan ito sa iyong browser.
    4. **I-paste** ang code at i-click ang **Next**.
    5. **Pumili ng account** at mag-sign in.
    6. Piliin ang **Continue**
    7. **Bumalik** sa terminal window sa VS Code.
    8. Kung na-prompt, **piliin** ang isang subscription.

3. Iwanang bukas ang terminal window para sa susunod na mga hakbang.

## I-deploy ang Azure Resources

Gumagawa ang deployment na ito ng mga sumusunod na resource sa iyong Azure subscription.

- Isang resource group na pinangalanang **rg-zava-agent-wks-nnnn**
- Isang **Azure AI Foundry hub** na pinangalanang **fdy-zava-agent-wks-nnnn**
- Isang **Azure AI Foundry project** na pinangalanang **prj-zava-agent-wks-nnnn**
- Dalawang modelo ang na-deploy: **gpt-4o-mini** at **text-embedding-3-small**. [Tingnan ang pricing.](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/){:target="_blank"}

!!! warning "Tiyaking mayroon kang hindi bababa sa sumusunod na mga model quota"
    - 120K TPM quota para sa gpt-4o-mini Global Standard SKU, dahil madalas gumawa ng model calls ang agent.
    - 50K TPM para sa text-embedding-3-small model Global Standard SKU.
    - Suriin ang iyong quota sa [AI Foundry Management Center](https://ai.azure.com/managementCenter/quota){:target="_blank"}."

### Automated Deployment

Patakbuhin ang sumusunod na bash script upang i-automate ang deployment ng mga resource na kailangan para sa workshop. Ang `deploy.sh` script ay nagde-deploy ng resources sa `westus` region bilang default. Upang patakbuhin ang script:

```bash
d cd infra && ./deploy.sh
```

<!-- !!! note "Sa Windows, patakbuhin ang `deploy.ps1` sa halip na `deploy.sh`" -->

### Workshop Configuration

=== "Python"

    #### Azure Resource Configuration

    Ginagawa ng deploy script ang **.env** file, na naglalaman ng project at model endpoints, model deployment names, at Application Insights connection string. Awtomatikong mase-save ang .env file sa `src/python/workshop` folder. 
    
    Ang iyong **.env** file ay magiging kahawig ng sumusunod, na may sarili mong mga value:

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

    Makakakita ka rin ng file na pinangalanang `resources.txt` sa `workshop` folder. Ang file na ito ay naglalaman ng mga pangalan ng Azure resources na nalikha sa panahon ng deployment. 

    Magiging katulad ito ng sumusunod:

    ```plaintext
    Azure AI Foundry Resources:
    - Resource Group Name: rg-zava-agent-wks-nnnn
    - AI Project Name: prj-zava-agent-wks-nnnn
    - Foundry Resource Name: fdy-zava-agent-wks-nnnn
    - Application Insights Name: appi-zava-agent-wks-nnnn
    ```

=== "C#"

    Sine-secure ng script ang project variables gamit ang Secret Manager para sa [ASP.NET Core development secrets](https://learn.microsoft.com/aspnet/core/security/app-secrets){:target="_blank"}.

    Maaari mong tingnan ang mga secret sa pamamagitan ng pagpapatakbo ng sumusunod na command pagkatapos mong buksan ang C# workspace sa VS Code:

    ```bash
    dotnet user-secrets list
    ```

*Isinalin gamit ang GitHub Copilot.*
