## भाषा वर्कस्पेस खोलना

वर्कशॉप में दो वर्कस्पेस हैं, एक Python के लिए और एक C# के लिए। वर्कस्पेस में सोर्स कोड और प्रत्येक भाषा के लिए लैब्स पूरा करने के लिए आवश्यक सभी फाइलें शामिल हैं। उस वर्कस्पेस को चुनें जो आपकी काम करने वाली भाषा से मेल खाता है।

=== "Python"

    1. निम्नलिखित कमांड को अपने क्लिपबोर्ड में कॉपी करें:

        ```text
        File: Open Workspace from File...
        ```
    2. Visual Studio Code पर स्विच करें, Command Palette खोलने के लिए <kbd>F1</kbd> दबाएं।
    3. कमांड को Command Palette में पेस्ट करें और **Open Workspace from File...** सेलेक्ट करें।
    4. निम्नलिखित पाथ को फाइल पिकर में कॉपी और पेस्ट करें और <kbd>Enter</kbd> दबाएं:

        ```text
        /workspace/.vscode/python-workspace.code-workspace
        ```

    ## प्रोजेक्ट स्ट्रक्चर

    वर्कशॉप के दौरान आप जिन मुख्य **फोल्डर्स** और **फाइलों** के साथ काम करेंगे, उनसे परिचित होना सुनिश्चित करें।

    ### workshop फोल्डर

    - **app.py** फाइल: ऐप का entry point, जिसमें इसकी मुख्य लॉजिक है।
  
    **INSTRUCTIONS_FILE** वेरिएबल नोट करें—यह सेट करता है कि एजेंट कौन सी instructions फाइल का उपयोग करता है। आप बाद की लैब में इस वेरिएबल को अपडेट करेंगे।

    - **resources.txt** फाइल: एजेंट ऐप द्वारा उपयोग किए जाने वाले रिसोर्सेस शामिल हैं।
    - **.env** फाइल: एजेंट ऐप द्वारा उपयोग किए जाने वाले environment variables शामिल हैं।

    ### mcp_server फोल्डर

    - **sales_analysis.py** फाइल: सेल्स एनालिसिस के लिए टूल्स के साथ MCP Server।

    ### shared फोल्डर

    - **instructions** फोल्डर: LLM को पास किए जाने वाले instructions शामिल हैं।

    ![Lab folder structure](media/project-structure-self-guided-python.png)

=== "C#"

    1. Visual Studio Code में, **File** > **Open Workspace from File** पर जाएं।
    2. डिफ़ॉल्ट पाथ को निम्नलिखित से बदलें:

        ```text
        /workspace/.vscode/csharp-workspace.code-workspace
        ```

    3. वर्कस्पेस खोलने के लिए **OK** सेलेक्ट करें।

    ## प्रोजेक्ट स्ट्रक्चर

    वर्कशॉप के दौरान आप जिन मुख्य **फोल्डर्स** और **फाइलों** के साथ काम करेंगे, उनसे परिचित होना सुनिश्चित करें।

    ### workshop फोल्डर

    - **Lab1.cs, Lab2.cs, Lab3.cs** फाइलें: प्रत्येक लैब का entry point, जिसमें इसकी एजेंट लॉजिक है।
    - **Program.cs** फाइल: ऐप का entry point, जिसमें इसकी मुख्य लॉजिक है।
    - **SalesData.cs** फाइल: SQLite डेटाबेस के विरुद्ध डायनामिक SQL क्वेरीज़ एक्जीक्यूट करने के लिए फंक्शन लॉजिक।

    ### shared फोल्डर

    - **files** फोल्डर: एजेंट ऐप द्वारा बनाई गई फाइलें शामिल हैं।
    - **fonts** फोल्डर: Code Interpreter द्वारा उपयोग किए जाने वाले बहुभाषी फॉन्ट्स शामिल हैं।
    - **instructions** फोल्डर: LLM को पास किए जाने वाले instructions शामिल हैं।

    ![Lab folder structure](media/project-structure-self-guided-csharp.png)

*GitHub Copilot का उपयोग करके अनुवादित।*
