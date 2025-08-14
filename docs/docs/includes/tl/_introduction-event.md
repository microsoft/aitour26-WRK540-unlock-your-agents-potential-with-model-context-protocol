## Microsoft Event Attendees

Ang mga instructions sa page na ito ay nagiging assumption na dadalo kayo sa [Microsoft Event 2025](https://build.microsoft.com/){:target="_blank"} at may access sa pre-configured lab environment. Nagbibigay ang environment na ito ng Azure subscription na may lahat ng tools at resources na kailangan upang makompleto ang workshop.

## Introduction

Idinisenyo ang workshop na ito upang turuan kayo tungkol sa Azure AI Agents Service at ang kaugnay na [SDK](https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme?context=%2Fazure%2Fai-services%2Fagents%2Fcontext%2Fcontext){:target="_blank"}. Binubuo ito ng maraming labs, bawat isa ay nag-highlight ng specific feature ng Azure AI Agents Service. Dapat na makompleto ang mga labs nang sunod-sunod, dahil binubuo ng bawat isa ang knowledge at work mula sa nakaraang lab.

## Piliin ang Workshop Programming Language

Available ang workshop sa Python at C#. Pakisiguraduhin na piliin ang language na akma sa lab room na inyong kinalalagyan, sa pamamagitan ng paggamit ng language selector tabs. Tandaan, huwag mag-switch ng languages sa gitna ng workshop.

**Piliin ang language tab na tumugma sa inyong lab room:**

=== "Python"
    Ang default language para sa workshop ay naka-set sa **Python**.
=== "C#"
    Ang default language para sa workshop ay naka-set sa **C#**.

## Mag-authenticate sa Azure

Kailangan ninyong mag-authenticate sa Azure upang ma-access ng agent app ang Azure AI Agents Service at models. Sundin ang mga steps na ito:

1. Buksan ang terminal window. Ang terminal app ay **nakapin** sa Windows 11 taskbar.

    ![Open the terminal window](../media/windows-taskbar.png){ width="300" }

2. Patakbuhin ang sumusunod na command upang mag-authenticate sa Azure:

    ```powershell
    az login
    ```

    !!! note
        Magiging prompted kayo na buksan ang browser link at mag-log in sa inyong Azure account.

        1. Awtomatikong magbubukas ang browser window, piliin ang **Work or school account** at i-click ang **Next**.

        1. Gamitin ang **Username** at **Password** na makikita sa **top section** ng **Resources** tab sa lab environment.

        2. Piliin ang **OK**, pagkatapos **Done**.

3. Pagkatapos ay piliin ang **Default** subscription mula sa command line, sa pamamagitan ng pag-click sa **Enter**.

4. Kapag naka-log in na kayo, patakbuhin ang sumusunod na command upang i-assign ang **user** role sa resource group:

    ```powershell
    $subId = $(az account show --query id --output tsv) `
    ;$objectId = $(az ad signed-in-user show --query id -o tsv) `
    ; az role assignment create --role "f6c7c914-8db3-469d-8ca1-694a8f32e121" --assignee-object-id $objectId --scope /subscriptions/$subId/resourceGroups/"rg-agent-workshop" --assignee-principal-type 'User'
    ```

5. Iwanang bukas ang terminal window para sa susunod na steps.

## Buksan ang Workshop

Sundin ang mga steps na ito upang buksan ang workshop sa Visual Studio Code:

=== "Python"

      1. Mula sa terminal window, i-execute ang sumusunod na commands upang i-clone ang workshop repository, mag-navigate sa relevant folder, mag-set up ng virtual environment, i-activate ito, at i-install ang required packages:

          ```powershell
          git clone https://github.com/microsoft/build-your-first-agent-with-azure-ai-agent-service-workshop.git `
          ; cd build-your-first-agent-with-azure-ai-agent-service-workshop `
          ; python -m venv src/python/workshop/.venv `
          ; src\python\workshop\.venv\Scripts\activate `
          ; pip install -r src/python/workshop/requirements.txt `
          ; code --install-extension tomoki1207.pdf
          ```

      2. Buksan sa VS Code. Mula sa terminal window, patakbuhin ang sumusunod na command:

          ```powershell
          code .vscode\python-workspace.code-workspace
          ```

        !!! warning "Kapag nagbukas ang project sa VS Code, dalawang notifications ang lalabas sa bottom right corner. I-click ang ✖ upang isara ang dalawang notifications."

=== "C#"

    1. Mula sa terminal window, i-execute ang sumusunod na commands upang i-clone ang workshop repository:

        ```powershell
        git clone https://github.com/microsoft/build-your-first-agent-with-azure-ai-agent-service-workshop.git
        ```

    === "VS Code"

        1. Buksan ang workshop sa Visual Studio Code. Mula sa terminal window, patakbuhin ang sumusunod na command:

            ```powershell
            code build-your-first-agent-with-azure-ai-agent-service-workshop\.vscode\csharp-workspace.code-workspace
            ```

        !!! note "Kapag nagbukas ang project sa VS Code, lalabas ang notification sa bottom right corner upang i-install ang C# extension. I-click ang **Install** upang i-install ang C# extension, dahil magbibigay ito ng necessary features para sa C# development."

    === "Visual Studio 2022"

        1. Buksan ang workshop sa Visual Studio 2022. Mula sa terminal window, patakbuhin ang sumusunod na command:

            ```powershell
            start build-your-first-agent-with-azure-ai-agent-service-workshop\src\csharp\workshop\AgentWorkshop.sln
            ```

            !!! note "Maaaring magtanong kung anong program ang gagamitin upang buksan ang solution. Piliin ang **Visual Studio 2022**."

## Azure AI Foundry Project Endpoint

Susunod, mag-log in tayo sa Azure AI Foundry upang kunin ang project endpoint, na ginagamit ng agent app upang kumonekta sa Azure AI Agents Service.

1. Pumunta sa [Azure AI Foundry](https://ai.azure.com){:target="_blank"} website.
2. Piliin ang **Sign in** at gamitin ang **Username** at **Password** na makikita sa **top section** ng **Resources** tab sa lab environment. I-click ang **Username** at **Password** fields upang awtomatikong ma-fill in ang login details.
    ![Azure credentials](../media/azure-credentials.png){:width="500"}
3. Basahin ang introduction sa Azure AI Foundry at i-click ang **Got it**.
4. Pumunta sa [All Resources](https://ai.azure.com/AllResources){:target="_blank"} upang tingnan ang listahan ng AI resources na na-pre-provision para sa inyo.
5. Piliin ang resource name na nagsisimula sa **aip-** na may type na **Project**.

    ![Select project](../media/ai-foundry-project.png){:width="500"}

6. Suriin ang introduction guide at i-click ang **Close**.
7. Mula sa **Overview** sidebar menu, hanapin ang **Endpoints and keys** -> **Libraries** -> **Azure AI Foundry** section, i-click ang **Copy** icon upang i-copy ang **Azure AI Foundry project endpoint**.

    ![Copy connection string](../media/project-connection-string.png){:width="500"}

=== "Python"

    ## I-configure ang Workshop

    1. Bumalik sa workshop na binuksan ninyo sa VS Code.
    2. **I-rename** ang `.env.sample` file sa `.env`.

        - Piliin ang **.env.sample** file sa VS Code **Explorer** panel.
        - I-right-click ang file at piliin ang **Rename**, o pindutin ang <kbd>F2</kbd>.
        - Baguhin ang file name sa `.env` at pindutin ang <kbd>Enter</kbd>.

    3. I-paste ang **Project endpoint** na kinopya ninyo mula sa Azure AI Foundry sa `.env` file.

        ```python
        PROJECT_ENDPOINT="<your_project_endpoint>"
        ```

        Ang inyong `.env` file ay dapat maging katulad nito pero na may inyong project endpoint.

        ```python
        PROJECT_ENDPOINT="<your_project_endpoint>"
        MODEL_DEPLOYMENT_NAME="<your_model_deployment_name>"
        DEV_TUNNEL_URL="<your_dev_tunnel_url>"
        ```

    4. I-save ang `.env` file.

    ## Project Structure

    Siguraduhing pamilyaruhin ang sarili sa mga key **subfolders** at **files** na gagamitin ninyo sa buong workshop.

    5. Ang **app.py** file: Ang entry point para sa app, na naglalaman ng main logic nito.
    6. Ang **sales_data.py** file: Ang function logic upang mag-execute ng dynamic SQL queries laban sa SQLite database.
    7. Ang **stream_event_handler.py** file: Naglalaman ng event handler logic para sa token streaming.
    8. Ang **shared/files** folder: Naglalaman ng mga files na ginawa ng agent app.
    9. Ang **shared/instructions** folder: Naglalaman ng mga instructions na ipinasa sa LLM.

    ![Lab folder structure](../media/project-structure-self-guided-python.png)

=== "C#"

    ## I-configure ang Workshop

    1. Buksan ang terminal at mag-navigate sa **src/csharp/workshop/AgentWorkshop.Client** folder.

        ```powershell
        cd build-your-first-agent-with-azure-ai-agent-service-workshop\src\csharp\workshop\AgentWorkshop.Client
        ```

    2. Idagdag ang **Project endpoint** na kinopya ninyo mula sa Azure AI Foundry sa user secrets.

        ```powershell
        dotnet user-secrets set "ConnectionStrings:AiAgentService" "<your_project_endpoint>"
        ```

    3. Idagdag ang **Model deployment name** sa user secrets.

        ```powershell
        dotnet user-secrets set "Azure:ModelName" "gpt-4o"
        ```

    4. Idagdag ang **Bing connection ID** sa user secrets para sa grounding gamit ang Bing search.

        ```powershell
        $subId = $(az account show --query id --output tsv)
        $rgName = "rg-agent-workshop"
        $aiAccount = "<ai_account_name>" # Palitan ng actual AI account name
        $aiProject = "<ai_project_name>" # Palitan ng actual AI project name
        $bingConnectionId = "/subscriptions/$subId/resourceGroups/$rgName/providers/Microsoft.CognitiveServices/accounts/$aiAccount/projects/$aiProject/connections/groundingwithbingsearch"
        dotnet user-secrets set "Azure:BingConnectionId" "$bingConnectionId"
        ```

    ## Project Structure

    Siguraduhing pamilyaruhin ang sarili sa mga key **subfolders** at **files** na gagamitin ninyo sa buong workshop.

    ### Ang workshop folder

    - Ang **Lab1.cs, Lab2.cs, Lab3.cs** files: Ang entry point para sa bawat lab, na naglalaman ng agent logic nito.
    - Ang **Program.cs** file: Ang entry point para sa app, na naglalaman ng main logic nito.
    - Ang **SalesData.cs** file: Ang function logic upang mag-execute ng dynamic SQL queries laban sa SQLite database.

    ### Ang shared folder

    - Ang **files** folder: Naglalaman ng mga files na ginawa ng agent app.
    - Ang **fonts** folder: Naglalaman ng mga multilingual fonts na ginagamit ng Code Interpreter.
    - Ang **instructions** folder: Naglalaman ng mga instructions na ipinasa sa LLM.

    ![Lab folder structure](../media/project-structure-self-guided-csharp.png)

## Pro Tips

!!! tips
    1. Ang **Burger Menu** sa right-hand panel ng lab environment ay nag-aalok ng additional features, kasama ang **Split Window View** at ang option na tapusin ang lab. Ang **Split Window View** ay nagbibigay-daan sa inyo na i-maximize ang lab environment sa full screen, na nag-optimize ng screen space. Ang **Instructions** at **Resources** panel ng lab ay magbubukas sa hiwalay na window.
    2. Kung mabagal ang scroll ng lab instructions sa lab environment, subukan ninyong kopyahin ang URL ng instructions at buksan ito sa **local browser ng inyong computer** para sa smoother experience.
    3. Kung may problema kayo sa pagtingin sa image, i-click lang ang **image upang palakihin ito**.

*Isinalin gamit ang GitHub Copilot.*
