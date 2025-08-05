Deze workshop applicatie is ontworpen voor educatie en aanpassing, en is niet bedoeld voor productiegebruik out-of-the-box. Desondanks demonstreert het enkele best practices voor beveiliging.

## Kwaadaardige SQL Aanvallen

Een veelvoorkomende zorg bij LLM-gegenereerde SQL is het risico van injectie of schadelijke queries. Deze risico's worden verminderd door databasemachtigingen te beperken.

Deze app gebruikt PostgreSQL met beperkte privileges voor de agent en draait in een veilige omgeving. Row-Level Security (RLS) zorgt ervoor dat agenten alleen toegang hebben tot gegevens voor hun toegewezen winkels.

In enterprise settings worden gegevens typisch geëxtraheerd naar een read-only database of warehouse met een vereenvoudigd schema. Dit zorgt voor veilige, performante en read-only toegang voor de agent.

## Sandboxing

Dit gebruikt de [Azure AI Agents Service Code Interpreter](https://learn.microsoft.com/azure/ai-services/agents/how-to/tools/code-interpreter?view=azure-python-preview&tabs=python&pivots=overview){:target="_blank"} om code te maken en uit te voeren op aanvraag. De code draait in een sandboxed uitvoeringsomgeving om te voorkomen dat de code acties onderneemt die buiten het bereik van de agent vallen.

*Vertaald met behulp van GitHub Copilot.*
