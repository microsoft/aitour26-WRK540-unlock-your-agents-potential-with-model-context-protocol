## Wacht tot Codespace Build Voltooid is

Voordat je verder gaat, zorg ervoor dat je Codespace of Dev Container volledig is gebouwd en klaar is. Dit kan enkele minuten duren, afhankelijk van je internetverbinding en de resources die worden gedownload.

## Authenticeren met Azure

Authenticeer met Azure om de agent app toegang te geven tot de Azure AI Agents Service en modellen. Volg deze stappen:

1. Bevestig dat de workshop omgeving klaar is en geopend in VS Code.
2. Open vanuit VS Code een terminal via **Terminal** > **New Terminal** in VS Code, voer dan uit:

    ```shell
    az login --use-device-code
    ```

    !!! note
        Je wordt gevraagd om een browser te openen en in te loggen op Azure. Kopieer de authenticatiecode en:

        1. Kies je accounttype en klik **Volgende**.
        2. Log in met je Azure credentials.
        3. Plak de code.
        4. Klik **OK**, dan **Klaar**.

    !!! warning
        Als je meerdere Azure tenants hebt, specificeer dan de juiste met:

        ```shell
        az login --use-device-code --tenant <tenant_id>
        ```

3. Selecteer vervolgens het juiste abonnement vanaf de commandoregel.
4. Laat het terminal venster open voor de volgende stappen.

## De Azure Resources Implementeren

Deze implementatie creëert de volgende resources in je Azure abonnement onder de **rg-zava-agent-wks-nnnn** resource groep:

- Een **Azure AI Foundry hub** genaamd **fdy-zava-agent-wks-nnnn**
- Een **Azure AI Foundry project** genaamd **prj-zava-agent-wks-nnnn**
- Twee modellen worden geïmplementeerd: **gpt-4o-mini** en **text-embedding-3-small**. [Zie prijzen.](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/){:target="_blank"}

!!! warning "Zorg ervoor dat je minstens 120K TPM quota hebt voor de gpt-4o-mini Global Standard SKU, omdat de agent frequente model aanroepen doet. Controleer je quota in het [AI Foundry Management Center](https://ai.azure.com/managementCenter/quota){:target="_blank"}."

We hebben een bash script voorzien om de implementatie van de resources die nodig zijn voor de workshop te automatiseren.

### Geautomatiseerde Implementatie

Het `deploy.sh` script implementeert resources naar de `westus` regio standaard. Om het script uit te voeren:

```bash
cd infra && ./deploy.sh
```

<!-- !!! note "Op Windows, voer `deploy.ps1` uit in plaats van `deploy.sh`" -->

### Workshop Configuratie

=== "Python"

    #### Azure Resource Configuratie

    Het deploy script genereert het **.env** bestand, dat de project en model endpoints, model implementatie namen en Application Insights connection string bevat. Het .env bestand wordt automatisch opgeslagen in de `src/python/workshop` map.
    
    Je **.env** bestand zal er ongeveer zo uitzien, bijgewerkt met jouw waarden:

    ```python
    PROJECT_ENDPOINT="<your_project_endpoint>"
    GPT_MODEL_DEPLOYMENT_NAME="<your_model_deployment_name>"
    EMBEDDING_MODEL_DEPLOYMENT_NAME="<your_embedding_model_deployment_name>"
    APPLICATIONINSIGHTS_CONNECTION_STRING="<your_application_insights_connection_string>"
    DEV_TUNNEL_URL="<your_dev_tunnel_url>"
    AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED="true"
    AZURE_OPENAI_ENDPOINT="<your_azure_openai_endpoint>"
    ```

    #### Azure Resource Namen

    Je vindt ook een bestand genaamd `resources.txt` in de `workshop` map. Dit bestand bevat de namen van de Azure resources die zijn gemaakt tijdens de implementatie.

    Het zal er ongeveer zo uitzien:

    ```plaintext
    Azure AI Foundry Resources:
    - Resource Group Name: rg-zava-agent-wks-nnnn
    - AI Project Name: prj-zava-agent-wks-nnnn
    - Foundry Resource Name: fdy-zava-agent-wks-nnnn
    - Application Insights Name: appi-zava-agent-wks-nnnn
    ```


=== "C#"

    Het script slaat project variabelen veilig op met behulp van de Secret Manager voor [ASP.NET Core development secrets](https://learn.microsoft.com/aspnet/core/security/app-secrets){:target="_blank"}.

    Je kunt de secrets bekijken door het volgende commando uit te voeren nadat je de C# workspace hebt geopend in VS Code:

    ```bash
    dotnet user-secrets list
    ```

*Vertaald met behulp van GitHub Copilot.*
