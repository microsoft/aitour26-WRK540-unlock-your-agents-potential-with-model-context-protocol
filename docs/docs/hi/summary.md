# सारांश

इस workshop ने demonstrate किया कि Foundry Agent Service का leverage करके कैसे एक robust conversational agent बनाया जाए जो sales-related प्रश्नों के उत्तर देने, data analysis perform करने, visualizations generate करने, और enhanced insights के लिए external data sources को integrate करने में सक्षम हो। यहां मुख्य takeaways हैं:

## 1. Model Context Protocol (MCP) और Dynamic SQL Queries

- Agent PostgreSQL database के against dynamically SQL queries generate और execute करने के लिए Foundry Agent Service का उपयोग करता है, जिससे यह accurate data retrieval के साथ user questions का जवाब दे सकता है। MCP Server conversation context को manage करने और यह सुनिश्चित करने का structured way प्रदान करता है कि agent complex queries को effectively handle कर सके।

## 2. Context Management

- Agent Foundry Agent Service का उपयोग करके conversation context को efficiently manage करता है, यह सुनिश्चित करते हुए कि interactions relevant और coherent रहें।

## 3. Data Visualization

- Code Interpreter के साथ, agent user queries के based पर pie charts और tables जैसे visualizations generate कर सकता है, data को अधिक accessible और actionable बनाता है। आप multiple languages को support करने वाले visualizations create करने के लिए Code Interpreter में additional fonts attach कर सकते हैं।

## 4. File Generation

- Agent Excel, CSV, JSON, और image formats सहित downloadable files create कर सकता है, users को data का विश्लेषण और share करने के लिए flexible options प्रदान करता है।

## 5. Monitoring और Logging

- Foundry Agent Service में built-in monitoring और logging capabilities शामिल हैं, जो आपको agent performance, user interactions, और system health को track करने की अनुमति देती हैं। यह production environments में agent की reliability और effectiveness बनाए रखने के लिए crucial है।

## 6. Security Best Practices

- SQL injection जैसे security risks को read-only database access enforce करके और app को secure environment के भीतर run करके कम किया जाता है।

## 7. Multi-Language Support

- Agent और LLM multiple languages को support करते हैं, diverse linguistic backgrounds से users के लिए inclusive experience offer करते हैं।

## 8. Adaptability और Customization

- Workshop Foundry Agent Service की flexibility पर emphasis करती है, आपको instructions modify करके और additional tools integrate करके विभिन्न use cases, जैसे customer support या competitive analysis, के लिए agent को adapt करने की अनुमति देती है।

यह workshop आपको अपनी business needs के अनुरूप conversational agents बनाने और extend करने के लिए knowledge और tools से equip करती है, Foundry Agent Service की full capabilities का leverage करते हुए।

*GitHub Copilot का उपयोग करके अनुवादित।*
