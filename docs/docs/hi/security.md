यह कार्यशाला एप्लिकेशन शिक्षा और अनुकूलन के लिए डिज़ाइन किया गया है, और out-of-the-box production उपयोग के लिए अभिप्रेत नहीं है। फिर भी, यह सुरक्षा के लिए कुछ सर्वोत्तम प्रथाओं को प्रदर्शित करता है।

## दुर्भावनापूर्ण SQL हमले

LLM-generated SQL के साथ एक सामान्य चिंता injection या हानिकारक क्वेरीज़ का जोखिम है। ये जोखिम डेटाबेस अनुमतियों को सीमित करके कम किए गए हैं।

यह ऐप PostgreSQL का उपयोग करता है जिसमें एजेंट के लिए प्रतिबंधित विशेषाधिकार हैं और एक सुरक्षित वातावरण में चलता है। Row-Level Security (RLS) सुनिश्चित करता है कि एजेंट केवल अपने असाइन किए गए स्टोर के डेटा तक पहुंच सकें।

Enterprise सेटिंग्स में, डेटा आमतौर पर एक सरलीकृत स्कीमा के साथ read-only डेटाबेस या warehouse में निकाला जाता है। यह एजेंट के लिए सुरक्षित, performant, और read-only पहुंच सुनिश्चित करता है।

## Sandboxing

यह मांग पर कोड बनाने और चलाने के लिए [Azure AI Agents Service Code Interpreter](https://learn.microsoft.com/azure/ai-services/agents/how-to/tools/code-interpreter?view=azure-python-preview&tabs=python&pivots=overview){:target="_blank"} का उपयोग करता है। कोड एजेंट के दायरे से परे कार्यों को लेने से रोकने के लिए sandboxed execution environment में चलता है।

*GitHub Copilot और GPT-4o का उपयोग करके अनुवादित।*
