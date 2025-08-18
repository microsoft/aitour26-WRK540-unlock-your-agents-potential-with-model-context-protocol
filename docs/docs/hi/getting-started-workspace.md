दो VS Code वर्कस्पेस इस वर्कशॉप में हैं, एक Python के लिए और एक C# के लिए। वर्कस्पेस में स्रोत कोड और प्रत्येक भाषा की लैब्स पूरी करने के लिए सभी फ़ाइलें शामिल हैं। उस भाषा से मेल खाने वाला वर्कस्पेस चुनें जिसके साथ आप काम करना चाहते हैं।

=== "Python"

    1. **निम्न पथ कॉपी** करें:

        ```text
        /workspace/.vscode/python-workspace.code-workspace
        ```
    1. VS Code मेनू से **File** फिर **Open Workspace from File** चुनें।
    3. पेस्ट करें और **OK** चुनें।


    ## प्रोजेक्ट संरचना

    उस वर्कस्पेस की मुख्य **फोल्डर** और **फ़ाइल** से परिचित हों जिसके साथ आप पूरे वर्कशॉप में काम करेंगे।

    ### "workshop" फ़ोल्डर

    - **app.py** फ़ाइल: ऐप का एंट्री पॉइंट, मुख्य लॉजिक।
  
    **INSTRUCTIONS_FILE** वेरिएबल देखें—यह सेट करता है कौन‑सी निर्देश फ़ाइल एजेंट उपयोग करेगा। आप इसे बाद की लैब में अपडेट करेंगे।

    - **resources.txt**: एजेंट ऐप द्वारा उपयोग किए गए संसाधन।
    - **.env**: एजेंट ऐप के लिए पर्यावरण चर।

    ### "mcp_server" फ़ोल्डर

    - **sales_analysis.py**: बिक्री विश्लेषण के लिए MCP सर्वर और टूल।

    ### "shared/instructions" फ़ोल्डर

    - **instructions** फ़ोल्डर: LLM को पास किए गए निर्देश।

    ![लैब फ़ोल्डर संरचना](media/project-structure-self-guided-python.png)

=== "C#"

    1. Visual Studio Code में **File** > **Open Workspace from File**।
    2. डिफ़ॉल्ट पथ को निम्न से बदलें:

        ```text
        /workspace/.vscode/csharp-workspace.code-workspace
        ```

    3. **OK** चुनें।

    ## प्रोजेक्ट संरचना

    मुख्य **फोल्डर** और **फ़ाइल** से परिचित हों जिनके साथ आप काम करेंगे।

    ### workshop फ़ोल्डर

    - **Lab1.cs, Lab2.cs, Lab3.cs**: प्रत्येक लैब का एंट्री पॉइंट।
    - **Program.cs**: ऐप का एंट्री पॉइंट।
    - **SalesData.cs**: SQLite डेटाबेस पर डायनेमिक SQL क्वेरी निष्पादन लॉजिक।

    ### shared फ़ोल्डर

    - **files**: एजेंट ऐप द्वारा बनाई गई फ़ाइलें।
    - **fonts**: Code Interpreter द्वारा उपयोग किए गए बहुभाषी फ़ॉन्ट।
    - **instructions**: LLM को पास किए गए निर्देश।

    ![लैब फ़ोल्डर संरचना](media/project-structure-self-guided-csharp.png)

*GitHub Copilot द्वारा अनुवादित.*
