## Wat Je Gaat Leren

In deze lab ga je:

- DevTunnel gebruiken om je lokale MCP server toegankelijk te maken voor cloud-gebaseerde agent services
- Je omgeving opzetten voor hands-on experimenten met het Model Context Protocol

## Introductie

De Model Context Protocol (MCP) server is een cruciaal component dat de communicatie tussen Large Language Models (LLMs) en externe tools en gegevensbronnen afhandelt. Je draait de MCP server op je lokale machine, maar de Azure AI Foundry Agent Service heeft internettoegang nodig om ermee te verbinden. Om je lokale MCP server toegankelijk te maken vanaf het internet, gebruik je een DevTunnel. Dit stelt de Agent Service in staat om met je MCP server te communiceren alsof deze als een service in Azure draait.

## Interface opties voor MCP

MCP ondersteunt twee hoofdinterfaces voor het verbinden van LLMs met tools:

- **Streamable HTTP Transport**: Voor web-gebaseerde API's en services.
- **Stdio Transport**: Voor lokale scripts en commandoregel tools.

Deze lab gebruikt de Streamable HTTP transport interface om te integreren met de Azure AI Foundry Agent Service.

!!! note
    Normaal zou je de MCP server in een productieomgeving implementeren, maar voor deze workshop draai je hem lokaal in je ontwikkelomgeving. Dit stelt je in staat om te testen en te interacteren met de MCP tools zonder een volledige implementatie nodig te hebben.

### Een DevTunnel opstarten voor de MCP Server

1. In een nieuwe terminal, authenticeer DevTunnel. Je wordt gevraagd om in te loggen met je Azure account, gebruik hetzelfde account dat je hebt gebruikt om in te loggen bij de Azure AI Foundry Agent Service of Azure Portal. Voer het volgende commando uit:

    ```bash
    devtunnel login
    ```

1. Vervolgens, in de terminal waar de MCP server draait, start een DevTunnel door het volgende uit te voeren:

    ```bash
    devtunnel host -p 8000 --allow-anonymous
    ```

    Dit geeft een URL uit die je nodig hebt voor de agent om verbinding te maken met de MCP server. De output zal er ongeveer zo uitzien:

    ```text
    Hosting port: 8000
    Connect via browser: https://<tunnel-id>-8000.aue.devtunnels.ms
    Inspect network activity: https://<tunnel-id>-8000-inspect.aue.devtunnels.ms
    ```

## De DevTunnel Omgevingsvariabele Bijwerken

1. Kopieer de **Connect via browser** URL naar het klembord - je hebt deze nodig in de volgende lab om de agent te configureren.
2. Open het `.env` bestand in de workshop map.
3. Werk de `DEV_TUNNEL_URL` variabele bij met de gekopieerde URL.

    ```text
    DEV_TUNNEL_URL=https://<tunnel-id>-8000.aue.devtunnels.ms
    ```

## De Agent App Starten

1. Kopieer de tekst hieronder naar het klembord:

    ```text
    Debug: Select and Start Debugging
    ```

2. Druk op <kbd>F1</kbd> om het VS Code Command Palette te openen.
3. Plak de tekst in het Command Palette en selecteer **Debug: Select and Start Debugging**.
4. Selecteer **🌎🤖Debug Compound: Agent and MCP (http)** uit de lijst. Dit start de agent app en de web chat client.

## Een gesprek starten met de Agent

Ga naar het **Web Chat** tabblad in je browser. Je zou de agent app moeten zien draaien en klaar om vragen te accepteren.

### Debuggen met DevTunnel

Je kunt DevTunnel gebruiken om de MCP server en de agent app te debuggen. Dit stelt je in staat om netwerkactiviteit te inspecteren en problemen in realtime op te lossen.

1. Selecteer de **Inspect network activity** URL uit de DevTunnel output.
2. Dit opent een nieuw tabblad in je browser waar je de netwerkactiviteit van de MCP server en de agent app kunt zien.
3. Je kunt dit gebruiken om eventuele problemen die ontstaan tijdens de workshop te debuggen.

Je kunt ook breakpoints instellen in de MCP server code en de agent app code om specifieke problemen te debuggen. Om dit te doen:

1. Open het `sales_analysis.py` bestand in de `mcp_server` map.
2. Stel een breakpoint in door te klikken in de gutter naast het regelnummer waar je de uitvoering wilt pauzeren.
3. Wanneer de uitvoering het breakpoint bereikt, kun je variabelen inspecteren, door code stappen en expressies evalueren in de Debug Console.

*Vertaald met behulp van GitHub Copilot.*
