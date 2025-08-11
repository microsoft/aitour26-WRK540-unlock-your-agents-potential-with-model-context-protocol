## Microsoft Event प्रतिभागी

इस पेज पर दिए गए निर्देशों का अनुमान है कि आप [Microsoft Event 2025](https://build.microsoft.com/){:target="_blank"} में भाग ले रहे हैं और आपके पास pre-configured lab environment तक पहुंच है। यह environment एक Azure subscription प्रदान करता है जिसमें workshop पूरा करने के लिए आवश्यक सभी tools और resources हैं।

## परिचय

यह workshop आपको Azure AI Agents Service और संबंधित [SDK](https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme?context=%2Fazure%2Fai-services%2Fagents%2Fcontext%2Fcontext){:target="_blank"} के बारे में सिखाने के लिए डिज़ाइन किया गया है। इसमें मल्टिपल labs हैं, प्रत्येक Azure AI Agents Service की specific feature को highlight करती है। Labs को order में पूरा करना है, क्योंकि प्रत्येक previous lab के knowledge और work पर build करती है।

## Workshop Programming Language सेलेक्ट करना

Workshop Python और C# दोनों में उपलब्ध है। कृपया सुनिश्चित करें कि आप language selector tabs का उपयोग करके उस language को सेलेक्ट करें जो आपके lab room में fit करती है। नोट करें, workshop के बीच में languages switch न करें।

**अपने lab room से match करने वाला language tab सेलेक्ट करें:**

=== "Python"
    Workshop के लिए default language **Python** पर set है।
=== "C#"
    Workshop के लिए default language **C#** पर set है।

## Azure के साथ Authenticate करना

आपको Azure के साथ authenticate करना होगा ताकि agent app Azure AI Agents Service और models तक पहुंच सके। इन steps को follow करें:

1. Terminal window खोलें। Terminal app Windows 11 taskbar पर **pinned** है।

    ![Open the terminal window](../media/windows-taskbar.png){ width="300" }

2. Azure के साथ authenticate करने के लिए निम्नलिखित command चलाएं:

    ```powershell
    az login
    ```

    !!! note
        आपको browser link खोलने और अपने Azure account में log in करने के लिए कहा जाएगा।

        1. Browser window automatically खुलेगा, **Work or school account** सेलेक्ट करें और **Next** पर click करें।

        1. Lab environment के **Resources** tab के **top section** में मिले **Username** और **Password** का उपयोग करें।

        2. **OK**, फिर **Done** सेलेक्ट करें।

3. फिर command line से **Enter** पर click करके **Default** subscription सेलेक्ट करें।

4. एक बार log in हो जाने के बाद, resource group को **user** role assign करने के लिए निम्नलिखित command चलाएं:

    ```powershell
    $subId = $(az account show --query id --output tsv) `
    ;$objectId = $(az ad signed-in-user show --query id -o tsv) `
    ; az role assignment create --role "f6c7c914-8db3-469d-8ca1-694a8f32e121" --assignee-object-id $objectId --scope /subscriptions/$subId/resourceGroups/"rg-agent-workshop" --assignee-principal-type 'User'
    ```

5. अगले steps के लिए terminal window को खुला छोड़ दें।

## Workshop खोलना

Visual Studio Code में workshop खोलने के लिए इन steps को follow करें:

=== "Python"

      1. Terminal window से, workshop repository को clone करने, relevant folder पर navigate करने, virtual environment set up करने, उसे activate करने, और required packages install करने के लिए निम्नलिखित commands execute करें:

          ```powershell
          git clone https://github.com/microsoft/build-your-first-agent-with-azure-ai-agent-service-workshop.git `
          ; cd build-your-first-agent-with-azure-ai-agent-service-workshop `
          ; python -m venv src/python/workshop/.venv `
          ; src\python\workshop\.venv\Scripts\activate `
          ; pip install -r src/python/workshop/requirements.txt `
          ; code --install-extension tomoki1207.pdf
          ```

      2. VS Code में खोलें। Terminal window से, निम्नलिखित command चलाएं:

          ```powershell
          code .vscode\python-workspace.code-workspace
          ```

        !!! warning "जब project VS Code में खुलता है, तो bottom right corner में दो notifications appear होती हैं। दोनों notifications को बंद करने के लिए ✖ पर click करें।"

=== "C#"

    1. Terminal window से, workshop repository को clone करने के लिए निम्नलिखित commands execute करें:

        ```powershell
        git clone https://github.com/microsoft/build-your-first-agent-with-azure-ai-agent-service-workshop.git
        ```

    === "VS Code"

        1. Visual Studio Code में workshop खोलें। Terminal window से, निम्नलिखित command चलाएं:

            ```powershell
            code build-your-first-agent-with-azure-ai-agent-service-workshop\.vscode\csharp-workspace.code-workspace
            ```

        !!! note "जब project VS Code में खुलता है, तो C# extension install करने के लिए bottom right corner में notification appear होगी। C# extension install करने के लिए **Install** पर click करें, क्योंकि यह C# development के लिए आवश्यक features प्रदान करेगा।"

    === "Visual Studio 2022"

        1. Visual Studio 2022 में workshop खोलें। Terminal window से, निम्नलिखित command चलाएं:

            ```powershell
            start build-your-first-agent-with-azure-ai-agent-service-workshop\src\csharp\workshop\AgentWorkshop.sln
            ```

            !!! note "आपसे पूछा जा सकता है कि solution को किस program से खोलना है। **Visual Studio 2022** सेलेक्ट करें।"

## Azure AI Foundry Project Endpoint

इसके बाद, हम project endpoint retrieve करने के लिए Azure AI Foundry में log in करते हैं, जिसका उपयोग agent app Azure AI Agents Service से connect करने के लिए करता है।

1. [Azure AI Foundry](https://ai.azure.com){:target="_blank"} website पर navigate करें।
2. **Sign in** सेलेक्ट करें और lab environment के **Resources** tab के **top section** में मिले **Username** और **Password** का उपयोग करें। Login details को automatically fill करने के लिए **Username** और **Password** fields पर click करें।
    ![Azure credentials](../media/azure-credentials.png){:width="500"}
3. Azure AI Foundry का introduction पढ़ें और **Got it** पर click करें।
4. आपके लिए pre-provisioned AI resources की list देखने के लिए [All Resources](https://ai.azure.com/AllResources){:target="_blank"} पर navigate करें।
5. **Project** type के **aip-** से शुरू होने वाले resource name को सेलेक्ट करें।

    ![Select project](../media/ai-foundry-project.png){:width="500"}

6. Introduction guide को review करें और **Close** पर click करें।
7. **Overview** sidebar menu से, **Endpoints and keys** -> **Libraries** -> **Azure AI Foundry** section locate करें, **Azure AI Foundry project endpoint** copy करने के लिए **Copy** icon पर click करें।

    ![Copy connection string](../media/project-connection-string.png){:width="500"}

=== "Python"

    ## Workshop को Configure करना

    1. VS Code में खोली गई workshop पर वापस switch करें।
    2. `.env.sample` file को `.env` में **Rename** करें।

        - VS Code **Explorer** panel में **.env.sample** file सेलेक्ट करें।
        - File पर right-click करें और **Rename** सेलेक्ट करें, या <kbd>F2</kbd> दबाएं।
        - File name को `.env` में बदलें और <kbd>Enter</kbd> दबाएं।

    3. Azure AI Foundry से copy किया गया **Project endpoint** को `.env` file में paste करें।

        ```python
        PROJECT_ENDPOINT="<your_project_endpoint>"
        ```

        आपकी `.env` file इस प्रकार दिखनी चाहिए लेकिन आपके project endpoint के साथ।

        ```python
        PROJECT_ENDPOINT="<your_project_endpoint>"
        MODEL_DEPLOYMENT_NAME="<your_model_deployment_name>"
        DEV_TUNNEL_URL="<your_dev_tunnel_url>"
        ```

    4. `.env` file को save करें।

    ## Project Structure

    Workshop के दौरान आप जिन मुख्य **subfolders** और **files** के साथ काम करेंगे, उनसे परिचित होना सुनिश्चित करें।

    5. **app.py** file: App का entry point, जिसमें इसकी main logic है।
    6. **sales_data.py** file: SQLite database के against dynamic SQL queries execute करने के लिए function logic।
    7. **stream_event_handler.py** file: Token streaming के लिए event handler logic शामिल है।
    8. **shared/files** folder: Agent app द्वारा बनाई गई files शामिल हैं।
    9. **shared/instructions** folder: LLM को pass किए जाने वाले instructions शामिल हैं।

    ![Lab folder structure](../media/project-structure-self-guided-python.png)

=== "C#"

    ## Workshop को Configure करना

    1. Terminal खोलें और **src/csharp/workshop/AgentWorkshop.Client** folder पर navigate करें।

        ```powershell
        cd build-your-first-agent-with-azure-ai-agent-service-workshop\src\csharp\workshop\AgentWorkshop.Client
        ```

    2. Azure AI Foundry से copy किया गया **Project endpoint** को user secrets में add करें।

        ```powershell
        dotnet user-secrets set "ConnectionStrings:AiAgentService" "<your_project_endpoint>"
        ```

    3. **Model deployment name** को user secrets में add करें।

        ```powershell
        dotnet user-secrets set "Azure:ModelName" "gpt-4o"
        ```

    4. Bing search के साथ grounding के लिए **Bing connection ID** को user secrets में add करें।

        ```powershell
        $subId = $(az account show --query id --output tsv)
        $rgName = "rg-agent-workshop"
        $aiAccount = "<ai_account_name>" # Actual AI account name से replace करें
        $aiProject = "<ai_project_name>" # Actual AI project name से replace करें
        $bingConnectionId = "/subscriptions/$subId/resourceGroups/$rgName/providers/Microsoft.CognitiveServices/accounts/$aiAccount/projects/$aiProject/connections/groundingwithbingsearch"
        dotnet user-secrets set "Azure:BingConnectionId" "$bingConnectionId"
        ```

    ## Project Structure

    Workshop के दौरान आप जिन मुख्य **subfolders** और **files** के साथ काम करेंगे, उनसे परिचित होना सुनिश्चित करें।

    ### workshop folder

    - **Lab1.cs, Lab2.cs, Lab3.cs** files: प्रत्येक lab का entry point, जिसमें इसकी agent logic है।
    - **Program.cs** file: App का entry point, जिसमें इसकी main logic है।
    - **SalesData.cs** file: SQLite database के against dynamic SQL queries execute करने के लिए function logic।

    ### shared folder

    - **files** folder: Agent app द्वारा बनाई गई files शामिल हैं।
    - **fonts** folder: Code Interpreter द्वारा उपयोग किए जाने वाले multilingual fonts शामिल हैं।
    - **instructions** folder: LLM को pass किए जाने वाले instructions शामिल हैं।

    ![Lab folder structure](../media/project-structure-self-guided-csharp.png)

## Pro Tips

!!! tips
    1. Lab environment के right-hand panel में **Burger Menu** additional features offer करता है, जिसमें **Split Window View** और lab end करने का option शामिल है। **Split Window View** आपको lab environment को full screen पर maximize करने की अनुमति देता है, screen space को optimize करता है। Lab के **Instructions** और **Resources** panel अलग window में खुलेंगे।
    2. यदि lab environment में lab instructions scroll करने में slow हैं, तो smoother experience के लिए instructions के URL को copy करके **अपने computer के local browser** में खोलने की कोशिश करें।
    3. यदि आपको image देखने में trouble हो रही है, तो बस **image को enlarge करने के लिए click करें**।

*GitHub Copilot का उपयोग करके अनुवादित।*
