MCP (Model Context Protocol) एक ओपन स्टैंडर्ड है जो AI एजेंट को एक unified interface के माध्यम से बाहरी टूल्स, APIs, और डेटा स्रोतों तक पहुंचने देता है। यह टूल discovery और access को मानकीकृत करता है, REST services के लिए OpenAPI के समान। MCP AI system composability और agility में सुधार करता है क्योंकि आपकी व्यावसायिक आवश्यकताएं विकसित होने पर AI टूल्स के अपडेट या replacement को सरल बनाता है।

# मुख्य लाभ

- **इंटरऑपेरेबिलिटी** – न्यूनतम कस्टम कोड के साथ AI एजेंट को किसी भी vendor के MCP-enabled tools से कनेक्ट करें।  
- **सुरक्षा hooks** – sign-in, permissions, और activity logging को एकीकृत करें।  
- **पुन: उपयोग** – एक बार बनाएं, projects, clouds, और runtimes में पुनः उपयोग करें।  
- **परिचालन सरलता** – Single contract boilerplate और maintenance को कम करता है।

# आर्किटेक्चर

```
┌─────────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Azure AI Agent    │    │   MCP Client    │    │   MCP Server    │
│   (main.py)         │◄──►│ (mcp_client.py) │◄──►│ (mcp_server_sales_analysis.py) │
│                     │    └─────────────────┘    └─────────────────┘
│ ┌─────────────────┐ │                                   │
│ │ Azure AI        │ │                                   ▼
│ │ Agents Service  │ │                           ┌─────────────────┐
│ │ + Streaming     │ │                           │ Azure Database  │
│ │                 │ │                           │ for PostgreSQL  │
│ └─────────────────┘ │                           │       +         │
└─────────────────────┘                           │    pgvector     │
         │                                        └─────────────────┘
         ▼                                                │
┌─────────────────────┐                           ┌─────────────────┐
│ Azure OpenAI        │                           │ 8 Normalized    │
│ Model Deployment    │                           │ Tables with     │
│ (GPT-4, etc.)       │                           │ Performance     │
└─────────────────────┘                           │ Indexes         │
                                                  └─────────────────┘
```

# यह कैसे काम करता है

MCP बाहरी संसाधनों के साथ AI एजेंट बातचीत के लिए client-server model का उपयोग करता है:

- **MCP Host:** AI एजेंट चलाने वाला runtime या platform (जैसे Azure AI Foundry Agent Service)।  
- **MCP Client:** AI एजेंट टूल कॉल्स को MCP requests में रूपांतरित करने वाला SDK।  
- **MCP Server:** टूल्स register करता है, requests निष्पादित करता है, JSON results लौटाता है। Authentication, authorization, और logging का समर्थन करता है।

### MCP Server पर घटक

- **Resources:** डेटाबेस, APIs, file stores जैसे डेटा स्रोत।  
- **Tools:** मांग पर निष्पादित registered functions या APIs।  
- **Prompts (optional):** पुनः उपयोग के लिए versioned templates।  
- **Policies (optional):** Limits और safety checks (rate, depth, authentication)।

### MCP Transports

- **HTTP/HTTPS:** Streaming support के साथ मानक वेब protocols।  
- **stdio:** Runtime साझा करने वाला lightweight local या containerized transport।

यह कार्यशाला स्थानीय MCP संचार के लिए stdio का उपयोग करती है। Production deployments scalability और security के लिए HTTPS का उपयोग करते हैं।

# उपयोग का मामला

इस कार्यशाला में, MCP server Azure AI Agent को Zava के sales data से जोड़ता है। जब आप products, sales, या inventory के बारे में पूछते हैं:

1. AI एजेंट MCP Server requests जेनरेट करता है।  
2. MCP Server:  
    - सटीक क्वेरीज़ के लिए schema info प्रदान करता है।  
    - SQL क्वेरीज़ चलाता है, structured data लौटाता है।  
    - समय-संवेदनशील रिपोर्ट के लिए time services प्रदान करता है।

यह कुशलतापूर्वक Zava के sales operations में real-time insights सक्षम करता है।

*GitHub Copilot और GPT-4o का उपयोग करके अनुवादित।*
