## Microsoft Event Deelnemers

De instructies op deze pagina gaan ervan uit dat je deelneemt aan [Microsoft Event 2025](https://build.microsoft.com/){:target="_blank"} en toegang hebt tot een vooraf geconfigureerde lab omgeving. Deze omgeving biedt een Azure abonnement met alle tools en resources die nodig zijn om de workshop te voltooien.

## Introductie

Deze workshop is ontworpen om je te leren over de Azure AI Agents Service en de bijbehorende [SDK](https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme?context=%2Fazure%2Fai-services%2Fagents%2Fcontext%2Fcontext){:target="_blank"}. Het bestaat uit meerdere labs, elk met de nadruk op een specifieke functie van de Azure AI Agents Service. De labs zijn bedoeld om in volgorde te worden voltooid, omdat elk lab voortbouwt op de kennis en het werk van de vorige lab.

## Workshop Programmeertaal Selecteren

De workshop is beschikbaar in zowel Python als C#. Zorg ervoor dat je de taal selecteert die past bij de lab ruimte waarin je je bevindt, door de taalselector tabs te gebruiken. Let op, wissel niet van taal tijdens de workshop.

**Selecteer de taal tab die overeenkomt met je lab ruimte:**

=== "Python"
    De standaardtaal voor de workshop is ingesteld op **Python**.
=== "C#"
    De standaardtaal voor de workshop is ingesteld op **C#**.

## Authenticeren met Azure

Je moet authenticeren met Azure zodat de agent app toegang kan krijgen tot de Azure AI Agents Service en modellen. Volg deze stappen:

1. Open een terminal venster. De terminal app is **vastgemaakt** aan de Windows 11 taakbalk.

    ![Open het terminal venster](../media/windows-taskbar.png){ width="300" }

2. Voer het volgende commando uit om te authenticeren met Azure:

    ```powershell
    az login
    ```

    !!! note
        Je wordt gevraagd om een browser link te openen en in te loggen op je Azure account.

        1. Een browser venster opent automatisch, selecteer **Werk- of schoolaccount** en klik **Volgende**.

        1. Gebruik de **Gebruikersnaam** en **Wachtwoord** die je vindt in de **top sectie** van het **Resources** tabblad in de lab omgeving.

        2. Selecteer **OK**, dan **Klaar**.

3. Selecteer vervolgens het **Standaard** abonnement vanaf de commandoregel, door op **Enter** te klikken.

4. Zodra je bent ingelogd, voer het volgende commando uit om de **user** rol toe te wijzen aan de resource groep:

    ```powershell
    $subId = $(az account show --query id --output tsv) `
    ;$objectId = $(az ad signed-in-user show --query id -o tsv) `
    ; az role assignment create --role "f6c7c914-8db3-469d-8ca1-694a8f32e121" --assignee-object-id $objectId --scope /subscriptions/$subId/resourceGroups/"rg-agent-workshop" --assignee-principal-type 'User'
    ```

5. Laat het terminal venster open voor de volgende stappen.

## De Workshop Openen

Volg deze stappen om de workshop te openen in Visual Studio Code:

=== "Python"

      1. Voer vanuit het terminal venster de volgende commando's uit om de workshop repository te klonen, naar de relevante map te navigeren, een virtuele omgeving op te zetten, deze te activeren en de vereiste pakketten te installeren:

          ```powershell
          git clone https://github.com/microsoft/build-your-first-agent-with-azure-ai-agent-service-workshop.git `
          ; cd build-your-first-agent-with-azure-ai-agent-service-workshop `
          ; python -m venv src/python/workshop/.venv `
          ; src\python\workshop\.venv\Scripts\activate `
          ; pip install -r src/python/workshop/requirements.txt `
          ; code --install-extension tomoki1207.pdf
          ```

      2. Open in VS Code. Voer vanuit het terminal venster het volgende commando uit:

          ```powershell
          code .vscode\python-workspace.code-workspace
          ```

        !!! warning "Wanneer het project opent in VS Code, verschijnen er twee meldingen in de rechteronderhoek. Klik ✖ om beide meldingen te sluiten."

=== "C#"

    1. Voer vanuit een terminal venster de volgende commando's uit om de workshop repository te klonen:

        ```powershell
        git clone https://github.com/microsoft/build-your-first-agent-with-azure-ai-agent-service-workshop.git
        ```

    === "VS Code"

        1. Open de workshop in Visual Studio Code. Voer vanuit het terminal venster het volgende commando uit:

            ```powershell
            code build-your-first-agent-with-azure-ai-agent-service-workshop\.vscode\csharp-workspace.code-workspace
            ```

        !!! note "Wanneer het project opent in VS Code, verschijnt er een melding in de rechteronderhoek om de C# extensie te installeren. Klik **Installeren** om de C# extensie te installeren, omdat dit de benodigde functies voor C# ontwikkeling biedt."

    === "Visual Studio 2022"

        1. Open de workshop in Visual Studio 2022. Voer vanuit het terminal venster het volgende commando uit:

            ```powershell
            start build-your-first-agent-with-azure-ai-agent-service-workshop\src\csharp\workshop\AgentWorkshop.sln
            ```

            !!! note "Je wordt mogelijk gevraagd met welk programma je de oplossing wilt openen. Selecteer **Visual Studio 2022**."

## Azure AI Foundry Project Endpoint

Vervolgens loggen we in op Azure AI Foundry om het project endpoint op te halen, dat de agent app gebruikt om verbinding te maken met de Azure AI Agents Service.

1. Navigeer naar de [Azure AI Foundry](https://ai.azure.com){:target="_blank"} website.
2. Selecteer **Inloggen** en gebruik de **Gebruikersnaam** en **Wachtwoord** die je vindt in de **top sectie** van het **Resources** tabblad in de lab omgeving. Klik op de **Gebruikersnaam** en **Wachtwoord** velden om automatisch de inloggegevens in te vullen.
    ![Azure credentials](../media/azure-credentials.png){:width="500"}
3. Lees de introductie van Azure AI Foundry en klik **Begrepen**.
4. Navigeer naar [Alle Resources](https://ai.azure.com/AllResources){:target="_blank"} om de lijst van AI resources te bekijken die voor je zijn voorbereid.
5. Selecteer de resource naam die begint met **aip-** van type **Project**.

    ![Selecteer project](../media/ai-foundry-project.png){:width="500"}

6. Bekijk de introductiegids en klik **Sluiten**.
7. Zoek in de **Overzicht** zijbalk menu de **Endpoints en sleutels** -> **Bibliotheken** -> **Azure AI Foundry** sectie, klik het **Kopiëren** icoon om het **Azure AI Foundry project endpoint** te kopiëren.

    ![Kopieer connection string](../media/project-connection-string.png){:width="500"}

=== "Python"

    ## De Workshop Configureren

    1. Ga terug naar de workshop die je hebt geopend in VS Code.
    2. **Hernoem** het `.env.sample` bestand naar `.env`.

        - Selecteer het **.env.sample** bestand in het VS Code **Explorer** paneel.
        - Rechtsklik op het bestand en selecteer **Hernoemen**, of druk <kbd>F2</kbd>.
        - Verander de bestandsnaam naar `.env` en druk <kbd>Enter</kbd>.

    3. Plak het **Project endpoint** dat je hebt gekopieerd van Azure AI Foundry in het `.env` bestand.

        ```python
        PROJECT_ENDPOINT="<your_project_endpoint>"
        ```

        Je `.env` bestand zou er ongeveer zo uit moeten zien maar dan met jouw project endpoint.

        ```python
        PROJECT_ENDPOINT="<your_project_endpoint>"
        MODEL_DEPLOYMENT_NAME="<your_model_deployment_name>"
        DEV_TUNNEL_URL="<your_dev_tunnel_url>"
        ```

    4. Sla het `.env` bestand op.

    ## Projectstructuur

    Zorg ervoor dat je vertrouwd raakt met de belangrijkste **submappen** en **bestanden** waarmee je tijdens de workshop zult werken.

    5. Het **app.py** bestand: Het toegangspunt voor de app, met de hoofdlogica.
    6. Het **sales_data.py** bestand: De functielogica om dynamische SQL queries uit te voeren tegen de SQLite database.
    7. Het **stream_event_handler.py** bestand: Bevat de event handler logica voor token streaming.
    8. De **shared/files** map: Bevat de bestanden die door de agent app zijn gemaakt.
    9. De **shared/instructions** map: Bevat de instructies die worden doorgegeven aan het LLM.

    ![Lab mapstructuur](../media/project-structure-self-guided-python.png)

=== "C#"

    ## De Workshop Configureren

    1. Open een terminal en navigeer naar de **src/csharp/workshop/AgentWorkshop.Client** map.

        ```powershell
        cd build-your-first-agent-with-azure-ai-agent-service-workshop\src\csharp\workshop\AgentWorkshop.Client
        ```

    2. Voeg het **Project endpoint** dat je hebt gekopieerd van Azure AI Foundry toe aan de user secrets.

        ```powershell
        dotnet user-secrets set "ConnectionStrings:AiAgentService" "<your_project_endpoint>"
        ```

    3. Voeg de **Model deployment naam** toe aan de user secrets.

        ```powershell
        dotnet user-secrets set "Azure:ModelName" "gpt-4o"
        ```

    4. Voeg de **Bing connection ID** toe aan de user secrets voor grounding met Bing search.

        ```powershell
        $subId = $(az account show --query id --output tsv)
        $rgName = "rg-agent-workshop"
        $aiAccount = "<ai_account_name>" # Vervang met de werkelijke AI account naam
        $aiProject = "<ai_project_name>" # Vervang met de werkelijke AI project naam
        $bingConnectionId = "/subscriptions/$subId/resourceGroups/$rgName/providers/Microsoft.CognitiveServices/accounts/$aiAccount/projects/$aiProject/connections/groundingwithbingsearch"
        dotnet user-secrets set "Azure:BingConnectionId" "$bingConnectionId"
        ```

    ## Projectstructuur

    Zorg ervoor dat je vertrouwd raakt met de belangrijkste **submappen** en **bestanden** waarmee je tijdens de workshop zult werken.

    ### De workshop map

    - De **Lab1.cs, Lab2.cs, Lab3.cs** bestanden: Het toegangspunt voor elke lab, met de agent logica.
    - Het **Program.cs** bestand: Het toegangspunt voor de app, met de hoofdlogica.
    - Het **SalesData.cs** bestand: De functielogica om dynamische SQL queries uit te voeren tegen de SQLite database.

    ### De shared map

    - De **files** map: Bevat de bestanden die door de agent app zijn gemaakt.
    - De **fonts** map: Bevat de meertalige lettertypen die door Code Interpreter worden gebruikt.
    - De **instructions** map: Bevat de instructies die worden doorgegeven aan het LLM.

    ![Lab mapstructuur](../media/project-structure-self-guided-csharp.png)

## Pro Tips

!!! tips
    1. Het **Burger Menu** in het rechter paneel van de lab omgeving biedt aanvullende functies, inclusief de **Split Window View** en de optie om de lab te beëindigen. De **Split Window View** stelt je in staat om de lab omgeving te maximaliseren naar volledig scherm, waardoor de schermruimte wordt geoptimaliseerd. Het **Instructies** en **Resources** paneel van de lab opent in een apart venster.
    2. Als de lab instructies traag scrollen in de lab omgeving, probeer dan de URL van de instructies te kopiëren en deze te openen in **de lokale browser van je computer** voor een vloeiendere ervaring.
    3. Als je moeite hebt met het bekijken van een afbeelding, **klik dan gewoon op de afbeelding om deze te vergroten**.

*Vertaald met behulp van GitHub Copilot.*
