MCP (Model Context Protocol) is een open standaard die AI-agenten laat toegang krijgen tot externe tools, API's en gegevensbronnen via een uniforme interface. Het standaardiseert tool discovery en toegang, vergelijkbaar met OpenAPI voor REST services. MCP verbetert de composabiliteit en wendbaarheid van AI-systemen door updates of vervangingen van AI-tools te vereenvoudigen naarmate je bedrijfsbehoeften evolueren.

# Belangrijkste Voordelen

- **Interoperabiliteit** – Verbind AI-agenten met MCP-enabled tools van elke leverancier met minimale aangepaste code.
- **Beveiligingshooks** – Integreer inloggen, machtigingen en activiteitenlogboeken.
- **Herbruikbaarheid** – Bouw eens, hergebruik over projecten, clouds en runtimes.
- **Operationele eenvoud** – Enkelvoudige overeenkomst vermindert boilerplate en onderhoud.

# Architectuur

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
│ Azure OpenAI        │                           │ 8 Genormaliseerde│
│ Model Deployment    │                           │ Tabellen met    │
│ (GPT-4, etc.)       │                           │ Prestatie       │
└─────────────────────┘                           │ Indexen         │
                                                  └─────────────────┘
```

# Hoe Het Werkt

MCP gebruikt een client-server model voor AI agent interacties met externe resources:

- **MCP Host:** Runtime of platform dat de AI agent draait (bijv. Azure AI Foundry Agent Service).
- **MCP Client:** SDK die AI agent tool calls omzet naar MCP requests.
- **MCP Server:** Registreert tools, voert requests uit, retourneert JSON resultaten. Ondersteunt authenticatie, autorisatie en logging.

### Componenten op MCP Server

- **Resources:** Gegevensbronnen zoals databases, API's, bestandsopslag.
- **Tools:** Geregistreerde functies of API's die op aanvraag worden uitgevoerd.
- **Prompts (optioneel):** Versioned templates voor hergebruik.
- **Policies (optioneel):** Limieten en veiligheidscontroles (rate, depth, authenticatie).

### MCP Transports

- **HTTP/HTTPS:** Standaard webprotocollen met streaming ondersteuning.
- **stdio:** Lichtgewicht lokaal of gecontaineriseerd transport dat runtime deelt.

Deze workshop gebruikt stdio voor lokale MCP communicatie. Productie implementaties gebruiken HTTPS voor schaalbaarheid en beveiliging.

# Gebruiksscenario

In deze workshop verbindt de MCP server de Azure AI Agent met Zava's verkoopgegevens. Wanneer je vragen stelt over producten, verkopen of voorraad:

1. De AI agent genereert MCP Server requests.
2. De MCP Server:
    - Biedt schema-informatie voor nauwkeurige queries.
    - Voert SQL queries uit, retourneert gestructureerde gegevens.
    - Biedt tijdservices voor tijdgevoelige rapporten.

Dit maakt real-time inzichten in Zava's verkoopoperaties efficiënt mogelijk.

*Vertaald met behulp van GitHub Copilot.*
