## Ano ang Matutuhan Ninyo

Sa lab na ito, ie-enable ninyo ang semantic search capabilities sa Azure AI Agent gamit ang Model Context Protocol (MCP) at ang PostgreSQL database na may na-enable na [PostgreSQL Vector](https://github.com/pgvector/pgvector){:target="_blank"} extension.

## Introduction

Iniupgrade ng lab na ito ang Azure AI Agent na may semantic search gamit ang Model Context Protocol (MCP) at PostgreSQL. Ang mga product names at descriptions ay na-convert sa mga vectors gamit ang OpenAI embedding model (text-embedding-3-small) at na-store sa database. Nagbibigay-daan ito sa agent na maintindihan ang user intent at magbigay ng mas accurate na responses.

## Lab Exercise

Mula sa nakaraang lab, makakapag-tanong kayo sa agent tungkol sa sales data, pero limitado ito sa exact matches. Sa lab na ito, ie-extend ninyo ang capabilities ng agent sa pamamagitan ng pag-implement ng semantic search gamit ang Model Context Protocol (MCP). Magbibigay-daan ito sa agent na maintindihan at tumugon sa mga queries na hindi exact matches, na nagpapahusay sa kakayahan nitong tumulong sa mga users na may mas complex na tanong.

1. I-paste ang sumusunod na tanong sa Web Chat tab sa inyong browser:

    ```text
    What 18 amp circuit breakers do we sell?
    ```

    Sasagot ang agent na may katulad ng mensaheng ito: "I couldn't find any specific 18 amp circuit breakers in our inventory. However, we may have other types of circuit breakers available. Would you like me to search for general circuit breakers or any other related products? 😊"

## Ihinto ang Agent App

Mula sa VS Code, ihinto ang agent app sa pamamagitan ng pagpindot ng <kbd>Shift + F5</kbd>.

## I-implement ang Semantic Search

Sa section na ito, ie-implement ninyo ang semantic search gamit ang Model Context Protocol (MCP) upang mapahusay ang capabilities ng agent.

1. Pindutin ang <kbd>F1</kbd> upang **buksan** ang VS Code Command Palette.
2. I-type ang **Open File** at piliin ang **File: Open File...**.
3. **I-paste** ang sumusunod na path sa file picker at pindutin ang <kbd>Enter</kbd>:

    ```text
    /workspace/src/python/mcp_server/sales_analysis/sales_analysis.py
    ```

4. Mag-scroll down sa paligid ng line 100 at hanapin ang `semantic_search_products` method. Ang method na ito ay responsable sa pagsasagawa ng semantic search sa sales data. Mapapansin ninyo na ang **@mcp.tool()** decorator ay naka-comment out. Ginagamit ang decorator na ito upang ma-register ang method bilang MCP tool, na nagbibigay-daan sa agent na tawagin ito.

5. I-uncomment ang `@mcp.tool()` decorator sa pamamagitan ng pag-alis ng `#` sa simula ng line. Magkakaroon ng kakayahan ang semantic search tool.

    ```python
    # @mcp.tool()
    async def semantic_search_products(
        ctx: Context,
        query_description: Annotated[str, Field(
        ...
    ```

6. Susunod, kailangan ninyong i-enable ang Agent instructions na gamitin ang semantic search tool. Bumalik sa `app.py` file.
7. Mag-scroll down sa paligid ng line 30 at hanapin ang line na `# INSTRUCTIONS_FILE = "instructions/mcp_server_tools_with_semantic_search.txt".
8. I-uncomment ang line sa pamamagitan ng pag-alis ng `#` sa simula. Magkakaroon ng kakayahan ang agent na gamitin ang semantic search tool.

    ```python
    INSTRUCTIONS_FILE = "instructions/mcp_server_tools_with_semantic_search.txt"
    ```

## Suriin ang Agent Instructions

1. Pindutin ang <kbd>F1</kbd> upang buksan ang VS Code Command Palette.
2. I-type ang **Open File** at piliin ang **File: Open File...**.
3. I-paste ang sumusunod na path sa file picker at pindutin ang <kbd>Enter</kbd>:

    ```text
    /workspace/src/shared/instructions/mcp_server_tools_with_semantic_search.txt
    ```

4. Suriin ang mga instructions sa file. Ang mga instructions na ito ay nag-instruct sa agent na gamitin ang semantic search tool upang sagutin ang mga tanong tungkol sa sales data.

## Simulan ang Agent App na may Semantic Search Tool

1. **Simulan** ang agent app sa pamamagitan ng pagpindot ng <kbd>F5</kbd>. Magsisimula ito ng agent na may updated instructions at na-enable na semantic search tool.
2. Bumalik sa **Web Chat** tab sa inyong browser.
3. Ilagay ang sumusunod na tanong sa chat:

    ```text
    What 18 amp circuit breakers do we sell?
    ```

    Maintindihan na ngayon ng agent ang semantic meaning ng tanong at tumutugon nang naaayon na may relevant sales data.

    !!! info "Note"
        Gumagana ang MCP Semantic Search tool sa sumusunod na paraan:

        1. Ang tanong ay na-convert sa vector gamit ang parehong OpenAI embedding model (text-embedding-3-small) tulad ng product descriptions.
        2. Ginagamit ang vector na ito upang maghanap ng mga katulad na product vectors sa PostgreSQL database.
        3. Natanggap ng agent ang mga results at ginagamit ang mga ito upang mag-generate ng response.

## Sumulat ng Executive Report

Ang huling prompt para sa workshop na ito ay ang sumusunod:

```plaintext
Write an executive report on the sales performance of different stores for these circuit breakers.
```

## Iwanang Tumatakbo ang Agent App

Iwanang tumatakbo ang agent app dahil gagamitin ninyo ito sa susunod na lab upang i-extend ang agent na may mas maraming tools at capabilities.

*Isinalin gamit ang GitHub Copilot.*
