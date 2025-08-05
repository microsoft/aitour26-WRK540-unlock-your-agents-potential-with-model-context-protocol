## Wat Je Gaat Leren

In deze lab schakel je de Code Interpreter in om verkoopgegevens te analyseren en grafieken te maken met natuurlijke taal.

## Introductie

In deze lab breid je de Azure AI Agent uit met twee tools:

- **Code Interpreter:** Laat de agent Python code genereren en uitvoeren voor data-analyse en visualisatie.
- **MCP Server tools:** Stellen de agent in staat om externe gegevensbronnen te benaderen met behulp van MCP Tools, in ons geval gegevens in een PostgreSQL database.

## Lab Oefening

### De Code Interpreter Inschakelen

In deze lab schakel je de Code Interpreter in om Python code uit te voeren die door het LLM is gegenereerd voor het analyseren van Zava's retail verkoopgegevens.

=== "Python"

    1. **Open** de `app.py`.
    2. **Uncommenteer** de regel die de Code Interpreter tool toevoegt aan de agent's toolset in de `_setup_agent_tools` methode van de `AgentManager` klasse. Deze regel is momenteel uitgecommentarieerd met een `#` aan het begin.:

        ```python
        # code_interpreter = CodeInterpreterTool()
        # self.toolset.add(code_interpreter)
        ```

    3. **Bekijk** de code in het `app.py` bestand. Je zult merken dat de Code Interpreter en MCP Server tools worden toegevoegd aan de agent's toolset in de `_setup_agent_tools` methode van de `AgentManager` klasse.

        ```python

        Na het uncommenteren zou je code er zo uit moeten zien:

        ```python
        class AgentManager:
            """Manages Azure AI Agent lifecycle and dependencies."""

            async def _setup_agent_tools(self) -> None:
                """Setup MCP tools and code interpreter."""

                # Enable the code interpreter tool
                code_interpreter = CodeInterpreterTool()
                self.toolset.add(code_interpreter)

                print("Setting up Agent tools...")
                ...
        ```

=== "C#"

    TBD

## De Agent App Starten

1. Kopieer de tekst hieronder naar het klembord:

    ```text
    Debug: Select and Start Debugging
    ```

2. Druk op <kbd>F1</kbd> om het VS Code Command Palette te openen.
3. Plak de tekst in het Command Palette en selecteer **Debug: Select and Start Debugging**.
4. Selecteer **🔁🤖Debug Compound: Agent and MCP (stdio)** uit de lijst. Dit start de agent app en de web chat client.

## De Agent Web Chat Client Openen

1. Kopieer de tekst hieronder naar het klembord:

    ```text
    Open Port in Browser
    ```

2. Druk op <kbd>F1</kbd> om het VS Code Command Palette te openen.
3. Plak de tekst in het Command Palette en selecteer **Open Port in Browser**.
4. Selecteer **8005** uit de lijst. Dit opent de agent web chat client in je browser.

### Een Gesprek Starten met de Agent

Vanuit de web chat client kun je een gesprek starten met de agent. De agent is ontworpen om vragen over Zava's verkoopgegevens te beantwoorden en visualisaties te genereren met behulp van de Code Interpreter.

1. Productverkoopanalyse. Kopieer en plak de volgende vraag in de chat:

    ```text
    Toon de top 10 producten per omzet per winkel voor het laatste kwartaal
    ```

    Na een moment zal de agent reageren met een tabel die de top 10 producten per omzet voor elke winkel toont.

    !!! info
        De agent gebruikt het LLM dat drie MCP Server tools aanroept om de gegevens op te halen en weer te geven in een tabel:

           1. **get_current_utc_date()**: Krijgt de huidige datum en tijd zodat de agent het laatste kwartaal kan bepalen relatief aan de huidige datum.
           2. **get_multiple_table_schemas()**: Krijgt de schema's van de tabellen in de database die nodig zijn door het LLM om geldige SQL te genereren.
           3. **execute_sales_query**: Voert een SQL query uit om de top 10 producten per omzet voor het laatste kwartaal op te halen uit de PostgreSQL database.

2. Genereer een taartdiagram. Kopieer en plak de volgende vraag in de chat:

    ```text
    Toon verkopen per winkel als een taartdiagram voor dit financiële jaar
    ```

    De agent zal reageren met een taartdiagram dat de verkoopdistributie per winkel toont voor het huidige financiële jaar.

    !!! info
        Dit voelt misschien als magie, dus wat gebeurt er achter de schermen om het allemaal te laten werken?

        Foundry Agent Service orkestreert de volgende stappen:

        1. Net als bij de vorige vraag bepaalt de agent of het de tabelschema's heeft die nodig zijn voor de query. Zo niet, dan gebruikt het de **get_multiple_table_schemas()** tools om de huidige datum en het databaseschema te krijgen.
        2. De agent gebruikt dan de **execute_sales_query** tool om de verkopen op te halen
        3. Met behulp van de geretourneerde gegevens schrijft het LLM Python code om een taartdiagram te maken.
        4. Ten slotte voert de Code Interpreter de Python code uit om het diagram te genereren.

3. Blijf vragen stellen over Zava verkoopgegevens om de Code Interpreter in actie te zien. Hier zijn een paar vervolgvragen die je zou kunnen proberen:

    - ```Bepaal welke producten of categorieën de verkoop aandrijven. Toon als een staafdiagram.```
    - ```Wat zou de impact zijn van een schokgebeurtenis (bijv. 20% verkoopdaling in één regio) op de wereldwijde verkoopdistributie? Toon als een gegroepeerd staafdiagram.```
        - Vervolgvraag met ```Wat als de schokgebeurtenis 50% was?```
    - ```Welke regio's hebben verkopen boven of onder het gemiddelde? Toon als een staafdiagram met afwijking van het gemiddelde.```
    - ```Welke regio's hebben kortingen boven of onder het gemiddelde? Toon als een staafdiagram met afwijking van het gemiddelde.```
    - ```Simuleer toekomstige verkopen per regio met behulp van een Monte Carlo simulatie om betrouwbaarheidsintervallen te schatten. Toon als een lijn met betrouwbaarheidsbanden met levendige kleuren.```

<!-- ## Stop the Agent App

1. Switch back to the VS Code editor.
1. Press <kbd>Shift + F5</kbd> to stop the agent app. -->

## Laat de Agent App Draaien

Laat de agent app draaien omdat je deze in de volgende lab zult gebruiken om de agent uit te breiden met meer tools en mogelijkheden.

*Vertaald met behulp van GitHub Copilot.*
