## समाधान आर्किटेक्चर

इस वर्कशॉप में, आप Zava Sales Agent बनाएंगे: एक कन्वर्सेशनल एजेंट जो सेल्स डेटा के बारे में प्रश्नों के उत्तर देने, Zava के रिटेल DIY बिजनेस के लिए चार्ट जेनरेट करने के लिए डिज़ाइन किया गया है।

## Agent App के घटक

1. **Microsoft Azure सेवाएं**

    यह एजेंट Microsoft Azure सेवाओं पर बनाया गया है।

      - **जेनेरेटिव AI मॉडल**: इस ऐप को पावर करने वाला अंतर्निहित LLM [Azure OpenAI gpt-4o-mini](https://learn.microsoft.com/azure/ai-foundry/openai/concepts/models?tabs=global-standard%2Cstandard-chat-completions#how-do-i-access-the-gpt-4o-and-gpt-4o-mini-models){:target="_blank"} LLM है।

      - **कंट्रोल प्लेन**: ऐप और इसके आर्किटेक्चरल घटकों को [Azure AI Foundry](https://ai.azure.com){:target="_blank"} पोर्टल का उपयोग करके प्रबंधित और मॉनिटर किया जाता है, जो ब्राउज़र के माध्यम से पहुंच योग्य है।

2. **Azure AI Foundry (SDK)**

    वर्कशॉप Azure AI Foundry SDK का उपयोग करके [Python](https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme?view=azure-python-preview&context=%2Fazure%2Fai-services%2Fagents%2Fcontext%2Fcontext){:target="_blank"} में प्रदान की जाती है। SDK Azure AI Agents सेवा की मुख्य सुविधाओं को सपोर्ट करता है, जिसमें [Code Interpreter](https://learn.microsoft.com/azure/ai-services/agents/how-to/tools/code-interpreter?view=azure-python-preview&tabs=python&pivots=overview){:target="_blank"} और [Model Context Protocol (MCP)](https://modelcontextprotocol.io/){:target="_blank"} इंटीग्रेशन शामिल है।

3. **डेटाबेस**

    ऐप Zava Sales Database द्वारा संचालित है, एक [Azure Database for PostgreSQL flexible server](https://www.postgresql.org/){:target="_blank"} जो pgvector extension के साथ Zava के रिटेल DIY ऑपरेशन्स के लिए व्यापक सेल्स डेटा शामिल करता है।

    डेटाबेस सेल्स, इन्वेंटरी, और कस्टमर डेटा के लिए जटिल क्वेरीज़ को सपोर्ट करता है। Row-Level Security (RLS) सुनिश्चित करती है कि एजेंट्स केवल अपने असाइन्ड स्टोर्स तक पहुंच सकें।

4. **MCP Server**

    Model Context Protocol (MCP) सर्वर एक कस्टम Python सेवा है जो एजेंट और PostgreSQL डेटाबेस के बीच एक ब्रिज का काम करती है। यह हैंडल करती है:

     - **डेटाबेस स्कीमा डिस्कवरी**: एजेंट को उपलब्ध डेटा समझने में मदद करने के लिए स्वचालित रूप से डेटाबेस स्कीमा प्राप्त करती है।
     - **क्वेरी जेनरेशन**: प्राकृतिक भाषा अनुरोधों को SQL क्वेरीज़ में रूपांतरित करती है।
     - **टूल एक्जीक्यूशन**: SQL क्वेरीज़ को एक्जीक्यूट करती है और परिणामों को ऐसे फॉर्मेट में वापस करती है जिसका एजेंट उपयोग कर सके।
     - **टाइम सेवाएं**: समय-संवेदनशील रिपोर्ट्स जेनरेट करने के लिए समय से संबंधित डेटा प्रदान करती है।

## वर्कशॉप समाधान का विस्तार

वर्कशॉप को डेटाबेस अपडेट करके और Foundry Agent Service निर्देशों को कस्टमाइज़ करके कस्टमर सपोर्ट जैसे उपयोग मामलों के लिए आसानी से अनुकूलित किया जा सकता है।

## ऐप में प्रदर्शित सर्वोत्तम प्रथाएं

ऐप दक्षता और उपयोगकर्ता अनुभव के लिए कुछ सर्वोत्तम प्रथाओं का भी प्रदर्शन करता है।

- **एसिंक्रोनस APIs**:
  वर्कशॉप सैंपल में, Foundry Agent Service और PostgreSQL दोनों एसिंक्रोनस APIs का उपयोग करते हैं, रिसोर्स दक्षता और स्केलेबिलिटी को अनुकूलित करते हैं। यह डिज़ाइन चुनाव विशेष रूप से तब फायदेमंद होता है जब एप्लिकेशन को FastAPI, ASP.NET, या Streamlit जैसे एसिंक्रोनस वेब फ्रेमवर्क्स के साथ तैनात किया जाता है।

- **टोकन स्ट्रीमिंग**:
  LLM-पावर्ड एजेंट ऐप के लिए अनुभवित प्रतिक्रिया समय को कम करके उपयोगकर्ता अनुभव में सुधार के लिए टोकन स्ट्रीमिंग को लागू किया गया है।

- **ऑब्जर्वेबिलिटी**:
  ऐप में एजेंट प्रदर्शन, उपयोग पैटर्न, और लेटेंसी को मॉनिटर करने के लिए बिल्ट-इन [ट्रेसिंग](https://learn.microsoft.com/azure/ai-foundry/agents/concepts/tracing){:target="_blank"} और [मेट्रिक्स](https://learn.microsoft.com/azure/ai-foundry/agents/how-to/metrics){:target="_blank"} शामिल हैं। यह आपको समय के साथ समस्याओं की पहचान करने और एजेंट को अनुकूलित करने में सक्षम बनाता है।

*GitHub Copilot का उपयोग करके अनुवादित।*
