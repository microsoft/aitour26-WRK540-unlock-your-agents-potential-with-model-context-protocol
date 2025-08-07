MCP (Model Context Protocol) एक open standard है जो AI agents को unified interface के माध्यम से external tools, APIs, और data sources तक पहुंच की अनुमति देता है। यह tool discovery और access को standardize करता है, REST services के लिए OpenAPI के समान। MCP AI system composability और agility में सुधार करता है आपकी business needs के अनुसार AI tools के updates या replacements को सरल बनाकर।

# मुख्य फायदे

- **Interoperability** – AI agents को minimal custom code के साथ किसी भी vendor के MCP-enabled tools से connect करें।
- **Security hooks** – Sign-in, permissions, और activity logging को integrate करें।
- **Reusability** – एक बार build करें, projects, clouds, और runtimes में reuse करें।
- **Operational simplicity** – Single contract boilerplate और maintenance को कम करता है।

# आर्किटेक्चर

```
┌─────────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Azure AI Agent    │    │   MCP Client    │    │   MCP Server    │
│   (main.py)         │◄──►│ (mcp_client.py) │◄──►│ (sales_analysis)│
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

MCP external resources के साथ AI agent interactions के लिए client-server model का उपयोग करता है:

- **MCP Host:** AI agent चलाने वाला runtime या platform (जैसे Azure AI Foundry Agent Service)।
- **MCP Client:** AI agent tool calls को MCP requests में convert करने वाला SDK।
- **MCP Server:** Tools को register करता है, requests execute करता है, JSON results return करता है। Authentication, authorization, और logging को support करता है।

### MCP Server पर घटक

- **Resources:** Databases, APIs, file stores जैसे data sources।
- **Tools:** Registered functions या APIs जो demand पर execute होते हैं।
- **Prompts (optional):** Reuse के लिए versioned templates।
- **Policies (optional):** Limits और safety checks (rate, depth, authentication)।

### MCP Transports

- **HTTP/HTTPS:** Streaming support के साथ standard web protocols।
- **stdio:** Runtime sharing के साथ lightweight local या containerized transport।

यह workshop local MCP communication के लिए stdio का उपयोग करती है। Production deployments scalability और security के लिए HTTPS का उपयोग करते हैं।

# Use Case

इस workshop में, MCP server Azure AI Agent को Zava के sales data से link करता है। जब आप products, sales, या inventory के बारे में पूछते हैं:

1. AI agent MCP Server requests जेनरेट करता है।
2. MCP Server:
    - Accurate queries के लिए schema info प्रदान करता है।
    - SQL queries चलाता है, structured data return करता है।
    - Time-sensitive reports के लिए time services offer करता है।

यह Zava के sales operations में real-time insights efficiently enable करता है।

*GitHub Copilot का उपयोग करके अनुवादित।*
