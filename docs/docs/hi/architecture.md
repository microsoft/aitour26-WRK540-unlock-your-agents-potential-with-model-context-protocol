## एक नजर में मुख्य तकनीकें

- **Azure AI Foundry Agent Service**  
  LLM संचालित एजेंट को होस्ट करता है; टूल (MCP सर्वर सहित) को ऑर्केस्ट्रेट करता है; संदर्भ, Code Interpreter और टोकन स्ट्रीमिंग प्रबंधित करता है; तथा प्रमाणीकरण, लॉगिंग और स्केलिंग प्रदान करता है।
- **MCP Servers**  
  MCP (Model Context Protocol) एक खुला मानक है जो LLMs को बाहरी टूल, API और डेटा के लिए एकीकृत इंटरफ़ेस देता है। यह टूल डिस्कवरी को मानकीकृत करता है और कम्पोज़ेबिलिटी बेहतर करता है।
- **PostgreSQL + pgvector**  
  रिलेशनल डेटा और एंबेडिंग संग्रहीत करता है; SQL (रिलेशनल) और सेमान्टिक (वेक्टर) दोनों क्वेरी सपोर्ट (pgvector द्वारा), SQL और RLS से शासित।

**एक साथ:** Agent Service उपयोगकर्ता इरादे को रूट करता है; MCP सर्वर उन्हें टूल/SQL कॉल में अनुवाद करता है; PostgreSQL+pgvector सेमान्टिक और विश्लेषणात्मक प्रश्नों का उत्तर देता है।

## आर्किटेक्चर (उच्च स्तर)

```plaintext
┌─────────────────────┐                         ┌─────────────────┐
│   Zava Agent App    │       stdio/https       │   MCP Server    │
│   (app.py)          │◄───────────────────────►│ (sales_analysis)│
│                     │      MCP Transports     └─────────────────┘
│ ┌─────────────────┐ │                                 │
│ │ Azure AI        │ │                                 ▼
│ │ Agents Service  │ │                         ┌─────────────────┐
│ │ + Streaming     │ │                         │ Azure Database  │
│ │                 │ │                         │ for PostgreSQL  │
│ └─────────────────┘ │                         │   + pgvector    │
└─────────────────────┘                         └─────────────────┘
         │                                              |
         ▼                                              ▼
┌─────────────────────┐                         ┌─────────────────┐
│ Azure OpenAI        │                         │ Zava Sales      │
│ Model Deployments   │                         │ Database with   │
│ - gpt-4o-mini       │                         │ Semantic Search │
│ - text-embedding-3- │                         └─────────────────┘
│   small             │
└─────────────────────┘
```

## MCP Servers के प्रमुख लाभ

- **Interoperability** – कम कस्टम कोड के साथ किसी भी विक्रेता के MCP सक्षम टूल से कनेक्ट करें।
- **Security hooks** – साइन‑इन, अनुमति और गतिविधि लॉगिंग एकीकृत करें।
- **Reusability** – एक बार बनाएं, कई प्रोजेक्ट, क्लाउड और रनटाइम में पुन: उपयोग।
- **संचालन सरलता** – एकल कॉन्ट्रैक्ट बोइलरप्लेट और रखरखाव घटाता है।

## प्रदर्शित श्रेष्ठ अभ्यास

- **Asynchronous APIs:** Agents service और PostgreSQL async API उपयोग करते हैं; FastAPI/ASP.NET/Streamlit के साथ आदर्श।
- **Token streaming:** UI में प्रतीत विलंबता कम करता है।
- **Observability:** बिल्ट‑इन ट्रेसिंग और मेट्रिक्स मॉनिटरिंग व अनुकूलन।
- **डेटाबेस सुरक्षा:** PostgreSQL प्रतिबंधित एजेंट विशेषाधिकार और Row‑Level Security (RLS) के साथ सुरक्षित।
- **Code Interpreter:** [Azure AI Agents Service Code Interpreter](https://learn.microsoft.com/azure/ai-services/agents/how-to/tools/code-interpreter?view=azure-python-preview&tabs=python&pivots=overview){:target="_blank"} सैंडबॉक्स वातावरण में LLM द्वारा उत्पन्न कोड चलाता है।

## विस्तार क्षमता

वर्कशॉप पैटर्न (जैसे ग्राहक सहायता) को डेटाबेस + एजेंट निर्देश अपडेट करके अनुकूलित किया जा सकता है।

*GitHub Copilot द्वारा अनुवादित.*
