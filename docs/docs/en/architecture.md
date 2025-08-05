## Solution Architecture

In this workshop, you will create the Zava Sales Agent: a conversational agent designed to answer questions about sales data, generate charts, provide product recommendations, and support image-based product searches for Zava's retail DIY business.

## Components of the Agent App

1. **Microsoft Azure services**

    This agent is built on Microsoft Azure services.

      - **Generative AI model**: The underlying LLM powering this app is the [Azure OpenAI gpt-4o-mini](https://learn.microsoft.com/azure/ai-foundry/openai/concepts/models?tabs=global-standard%2Cstandard-chat-completions#how-do-i-access-the-gpt-4o-and-gpt-4o-mini-models){:target="_blank"} LLM.

      - **Control Plane**: The app and its architectural components are managed and monitored using the [Azure AI Foundry](https://ai.azure.com){:target="_blank"} portal, accessible via the browser.

2. **Azure AI Foundry (SDK)**

    The workshop is offered in [Python](https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme?view=azure-python-preview&context=%2Fazure%2Fai-services%2Fagents%2Fcontext%2Fcontext){:target="_blank"} using the Azure AI Foundry SDK. The SDK supports key features of the Azure AI Agents service, including [Code Interpreter](https://learn.microsoft.com/azure/ai-services/agents/how-to/tools/code-interpreter?view=azure-python-preview&tabs=python&pivots=overview){:target="_blank"} and [Model Context Protocol (MCP)](https://modelcontextprotocol.io/){:target="_blank"} integration.

3. **Database**

    The app is powered by the Zava Sales Database, a [Azure Database for PostgreSQL flexible server](https://www.postgresql.org/){:target="_blank"} with pgvector extension containing comprehensive sales data for Zava's retail DIY operations. 

    The database supports complex queries for sales, inventory, and customer data. Row-Level Security (RLS) ensures agents access only their assigned stores.

4. **MCP Server**

    The Model Context Protocol (MCP) server is a custom Python service that acts as a bridge between the agent and the PostgreSQL database. It handles:

     - **Database Schema Discovery**: Automatically retrieves database schemas to help the agent understand available data.
     - **Query Generation**: Transforms natural language requests into SQL queries.
     - **Tool Execution**: Executes SQL queries and returns results in a format the agent can use.
     - **Time Services**: Provides time-related data for generating time-sensitive reports.

## Extending the Workshop Solution

The workshop is easily adaptable to use cases like customer support by updating the database and customizing Foundry Agent Service instructions.

## Best Practices Demonstrated in the App

The app also demonstrates some best practices for efficiency and user experience.

- **Asynchronous APIs**:
  In the workshop sample, both the Foundry Agent Service and PostgreSQL use asynchronous APIs, optimizing resource efficiency and scalability. This design choice becomes especially advantageous when deploying the application with asynchronous web frameworks like FastAPI, ASP.NET, or Streamlit.

- **Token Streaming**:
  Token streaming is implemented to improve user experience by reducing perceived response times for the LLM-powered agent app.

- **Observability**:
  The app includes built-in [tracing](https://learn.microsoft.com/azure/ai-foundry/agents/concepts/tracing){:target="_blank"} and [metrics](https://learn.microsoft.com/azure/ai-foundry/agents/how-to/metrics){:target="_blank"} to monitor agent performance, usage patterns, and latency. This enables you to identify issues and optimize the agent over time.
