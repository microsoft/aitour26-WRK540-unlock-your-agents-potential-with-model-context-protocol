## Ano ang Iyong Matututuhan

Sa lab na ito, papaganahin mo ang semantic search capabilities sa Azure AI Agent gamit ang Model Context Protocol (MCP) at ang PostgreSQL database na may naka-enable na [PostgreSQL Vector](https://github.com/pgvector/pgvector){:target="_blank"} extension.

## Panimula

Ina-upgrade ng lab na ito ang Azure AI Agent gamit ang semantic search sa pamamagitan ng Model Context Protocol (MCP) at PostgreSQL. Ang mga pangalan at paglalarawan ng produkto ay na-convert sa vectors gamit ang OpenAI embedding model (text-embedding-3-small) at ini-store sa database. Pinapahintulutan nitong maunawaan ng agent ang user intent at magbigay ng mas tumpak na mga tugon.

## Lab Exercise

Mula sa nakaraang lab maaari kang magtanong sa agent tungkol sa sales data, ngunit limitado ito sa eksaktong pagtutugma. Sa lab na ito, palalawakin mo ang kakayahan ng agent sa pamamagitan ng pagpapatupad ng semantic search gamit ang Model Context Protocol (MCP). Papayagan nitong maunawaan ng agent at tugunan ang mga query na hindi eksaktong tugma, pinapahusay ang kakayahan nitong tumulong sa mas kumplikadong tanong.

1. I-paste ang sumusunod na tanong sa Web Chat tab sa iyong browser:

    ```text
    What 18 amp circuit breakers do we sell?
    ```

    Tutugon ang agent ng katulad sa mensaheng ito: "I couldn’t find any specific 18 amp circuit breakers in our inventory. However, we may have other types of circuit breakers available. Would you like me to search for general circuit breakers or any other related products? 😊"

## Itigil ang Agent App

Mula sa VS Code, itigil ang agent app sa pamamagitan ng pagpindot ng <kbd>Shift + F5</kbd>.

## Ipapatupad ang Semantic Search

Sa seksyong ito, ipapatupad mo ang semantic search gamit ang Model Context Protocol (MCP) upang mapahusay ang kakayahan ng agent.

1. Pindutin ang <kbd>F1</kbd> upang **buksan** ang VS Code Command Palette.
2. I-type ang **Open File** at piliin ang **File: Open File...**.
3. **I-paste** ang sumusunod na path sa file picker at pindutin ang <kbd>Enter</kbd>:

    ```text
    /workspace/src/python/mcp_server/sales_analysis/sales_analysis.py
    ```

4. Mag-scroll pababa bandang line 100 at hanapin ang `semantic_search_products` method. Ang method na ito ang responsable sa pagsasagawa ng semantic search sa sales data. Mapapansin mong naka-comment out ang **@mcp.tool()** decorator. Ginagamit ang decorator na ito upang irehistro ang method bilang isang MCP tool, na nagpapahintulot na ito ay matawag ng agent.

5. I-uncomment ang `@mcp.tool()` decorator sa pamamagitan ng pag-alis ng `#` sa simula ng linya. I-e-enable nito ang semantic search tool.

    ```python
    # @mcp.tool()
    async def semantic_search_products(
        ctx: Context,
        query_description: Annotated[str, Field(
        ...
    ```

6. Susunod, kailangan mong paganahin sa Agent instructions ang paggamit ng semantic search tool. Lumipat pabalik sa `app.py` file.
7. Mag-scroll pababa sa bandang line 30 at hanapin ang linyang `# INSTRUCTIONS_FILE = "instructions/mcp_server_tools_with_semantic_search.txt".
8. I-uncomment ang linya sa pamamagitan ng pag-alis ng `#` sa simula. I-e-enable nito ang agent na gamitin ang semantic search tool.

    ```python
    INSTRUCTIONS_FILE = "instructions/mcp_server_tools_with_semantic_search.txt"
    ```

## Repasuhin ang Agent Instructions

1. Pindutin ang <kbd>F1</kbd> upang buksan ang VS Code Command Palette.
2. I-type ang **Open File** at piliin ang **File: Open File...**.
3. I-paste ang sumusunod na path sa file picker at pindutin ang <kbd>Enter</kbd>:

    ```text
    /workspace/src/shared/instructions/mcp_server_tools_with_semantic_search.txt
    ```

4. Repasuhin ang instructions sa file. Ang mga instructions na ito ang nag-uutos sa agent na gamitin ang semantic search tool upang sagutin ang mga tanong tungkol sa sales data.

## I-start ang Agent App kasama ang Semantic Search Tool

1. **I-start** ang agent app sa pamamagitan ng pagpindot ng <kbd>F5</kbd>. Ia-start nito ang agent kasama ang na-update na instructions at naka-enable na semantic search tool.
2. Lumipat pabalik sa **Web Chat** tab sa iyong browser.
3. Ipasok ang sumusunod na tanong sa chat:

    ```text
    What 18 amp circuit breakers do we sell?
    ```

    Naiintindihan na ngayon ng agent ang semantic meaning ng tanong at tutugon nang naaayon gamit ang kaugnay na sales data.

    !!! info "Note"
        Gumagana ang MCP Semantic Search tool sa ganitong paraan:

        1. Ang tanong ay kino-convert sa isang vector gamit ang parehong OpenAI embedding model (text-embedding-3-small) tulad ng mga paglalarawan ng produkto.
        2. Ang vector na ito ay ginagamit upang maghanap ng mga katulad na product vectors sa PostgreSQL database.
        3. Tinatanggap ng agent ang mga resulta at ginagamit ang mga ito upang bumuo ng tugon.

## Sumulat ng Isang Executive Report

Ang huling prompt para sa workshop na ito ay ang sumusunod:

```plaintext
Write an executive report on the sales performance of different stores for these circuit breakers.
```

## Iwanang Tumatakbo ang Agent App

Iwanang tumatakbo ang agent app dahil gagamitin mo ito sa susunod na lab upang palawakin pa ang agent gamit ang mas maraming tool at kakayahan.

*Isinalin gamit ang GitHub Copilot.*
