## Wat Je Gaat Leren

In deze lab schakel je semantische zoekmogelijkheden in de Azure AI Agent in met behulp van het Model Context Protocol (MCP) en de PostgreSQL database.

## Introductie

Deze lab upgradet de Azure AI Agent met semantisch zoeken met behulp van Model Context Protocol (MCP) en PostgreSQL. Productnamen en beschrijvingen werden omgezet naar vectoren met het OpenAI embedding model (text-embedding-3-small) en opgeslagen in de database. Dit stelt de agent in staat om gebruikersintentie te begrijpen en nauwkeurigere antwoorden te geven.

## Lab Oefening

Vanuit de vorige lab kun je de agent vragen stellen over verkoopgegevens, maar het was beperkt tot exacte overeenkomsten. In deze lab breid je de mogelijkheden van de agent uit door semantisch zoeken te implementeren met behulp van het Model Context Protocol (MCP). Dit stelt de agent in staat om vragen te begrijpen en beantwoorden die geen exacte overeenkomsten zijn, waardoor het vermogen om gebruikers te helpen met complexere vragen wordt verbeterd.

1. Plak de volgende vraag in het Web Chat tabblad in je browser:

    ```text
    Hoe presteerden verschillende winkels met 18A breakers?
    ```

    De agent reageert: "Ik kon geen verkoopgegevens vinden voor 18A breakers in onze records. 😱 Echter, hier zijn enkele suggesties voor vergelijkbare producten die je zou willen verkennen." Dit gebeurt omdat de agent alleen vertrouwt op het matchen van queries door trefwoorden en de semantische betekenis van je vraag niet begrijpt. Het LLM kan nog steeds geïnformeerde productsuggestions doen vanuit elke productcontext die het al heeft.

## Semantisch Zoeken Implementeren

In deze sectie implementeer je semantisch zoeken met behulp van het Model Context Protocol (MCP) om de mogelijkheden van de agent te verbeteren.

1. Druk op <kbd>F1</kbd> om het VS Code Command Palette te **openen**.
2. Type **Open File** en selecteer **File: Open File...**.
3. **Plak** het volgende pad in de bestandskiezer en druk op <kbd>Enter</kbd>:

    ```text
    /workspace/src/python/mcp_server/sales_analysis/sales_analysis.py
    ```

4. Scroll naar beneden tot ongeveer regel 100 en zoek naar de `semantic_search_products` methode. Deze methode is verantwoordelijk voor het uitvoeren van semantisch zoeken op de verkoopgegevens. Je zult merken dat de **@mcp.tool()** decorator is uitgecommentarieerd. Deze decorator wordt gebruikt om de methode te registreren als een MCP tool, waardoor deze door de agent kan worden aangeroepen.

5. Uncommenteer de `@mcp.tool()` decorator door de `#` aan het begin van de regel te verwijderen. Dit schakelt de semantische zoektool in.

    ```python
    # @mcp.tool()
    async def semantic_search_products(
        ctx: Context,
        query_description: Annotated[str, Field(
        ...
    ```

6. Vervolgens moet je de Agent instructies inschakelen om de semantische zoektool te gebruiken. Ga terug naar het `app.py` bestand.
7. Scroll naar beneden tot ongeveer regel 30 en vind de regel `# INSTRUCTIONS_FILE = "instructions/mcp_server_tools_with_semantic_search.txt".
8. Uncommenteer de regel door de `#` aan het begin te verwijderen. Dit stelt de agent in staat om de semantische zoektool te gebruiken.

    ```python
    INSTRUCTIONS_FILE = "instructions/mcp_server_tools_with_semantic_search.txt"
    ```

## De Agent Instructies Bekijken

1. Druk op <kbd>F1</kbd> om het VS Code Command Palette te openen.
2. Type **Open File** en selecteer **File: Open File...**.
3. Plak het volgende pad in de bestandskiezer en druk op <kbd>Enter</kbd>:

    ```text
    /workspace/src/shared/instructions/mcp_server_tools_with_semantic_search.txt
    ```

4. Bekijk de instructies in het bestand. Deze instructies instrueren de agent om de semantische zoektool te gebruiken om vragen over verkoopgegevens te beantwoorden.

## De Agent App Starten met de Semantische Zoektool

1. **Stop** de huidige agent app door op <kbd>Shift + F5</kbd> te drukken.
2. **Herstart** de agent app door op <kbd>F5</kbd> te drukken. Dit start de agent met de bijgewerkte instructies en de semantische zoektool ingeschakeld.
3. Ga terug naar het **Web Chat** tabblad in je browser.
4. Voer de volgende vraag in de chat in:

    ```text
    Hoe presteerden verschillende winkels met 18A breakers?
    ```

    De agent begrijpt nu de semantische betekenis van de vraag en reageert dienovereenkomstig met relevante verkoopgegevens.

    !!! info "Opmerking"
        De MCP Semantische Zoektool werkt als volgt:

        1. De vraag wordt omgezet naar een vector met hetzelfde OpenAI embedding model (text-embedding-3-small) als de productbeschrijvingen.
        2. Deze vector wordt gebruikt om te zoeken naar vergelijkbare productvectoren in de PostgreSQL database.
        3. De agent ontvangt de resultaten en gebruikt ze om een antwoord te genereren.

*Vertaald met behulp van GitHub Copilot.*
