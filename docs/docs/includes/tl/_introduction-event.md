## Mga Dumadalo sa Microsoft Event

Ipinapalagay ng mga instruction sa pahinang ito na dumadalo ka sa [Microsoft Event 2025](https://build.microsoft.com/){:target="_blank"} at may access sa isang pre-configured na lab environment. Nagbibigay ang environment na ito ng isang Azure subscription na may lahat ng tools at resources na kailangan upang kumpletuhin ang workshop.

## Panimula

Dinisenyo ang workshop na ito upang turuan ka tungkol sa Azure AI Agents Service at kaugnay na [SDK](https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme?context=%2Fazure%2Fai-services%2Fagents%2Fcontext%2Fcontext){:target="_blank"}. Binubuo ito ng maraming lab, bawat isa ay nagha-highlight ng isang partikular na feature ng Azure AI Agents Service. Nilalayong kumpletuhin ang mga lab nang sunod-sunod dahil bawat isa ay nakabatay sa kaalaman at gawain mula sa naunang lab.

## Piliin ang Wika ng Workshop

Available ang workshop sa parehong Python at C#. Tiyaking piliin ang wikang tumutugma sa lab room na kinaroroonan mo gamit ang language selector tabs. Tandaan, huwag magpalit ng wika sa kalagitnaan ng workshop.

**Piliin ang language tab na tumutugma sa iyong lab room:**

=== "Python"
    Ang default na wika para sa workshop ay naka-set sa **Python**.
=== "C#"
    Ang default na wika para sa workshop ay naka-set sa **C#**.

## Mag-authenticate sa Azure

Kailangan mong mag-authenticate sa Azure upang makapag-access ang agent app sa Azure AI Agents Service at mga model. Sundin ang mga hakbang na ito:

1. Magbukas ng terminal window. Ang terminal app ay **naka-pin** sa Windows 11 taskbar.

    ![Open the terminal window](../media/windows-taskbar.png){ width="300" }

2. Patakbuhin ang sumusunod na command upang mag-authenticate sa Azure:

    ```powershell
    az login
    ```

    !!! note
        Ma-pi-prompt kang buksan ang isang browser link at mag-log in sa iyong Azure account.

        1. Awtomatikong magbubukas ang browser window, piliin ang **Work or school account** at i-click ang **Next**.

        1. Gamitin ang **Username** at **Password** na makikita sa **itaas na seksyon** ng **Resources** tab sa lab environment.

        2. Piliin ang **OK**, pagkatapos **Done**.

3. Pagkatapos piliin ang **Default** subscription mula sa command line, pamamagitan ng pag-click sa **Enter**.

4. Kapag naka-log in ka na, patakbuhin ang sumusunod na command upang i-assign ang **user** role sa resource group:

    ```powershell
    $subId = $(az account show --query id --output tsv) `
    ;$objectId = $(az ad signed-in-user show --query id -o tsv) `
    ; az role assignment create --role "f6c7c914-8db3-469d-8ca1-694a8f32e121" --assignee-object-id $objectId --scope /subscriptions/$subId/resourceGroups/"rg-agent-workshop" --assignee-principal-type 'User'
    ```

5. Iwanang bukas ang terminal window para sa susunod na mga hakbang.

## Buksan ang Workshop

Sundin ang mga hakbang na ito upang buksan ang workshop sa Visual Studio Code:

=== "Python"

      1. Mula sa terminal window, isagawa ang sumusunod na mga command upang i-clone ang workshop repository, mag-navigate sa kaukulang folder, mag-set up ng virtual environment, i-activate ito, at i-install ang mga kinakailangang packages:

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

        !!! warning "Kapag bumukas ang proyekto sa VS Code, lilitaw ang dalawang notification sa ibabang kanang sulok. I-click ang ✖ upang isara ang parehong notification."

=== "C#"

    1. Mula sa terminal window, isagawa ang sumusunod na mga command upang i-clone ang workshop repository:

        ```powershell
        git clone https://github.com/microsoft/build-your-first-agent-with-azure-ai-agent-service-workshop.git
        ```

    === "VS Code"

        1. Buksan ang workshop sa Visual Studio Code. Mula sa terminal window, patakbuhin ang sumusunod na command:

            ```powershell
            code build-your-first-agent-with-azure-ai-agent-service-workshop\.vscode\csharp-workspace.code-workspace
            ```

        !!! note "Kapag bumukas ang proyekto sa VS Code, may lalabas na notification sa ibabang kanang sulok para i-install ang C# extension. I-click ang **Install** upang i-install ang C# extension para sa kinakailangang features."

    === "Visual Studio 2022"

        1. Buksan ang workshop sa Visual Studio 2022. Mula sa terminal window, patakbuhin ang sumusunod na command:

            ```powershell
            start build-your-first-agent-with-azure-ai-agent-service-workshop\src\csharp\workshop\AgentWorkshop.sln
            ```

            !!! note "Maaaring tanungin ka kung aling programa ang gagamitin upang buksan ang solution. Piliin ang **Visual Studio 2022**."

## Azure AI Foundry Project Endpoint

Susunod, mag-log in tayo sa Azure AI Foundry upang makuha ang project endpoint, na ginagamit ng agent app upang kumonekta sa Azure AI Agents Service.

1. Mag-navigate sa [Azure AI Foundry](https://ai.azure.com){:target="_blank"} website.
2. Piliin ang **Sign in** at gamitin ang **Username** at **Password** na nasa **itaas na seksyon** ng **Resources** tab sa lab environment. I-click ang **Username** at **Password** fields upang awtomatikong punan ang login details.
    ![Azure credentials](../media/azure-credentials.png){:width="500"}
3. Basahin ang panimula sa Azure AI Foundry at i-click ang **Got it**.
4. Mag-navigate sa [All Resources](https://ai.azure.com/AllResources){:target="_blank"} upang makita ang listahan ng mga AI resource na pre-provisioned para sa iyo.
5. Piliin ang resource name na nagsisimula sa **aip-** na may type na **Project**.

    ![Select project](../media/ai-foundry-project.png){:width="500"}

6. Repasuhin ang introduction guide at i-click ang **Close**.
7. Mula sa **Overview** sidebar menu, hanapin ang **Endpoints and keys** -> **Libraries** -> **Azure AI Foundry** section, i-click ang **Copy** icon upang kopyahin ang **Azure AI Foundry project endpoint**.

    ![Copy connection string](../media/project-connection-string.png){:width="500"}

=== "Python"

    ## I-configure ang Workshop

    1. Lumipat pabalik sa workshop na binuksan mo sa VS Code.
    2. **I-rename** ang `.env.sample` file sa `.env`.

        - Piliin ang **.env.sample** file sa VS Code **Explorer** panel.
        - I-right-click ang file at piliin ang **Rename**, o pindutin ang <kbd>F2</kbd>.
        - Palitan ang file name sa `.env` at pindutin ang <kbd>Enter</kbd>.

    3. I-paste ang **Project endpoint** na kinopya mo mula sa Azure AI Foundry sa `.env` file.

        ```python
        PROJECT_ENDPOINT="<your_project_endpoint>"
        ```

        Ang iyong `.env` file ay dapat kahawig nito ngunit may sarili mong project endpoint.

        ```python
        PROJECT_ENDPOINT="<your_project_endpoint>"
        MODEL_DEPLOYMENT_NAME="<your_model_deployment_name>"
        DEV_TUNNEL_URL="<your_dev_tunnel_url>"
        ```

    4. I-save ang `.env` file.

    ## Istruktura ng Proyekto

    Tiyaking pamilyar ka sa mga pangunahing **subfolder** at **file** na gagamitin sa buong workshop.

    5. Ang **app.py** file: Ang entry point para sa app, naglalaman ng pangunahing lohika nito.
    6. Ang **sales_data.py** file: Ang function logic upang magpatupad ng dynamic SQL queries laban sa SQLite database.
    7. Ang **stream_event_handler.py** file: Naglalaman ng event handler logic para sa token streaming.
    8. Ang **shared/files** folder: Naglalaman ng mga file na ginawa ng agent app.
    9. Ang **shared/instructions** folder: Naglalaman ng instructions na ipinapasa sa LLM.

    ![Lab folder structure](../media/project-structure-self-guided-python.png)

=== "C#"

    ## I-configure ang Workshop

    1. Magbukas ng terminal at mag-navigate sa **src/csharp/workshop/AgentWorkshop.Client** folder.

        ```powershell
        cd build-your-first-agent-with-azure-ai-agent-service-workshop\src\csharp\workshop\AgentWorkshop.Client
        ```

    2. Idagdag ang **Project endpoint** na kinopya mo mula sa Azure AI Foundry sa user secrets.

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
        $aiAccount = "<ai_account_name>" # Palitan ng aktuwal na AI account name
        $aiProject = "<ai_project_name>" # Palitan ng aktuwal na AI project name
        $bingConnectionId = "/subscriptions/$subId/resourceGroups/$rgName/providers/Microsoft.CognitiveServices/accounts/$aiAccount/projects/$aiProject/connections/groundingwithbingsearch"
        dotnet user-secrets set "Azure:BingConnectionId" "$bingConnectionId"
        ```

    ## Istruktura ng Proyekto

    Tiyaking pamilyar ka sa mga pangunahing **subfolder** at **file** na gagamitin mo sa buong workshop.

    ### Ang workshop folder

    - Ang **Lab1.cs, Lab2.cs, Lab3.cs** files: Ang entry point para sa bawat lab, naglalaman ng agent logic nito.
    - Ang **Program.cs** file: Ang entry point para sa app, naglalaman ng pangunahing lohika nito.
    - Ang **SalesData.cs** file: Ang function logic upang magpatupad ng dynamic SQL queries laban sa SQLite database.

    ### Ang shared folder

    - Ang **files** folder: Naglalaman ng mga file na ginawa ng agent app.
    - Ang **fonts** folder: Naglalaman ng multilingual fonts na ginagamit ng Code Interpreter.
    - Ang **instructions** folder: Naglalaman ng instructions na ipinapasa sa LLM.

    ![Lab folder structure](../media/project-structure-self-guided-csharp.png)

## Mga Pro Tips

!!! tips
    1. Ang **Burger Menu** sa kanang panel ng lab environment ay nag-aalok ng karagdagang features, kabilang ang **Split Window View** at ang opsyon na tapusin ang lab. Pinapayagan ka ng **Split Window View** na i-maximize ang lab environment sa full screen, na nag-o-optimize ng screen space. Bubukas sa hiwalay na window ang **Instructions** at **Resources** panel ng lab.
    2. Kung mabagal mag-scroll ang lab instructions sa lab environment, subukang kopyahin ang URL ng instructions at buksan ito sa **lokal na browser ng iyong computer** para sa mas maayos na karanasan.
    3. Kung nahihirapan kang makita ang isang larawan, **i-click lang ang larawan para palakihin ito**.

*Isinalin gamit ang GitHub Copilot.*
