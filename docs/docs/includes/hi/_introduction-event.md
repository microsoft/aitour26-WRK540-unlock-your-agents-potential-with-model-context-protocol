## Microsoft Event उपस्थितकर्ता

इस पृष्ठ पर दिए गए निर्देश मानते हैं कि आप [Microsoft Event 2025](https://build.microsoft.com/){:target="_blank"} में भाग ले रहे हैं और आपके पास पूर्व-कॉन्फ़िगर किए गए लैब वातावरण तक पहुंच है। यह वातावरण कार्यशाला पूरा करने के लिए आवश्यक सभी टूल्स और संसाधनों के साथ एक Azure subscription प्रदान करता है।

## परिचय

यह कार्यशाला आपको Azure AI Agents Service और संबंधित [SDK](https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme?context=%2Fazure%2Fai-services%2Fagents%2Fcontext%2Fcontext){:target="_blank"} के बारे में सिखाने के लिए डिज़ाइन की गई है। इसमें कई लैब्स हैं, जो Azure AI Agents Service की एक विशिष्ट सुविधा को उजागर करती है। लैब्स को क्रम में पूरा करने के लिए बनाया गया है, क्योंकि प्रत्येक पिछली लैब के ज्ञान और कार्य पर आधारित है।

## कार्यशाला प्रोग्रामिंग भाषा का चयन

कार्यशाला Python और C# दोनों में उपलब्ध है। कृपया भाषा चयनकर्ता टैब का उपयोग करके उस भाषा का चयन करना सुनिश्चित करें जो आपके लैब रूम के अनुकूल है। नोट करें, कार्यशाला के बीच भाषा न बदलें।

**अपने लैब रूम से मेल खाने वाली भाषा टैब का चयन करें:**

=== "Python"
    कार्यशाला के लिए डिफ़ॉल्ट भाषा **Python** सेट है।
=== "C#"
    कार्यशाला के लिए डिफ़ॉल्ट भाषा **C#** सेट है।

## Azure के साथ प्रमाणीकरण

आपको Azure के साथ प्रमाणीकरण करना होगा ताकि एजेंट ऐप Azure AI Agents Service और models तक पहुंच सके। इन चरणों का पालन करें:

1. एक टर्मिनल विंडो खोलें। टर्मिनल ऐप Windows 11 taskbar में **pinned** है।

    ![Open the terminal window](../media/windows-taskbar.png){ width="300" }

2. Azure के साथ प्रमाणीकरण के लिए निम्नलिखित कमांड चलाएं:

    ```powershell
    az login
    ```

    !!! note
        आपको एक ब्राउज़र लिंक खोलने और अपने Azure खाते में लॉग इन करने के लिए कहा जाएगा।

        1. एक ब्राउज़र विंडो स्वचालित रूप से खुलेगी, **Work or school account** का चयन करें और **Next** पर क्लिक करें।

        1. लैब वातावरण के **Resources** टैब के **top section** में पाए गए **Username** और **Password** का उपयोग करें।

        2. **OK**, फिर **Done** का चयन करें।

3. फिर **Enter** पर क्लिक करके कमांड लाइन से **Default** subscription का चयन करें।

4. एक बार लॉग इन करने के बाद, resource group को **user** भूमिका असाइन करने के लिए निम्नलिखित कमांड चलाएं:

    ```powershell
    $subId = $(az account show --query id --output tsv) `
    ;$objectId = $(az ad signed-in-user show --query id -o tsv) `
    ; az role assignment create --role "f6c7c914-8db3-469d-8ca1-694a8f32e121" --assignee-object-id $objectId --scope /subscriptions/$subId/resourceGroups/"rg-agent-workshop" --assignee-principal-type 'User'
    ```

5. अगले चरणों के लिए टर्मिनल विंडो खुली छोड़ें।

## कार्यशाला खोलना

Visual Studio Code में कार्यशाला खोलने के लिए इन चरणों का पालन करें:

=== "Python"

      1. टर्मिनल विंडो से, कार्यशाला रिपॉजिटरी को clone करने, संबंधित फोल्डर में नेविगेट करने, virtual environment सेट करने, इसे activate करने, और आवश्यक packages इंस्टॉल करने के लिए निम्नलिखित कमांड निष्पादित करें:

          ```powershell
          git clone https://github.com/microsoft/build-your-first-agent-with-azure-ai-agent-service-workshop.git `
          ; cd build-your-first-agent-with-azure-ai-agent-service-workshop `
          ; python -m venv src/python/workshop/.venv `
          ; src\python\workshop\.venv\Scripts\activate `
          ; pip install -r src/python/workshop/requirements.txt `
          ; code --install-extension tomoki1207.pdf
          ```

      2. VS Code में खोलें। टर्मिनल विंडो से, निम्नलिखित कमांड चलाएं:

          ```powershell
          code .vscode\python-workspace.code-workspace
          ```

        !!! warning "जब प्रोजेक्ट VS Code में खुलता है, तो नीचे दाएं कोने में दो notifications दिखाई देती हैं। दोनों notifications को बंद करने के लिए ✖ पर क्लिक करें।"

=== "C#"

    1. टर्मिनल विंडो से, कार्यशाला रिपॉजिटरी को clone करने के लिए निम्नलिखित कमांड निष्पादित करें:

        ```powershell
        git clone https://github.com/microsoft/build-your-first-agent-with-azure-ai-agent-service-workshop.git
        ```

    === "VS Code"

        1. Visual Studio Code में कार्यशाला खोलें। टर्मिनल विंडो से, निम्नलिखित कमांड चलाएं:

            ```powershell
            code build-your-first-agent-with-azure-ai-agent-service-workshop\.vscode\csharp-workspace.code-workspace
            ```

        !!! note "जब प्रोजेक्ट VS Code में खुलता है, तो नीचे दाएं कोने में C# extension इंस्टॉल करने के लिए एक notification दिखाई देगी। C# extension इंस्टॉल करने के लिए **Install** पर क्लिक करें, क्योंकि यह C# development के लिए आवश्यक सुविधाएं प्रदान करेगा।"

    === "Visual Studio 2022"

        1. Visual Studio 2022 में कार्यशाला खोलें। टर्मिनल विंडो से, निम्नलिखित कमांड चलाएं:

            ```powershell
            start build-your-first-agent-with-azure-ai-agent-service-workshop\src\csharp\workshop\AgentWorkshop.sln
            ```

            !!! note "आपसे पूछा जा सकता है कि solution को किस प्रोग्राम से खोलना है। **Visual Studio 2022** का चयन करें।"

## Azure AI Foundry Project Endpoint

इसके बाद, हम project endpoint प्राप्त करने के लिए Azure AI Foundry में लॉग इन करते हैं, जिसका उपयोग एजेंट ऐप Azure AI Agents Service से कनेक्ट करने के लिए करता है।

1. [Azure AI Foundry](https://ai.azure.com){:target="_blank"} वेबसाइट पर नेविगेट करें।
2. **Sign in** का चयन करें और लैब वातावरण के **Resources** टैब के **top section** में पाए गए **Username** और **Password** का उपयोग करें। लॉगिन विवरण को स्वचालित रूप से भरने के लिए **Username** और **Password** fields पर क्लिक करें।
    ![Azure credentials](../media/azure-credentials.png){:width="500"}
3. Azure AI Foundry का परिचय पढ़ें और **Got it** पर क्लिक करें।
4. आपके लिए पूर्व-provisioned AI resources की सूची देखने के लिए [All Resources](https://ai.azure.com/AllResources){:target="_blank"} पर नेविगेट करें।
5. **aip-** से शुरू होने वाले **Project** प्रकार के resource name का चयन करें।

    ![Select project](../media/ai-foundry-project.png){:width="500"}

6. परिचय गाइड की समीक्षा करें और **Close** पर क्लिक करें।
7. **Overview** sidebar menu से, **Endpoints and keys** -> **Libraries** -> **Azure AI Foundry** section का पता लगाएं, **Azure AI Foundry project endpoint** को कॉपी करने के लिए **Copy** icon पर क्लिक करें।

    ![Copy connection string](../media/project-connection-string.png){:width="500"}

=== "Python"

    ## कार्यशाला कॉन्फ़िगर करें

    1. VS Code में खोली गई कार्यशाला पर वापस स्विच करें।
    2. `.env.sample` फाइल को `.env` में **rename** करें।

        - VS Code **Explorer** panel में **.env.sample** फाइल का चयन करें।
        - फाइल पर राइट-क्लिक करें और **Rename** का चयन करें, या <kbd>F2</kbd> दबाएं।
        - फाइल का नाम `.env` में बदलें और <kbd>Enter</kbd> दबाएं।

    3. Azure AI Foundry से कॉपी किए गए **Project endpoint** को `.env` फाइल में पेस्ट करें।

        ```python
        PROJECT_ENDPOINT="<your_project_endpoint>"
        ```

        आपकी `.env` फाइल इस तरह दिखनी चाहिए लेकिन आपके project endpoint के साथ।

        ```python
        PROJECT_ENDPOINT="<your_project_endpoint>"
        MODEL_DEPLOYMENT_NAME="<your_model_deployment_name>"
        DEV_TUNNEL_URL="<your_dev_tunnel_url>"
        ```

    4. `.env` फाइल सेव करें।

    ## प्रोजेक्ट संरचना

    उन मुख्य **subfolders** और **files** से परिचित होना सुनिश्चित करें जिनके साथ आप पूरी कार्यशाला में काम करेंगे।

    5. **app.py** फाइल: ऐप का entry point, जिसमें इसकी मुख्य logic है।
    6. **sales_data.py** फाइल: SQLite डेटाबेस के विरुद्ध dynamic SQL queries निष्पादित करने के लिए function logic।
    7. **stream_event_handler.py** फाइल: token streaming के लिए event handler logic शामिल है।
    8. **shared/files** फोल्डर: एजेंट ऐप द्वारा बनाई गई फाइलें शामिल हैं।
    9. **shared/instructions** फोल्डर: LLM को पास किए गए निर्देश शामिल हैं।

    ![Lab folder structure](../media/project-structure-self-guided-python.png)

=== "C#"

    ## कार्यशाला कॉन्फ़िगर करें

    1. एक टर्मिनल खोलें और **src/csharp/workshop/AgentWorkshop.Client** फोल्डर में नेविगेट करें।

        ```powershell
        cd build-your-first-agent-with-azure-ai-agent-service-workshop\src\csharp\workshop\AgentWorkshop.Client
        ```

    2. Azure AI Foundry से कॉपी किए गए **Project endpoint** को user secrets में जोड़ें।

        ```powershell
        dotnet user-secrets set "ConnectionStrings:AiAgentService" "<your_project_endpoint>"
        ```

    3. User secrets में **Model deployment name** जोड़ें।

        ```powershell
        dotnet user-secrets set "Azure:ModelName" "gpt-4o"
        ```

    4. Bing search के साथ grounding के लिए user secrets में **Bing connection ID** जोड़ें।

        ```powershell
        $subId = $(az account show --query id --output tsv)
        $rgName = "rg-agent-workshop"
        $aiAccount = "<ai_account_name>" # वास्तविक AI account name से बदलें
        $aiProject = "<ai_project_name>" # वास्तविक AI project name से बदलें
        $bingConnectionId = "/subscriptions/$subId/resourceGroups/$rgName/providers/Microsoft.CognitiveServices/accounts/$aiAccount/projects/$aiProject/connections/groundingwithbingsearch"
        dotnet user-secrets set "Azure:BingConnectionId" "$bingConnectionId"
        ```

    ## प्रोजेक्ट संरचना

    उन मुख्य **subfolders** और **files** से परिचित होना सुनिश्चित करें जिनके साथ आप पूरी कार्यशाला में काम करेंगे।

    ### कार्यशाला फोल्डर

    - **Lab1.cs, Lab2.cs, Lab3.cs** फाइलें: प्रत्येक लैब का entry point, जिसमें इसकी agent logic है।
    - **Program.cs** फाइल: ऐप का entry point, जिसमें इसकी मुख्य logic है।
    - **SalesData.cs** फाइल: SQLite डेटाबेस के विरुद्ध dynamic SQL queries निष्पादित करने के लिए function logic।

    ### shared फोल्डर

    - **files** फोल्डर: एजेंट ऐप द्वारा बनाई गई फाइलें शामिल हैं।
    - **fonts** फोल्डर: Code Interpreter द्वारा उपयोग किए जाने वाले multilingual fonts शामिल हैं।
    - **instructions** फोल्डर: LLM को पास किए गए निर्देश शामिल हैं।

    ![Lab folder structure](../media/project-structure-self-guided-csharp.png)

## Pro Tips

!!! tips
    1. लैब वातावरण के right-hand panel में **Burger Menu** अतिरिक्त सुविधाएं प्रदान करता है, जिसमें **Split Window View** और लैब समाप्त करने का विकल्प शामिल है। **Split Window View** आपको लैब वातावरण को full screen पर maximize करने की अनुमति देता है, screen space को अनुकूलित करता है। लैब के **Instructions** और **Resources** panel एक अलग विंडो में खुलेंगे।
    2. यदि लैब वातावरण में लैब निर्देशों को scroll करना धीमा है, तो smoother experience के लिए निर्देशों का URL कॉपी करके इसे **अपने कंप्यूटर के local browser** में खोलने की कोशिश करें।
    3. यदि आपको image देखने में परेशानी हो रही है, तो इसे बड़ा करने के लिए बस **image पर क्लिक करें**।

*GitHub Copilot और GPT-4o का उपयोग करके अनुवादित।*
