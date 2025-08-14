## Ano ang Matutuhan Ninyo

Sa lab na ito, ie-enable ninyo ang Code Interpreter upang mag-analyze ng sales data at gumawa ng charts gamit ang natural language.

## Introduction

Sa lab na ito, ie-extend ninyo ang Azure AI Agent na may dalawang tools:

- **Code Interpreter:** Nagbibigay-daan sa agent na mag-generate at mag-run ng Python code para sa data analysis at visualization.
- **MCP Server tools:** Nagbibigay-daan sa agent na mag-access ng external data sources gamit ang MCP Tools, sa case namin ay data sa PostgreSQL database.

## Lab Exercise

### I-enable ang Code Interpreter

Sa lab na ito, ie-enable ninyo ang Code Interpreter upang mag-execute ng Python code na na-generate ng LLM para sa pag-analyze ng Zava's retail sales data.

=== "Python"

    1. **Buksan** ang `app.py`.
    2. **I-uncomment** ang line na nagdadagdag ng Code Interpreter tool sa agent's toolset sa `_setup_agent_tools` method ng `AgentManager` class. Ang line na ito ay currently commented out na may `#` sa simula.:

        ```python
        # code_interpreter = CodeInterpreterTool()
        # self.toolset.add(code_interpreter)
        ```

    3. **Suriin** ang code sa `app.py` file. Mapapansin ninyo na ang Code Interpreter at MCP Server tools ay dinagdag sa agent's toolset sa `_setup_agent_tools` method ng `AgentManager` class.

        ```python

        Pagkatapos ng pag-uncomment, ang inyong code ay dapat maging ganito:

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

## Simulan ang Agent App

1. I-copy ang text sa ibaba sa clipboard:

    ```text
    Debug: Select and Start Debugging
    ```

2. Pindutin ang <kbd>F1</kbd> upang buksan ang VS Code Command Palette.
3. I-paste ang text sa Command Palette at piliin ang **Debug: Select and Start Debugging**.
4. Piliin ang **🔁🤖Debug Compound: Agent and MCP (stdio)** mula sa listahan. Magsisimula ito ng agent app at ng web chat client.

## Buksan ang Agent Web Chat Client

1. I-copy ang text sa ibaba sa clipboard:

    ```text
    Open Port in Browser
    ```

2. Pindutin ang <kbd>F1</kbd> upang buksan ang VS Code Command Palette.
3. I-paste ang text sa Command Palette at piliin ang **Open Port in Browser**.
4. Piliin ang **8005** mula sa listahan. Magbubukas ito ng agent web chat client sa inyong browser.

### Simulan ang Conversation sa Agent

Mula sa web chat client, makakapag-simula kayo ng conversation sa agent. Idinisenyo ang agent na sagutin ang mga tanong tungkol sa Zava's sales data at mag-generate ng visualizations gamit ang Code Interpreter.

1. Product sales analysis. I-copy at paste ang sumusunod na tanong sa chat:

    ```text
    Show the top 10 products by revenue by store for the last quarter
    ```

    Pagkatapos ng ilang sandali, sasagot ang agent na may table na nagpapakita ng top 10 products by revenue para sa bawat store.

    !!! info
        Ginagamit ng agent ang LLM na tumatawag sa tatlong MCP Server tools upang kunin ang data at ipakita ito sa table:

           1. **get_current_utc_date()**: Kumukuha ng current date at time para matukoy ng agent ang last quarter relative sa current date.
           2. **get_multiple_table_schemas()**: Kumukuha ng schemas ng mga tables sa database na kailangan ng LLM upang mag-generate ng valid SQL.
           3. **execute_sales_query**: Nag-e-execute ng SQL query upang kunin ang top 10 products by revenue para sa last quarter mula sa PostgreSQL database.

2. Mag-generate ng pie chart. I-copy at paste ang sumusunod na tanong sa chat:

    ```text
    Show sales by store as a pie chart for this financial year
    ```

    Sasagot ang agent na may pie chart na nagpapakita ng sales distribution by store para sa current financial year.

    !!! info
        Maaaring maging parang magic ito, kaya ano ang nangyayari sa likod upang gumana ang lahat?

        Nio-orchestrate ng Foundry Agent Service ang sumusunod na steps:

        1. Tulad ng nakaraang tanong, tinutukoy ng agent kung mayroon itong table schemas na kailangan para sa query. Kung wala, ginagamit nito ang **get_multiple_table_schemas()** tools upang kunin ang current date at ang database schema.
        2. Ginagamit ng agent ang **execute_sales_query** tool upang kunin ang sales
        3. Gamit ang returned data, nagsusulat ang LLM ng Python code upang gumawa ng Pie Chart.
        4. Sa wakas, ie-execute ng Code Interpreter ang Python code upang ma-generate ang chart.

3. Magpatuloy sa pagtanong tungkol sa Zava sales data upang makita ang Code Interpreter sa aksyon. Narito ang ilang follow-up questions na maaari ninyong subukan:

    - ```Determine which products or categories drive sales. Show as a Bar Chart.```
    - ```What would be the impact of a shock event (e.g., 20% sales drop in one region) on global sales distribution? Show as a Grouped Bar Chart.```
        - I-follow up ng ```What if the shock event was 50%?```
    - ```Which regions have sales above or below the average? Show as a Bar Chart with Deviation from Average.```
    - ```Which regions have discounts above or below the average? Show as a Bar Chart with Deviation from Average.```
    - ```Simulate future sales by region using a Monte Carlo simulation to estimate confidence intervals. Show as a Line with Confidence Bands using vivid colors.```

<!-- ## Stop the Agent App

1. Switch back to the VS Code editor.
1. Press <kbd>Shift + F5</kbd> to stop the agent app. -->

## Iwanang Tumatakbo ang Agent App

Iwanang tumatakbo ang agent app dahil gagamitin ninyo ito sa susunod na lab upang i-extend ang agent na may mas maraming tools at capabilities.

*Isinalin gamit ang GitHub Copilot.*
