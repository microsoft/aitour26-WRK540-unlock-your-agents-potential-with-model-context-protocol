## Oplossingsarchitectuur

In deze workshop creëer je de Zava Sales Agent: een conversatie-agent die is ontworpen om vragen over verkoopgegevens te beantwoorden en grafieken te genereren voor Zava's retail DIY-bedrijf.

## Componenten van de Agent App

1. **Microsoft Azure services**

    Deze agent is gebouwd op Microsoft Azure services.

      - **Generatief AI-model**: Het onderliggende LLM dat deze app aandrijft is het [Azure OpenAI gpt-4o-mini](https://learn.microsoft.com/azure/ai-foundry/openai/concepts/models?tabs=global-standard%2Cstandard-chat-completions#how-do-i-access-the-gpt-4o-and-gpt-4o-mini-models){:target="_blank"} LLM.

      - **Control Plane**: De app en zijn architecturale componenten worden beheerd en gemonitord met behulp van het [Azure AI Foundry](https://ai.azure.com){:target="_blank"} portaal, toegankelijk via de browser.

2. **Azure AI Foundry (SDK)**

    De workshop wordt aangeboden in [Python](https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme?view=azure-python-preview&context=%2Fazure%2Fai-services%2Fagents%2Fcontext%2Fcontext){:target="_blank"} met behulp van de Azure AI Foundry SDK. De SDK ondersteunt belangrijke functies van de Azure AI Agents service, inclusief [Code Interpreter](https://learn.microsoft.com/azure/ai-services/agents/how-to/tools/code-interpreter?view=azure-python-preview&tabs=python&pivots=overview){:target="_blank"} en [Model Context Protocol (MCP)](https://modelcontextprotocol.io/){:target="_blank"} integratie.

3. **Database**

    De app wordt aangedreven door de Zava Sales Database, een [Azure Database for PostgreSQL flexible server](https://www.postgresql.org/){:target="_blank"} met pgvector extensie die uitgebreide verkoopgegevens bevat voor Zava's retail DIY-operaties.

    De database ondersteunt complexe queries voor verkoop-, voorraad- en klantgegevens. Row-Level Security (RLS) zorgt ervoor dat agenten alleen toegang hebben tot hun toegewezen winkels.

4. **MCP Server**

    De Model Context Protocol (MCP) server is een aangepaste Python service die fungeert als een brug tussen de agent en de PostgreSQL database. Het behandelt:

     - **Database Schema Discovery**: Haalt automatisch databaseschema's op om de agent te helpen beschikbare gegevens te begrijpen.
     - **Query Generatie**: Transformeert natuurlijke taal verzoeken naar SQL queries.
     - **Tool Uitvoering**: Voert SQL queries uit en retourneert resultaten in een formaat dat de agent kan gebruiken.
     - **Tijdservices**: Biedt tijd-gerelateerde gegevens voor het genereren van tijdgevoelige rapporten.

## Uitbreiden van de Workshop Oplossing

De workshop is gemakkelijk aan te passen aan gebruiksscenario's zoals klantenservice door de database bij te werken en Foundry Agent Service instructies aan te passen.

## Best Practices Gedemonstreerd in de App

De app demonstreert ook enkele best practices voor efficiëntie en gebruikerservaring.

- **Asynchrone API's**:
  In het workshop voorbeeld gebruiken zowel de Foundry Agent Service als PostgreSQL asynchrone API's, wat de resource-efficiëntie en schaalbaarheid optimaliseert. Deze ontwerpkeuze wordt vooral voordelig bij het implementeren van de applicatie met asynchrone webframeworks zoals FastAPI, ASP.NET of Streamlit.

- **Token Streaming**:
  Token streaming is geïmplementeerd om de gebruikerservaring te verbeteren door de waargenomen responstijden voor de LLM-aangedreven agent app te verminderen.

- **Observabiliteit**:
  De app bevat ingebouwde [tracing](https://learn.microsoft.com/azure/ai-foundry/agents/concepts/tracing){:target="_blank"} en [metrics](https://learn.microsoft.com/azure/ai-foundry/agents/how-to/metrics){:target="_blank"} om agentprestaties, gebruikspatronen en latentie te monitoren. Dit stelt je in staat om problemen te identificeren en de agent in de loop van de tijd te optimaliseren.

*Vertaald met behulp van GitHub Copilot.*
