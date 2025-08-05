## समाधान आर्किटेक्चर

इस कार्यशाला में, आप Zava Sales Agent बनाएंगे: एक वार्तालाप एजेंट जो बिक्री डेटा के बारे में सवालों के जवाब देने, Zava के रिटेल DIY व्यवसाय के लिए चार्ट जेनरेट करने के लिए डिज़ाइन किया गया है।

## एजेंट ऐप के घटक

1. **Microsoft Azure सेवाएं**

    यह एजेंट Microsoft Azure सेवाओं पर बनाया गया है।

      - **जेनरेटिव AI मॉडल**: इस ऐप को संचालित करने वाला अंतर्निहित LLM [Azure OpenAI gpt-4o-mini](https://learn.microsoft.com/azure/ai-foundry/openai/concepts/models?tabs=global-standard%2Cstandard-chat-completions#how-do-i-access-the-gpt-4o-and-gpt-4o-mini-models){:target="_blank"} LLM है।

      - **कंट्रोल प्लेन**: ऐप और इसके आर्किटेक्चरल घटकों को [Azure AI Foundry](https://ai.azure.com){:target="_blank"} पोर्टल का उपयोग करके प्रबंधित और मॉनिटर किया जाता है, जो ब्राउज़र के माध्यम से एक्सेसिबल है।

2. **Azure AI Foundry (SDK)**

    कार्यशाला Azure AI Foundry SDK का उपयोग करते हुए [Python](https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme?view=azure-python-preview&context=%2Fazure%2Fai-services%2Fagents%2Fcontext%2Fcontext){:target="_blank"} में पेश की गई है। SDK Azure AI Agents सेवा की मुख्य सुविधाओं का समर्थन करता है, जिसमें [Code Interpreter](https://learn.microsoft.com/azure/ai-services/agents/how-to/tools/code-interpreter?view=azure-python-preview&tabs=python&pivots=overview){:target="_blank"} और [Model Context Protocol (MCP)](https://modelcontextprotocol.io/){:target="_blank"} एकीकरण शामिल है।

3. **डेटाबेस**

    ऐप Zava Sales Database द्वारा संचालित है, एक [Azure Database for PostgreSQL flexible server](https://www.postgresql.org/){:target="_blank"} pgvector एक्सटेंशन के साथ जिसमें Zava के रिटेल DIY ऑपरेशन के लिए व्यापक बिक्री डेटा है। 

    डेटाबेस बिक्री, इन्वेंटरी, और ग्राहक डेटा के लिए जटिल क्वेरीज़ का समर्थन करता है। Row-Level Security (RLS) यह सुनिश्चित करता है कि एजेंट केवल अपने असाइन किए गए स्टोर तक पहुंच सकें।

4. **MCP सर्वर**

    Model Context Protocol (MCP) सर्वर एक कस्टम Python सेवा है जो एजेंट और PostgreSQL डेटाबेस के बीच एक ब्रिज का काम करती है। यह संभालती है:

     - **डेटाबेस स्कीमा डिस्कवरी**: एजेंट को उपलब्ध डेटा समझने में मदद करने के लिए स्वचालित रूप से डेटाबेस स्कीमा प्राप्त करती है।
     - **क्वेरी जेनरेशन**: प्राकृतिक भाषा अनुरोधों को SQL क्वेरीज़ में रूपांतरित करती है।
     - **टूल निष्पादन**: SQL क्वेरीज़ निष्पादित करती है और परिणामों को एक ऐसे प्रारूप में वापस करती है जिसका एजेंट उपयोग कर सके।
     - **समय सेवाएं**: समय-संवेदनशील रिपोर्ट जेनरेट करने के लिए समय-संबंधी डेटा प्रदान करती है।

## कार्यशाला समाधान का विस्तार

कार्यशाला को डेटाबेस अपडेट करके और Foundry Agent Service निर्देशों को कस्टमाइज़ करके ग्राहक सहायता जैसे उपयोग के मामलों के लिए आसानी से अनुकूलित किया जा सकता है।

## ऐप में प्रदर्शित सर्वोत्तम प्रथाएं

ऐप दक्षता और उपयोगकर्ता अनुभव के लिए कुछ सर्वोत्तम प्रथाओं को भी प्रदर्शित करता है।

- **एसिंक्रोनस APIs**:
  कार्यशाला नमूने में, Foundry Agent Service और PostgreSQL दोनों एसिंक्रोनस APIs का उपयोग करते हैं, संसाधन दक्षता और स्केलेबिलिटी को अनुकूलित करते हैं। यह डिज़ाइन विकल्प विशेष रूप से तब फायदेमंद हो जाता है जब एप्लिकेशन को FastAPI, ASP.NET, या Streamlit जैसे एसिंक्रोनस वेब फ्रेमवर्क के साथ तैनात किया जाता है।

- **टोकन स्ट्रीमिंग**:
  LLM-संचालित एजेंट ऐप के लिए अनुमानित प्रतिक्रिया समय को कम करके उपयोगकर्ता अनुभव में सुधार के लिए टोकन स्ट्रीमिंग को लागू किया गया है।

- **ऑब्जर्वेबिलिटी**:
  ऐप में एजेंट प्रदर्शन, उपयोग पैटर्न, और विलंबता की मॉनिटरिंग के लिए बिल्ट-इन [ट्रेसिंग](https://learn.microsoft.com/azure/ai-foundry/agents/concepts/tracing){:target="_blank"} और [मेट्रिक्स](https://learn.microsoft.com/azure/ai-foundry/agents/how-to/metrics){:target="_blank"} शामिल हैं। यह आपको समय के साथ समस्याओं की पहचान करने और एजेंट को अनुकूलित करने में सक्षम बनाता है।

*GitHub Copilot और GPT-4o का उपयोग करके अनुवादित।*
