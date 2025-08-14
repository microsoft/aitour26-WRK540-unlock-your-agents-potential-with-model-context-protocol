## Ano ang Iyong Matututuhan

Sa lab na ito, iyo nang papaganahin ang Code Interpreter upang magsuri ng sales data at lumikha ng charts gamit ang natural language.

## Panimula

Sa lab na ito, palalawakin mo ang Azure AI Agent gamit ang dalawang tool:

- **Code Interpreter:** Pinapahintulutan ang agent na bumuo at magpatakbo ng Python code para sa data analysis at visualization.
- **MCP Server tools:** Nagbibigay-daan sa agent na i-access ang panlabas na mga pinagkukunan ng datos gamit ang MCP Tools, sa ating kaso datos sa isang PostgreSQL database.

## Lab Exercise

### Paganahin ang Code Interpreter

Sa lab na ito, papaganahin mo ang Code Interpreter upang magpatupad ng Python code na binuo ng LLM para sa pagsusuri ng retail sales data ng Zava.

=== "Python"

    1. **Buksan** ang `app.py`.
    2. **I-uncomment** ang linyang nagdaragdag ng Code Interpreter tool sa agent's toolset sa `_setup_agent_tools` method ng `AgentManager` class. Ang linyang ito ay kasalukuyang naka-comment gamit ang `#` sa simula:

        ```python
        # code_interpreter = CodeInterpreterTool()
        # self.toolset.add(code_interpreter)
        ```

    3. **Repasuhin** ang code sa `app.py` file. Mapapansin mong idinaragdag ang Code Interpreter at MCP Server tools sa agent's toolset sa `_setup_agent_tools` method ng `AgentManager` class.

        ```python

        Pagkatapos i-uncomment, ang iyong code ay dapat ganito ang hitsura:

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

## I-start ang Agent App

1. Kopyahin ang text sa ibaba sa clipboard:

    ```text
    Debug: Select and Start Debugging
    ```

2. Pindutin ang <kbd>F1</kbd> upang buksan ang VS Code Command Palette.
3. I-paste ang text sa Command Palette at piliin ang **Debug: Select and Start Debugging**.
4. Piliin ang **🔁🤖Debug Compound: Agent and MCP (stdio)** mula sa listahan. Ia-start nito ang agent app at ang web chat client.

## Buksan ang Agent Web Chat Client

1. Kopyahin ang text sa ibaba sa clipboard:

    ```text
    Open Port in Browser
    ```

2. Pindutin ang <kbd>F1</kbd> upang buksan ang VS Code Command Palette.
3. I-paste ang text sa Command Palette at piliin ang **Open Port in Browser**.
4. Piliin ang **8005** mula sa listahan. Bubuksan nito ang agent web chat client sa iyong browser.

### Mag-umpisa ng Usapan sa Agent

Mula sa web chat client, maaari kang magsimula ng usapan sa agent. Dinisenyo ang agent upang sumagot ng mga tanong tungkol sa sales data ng Zava at bumuo ng visualizations gamit ang Code Interpreter.

1. Pagsusuri ng product sales. Kopyahin at i-paste ang sumusunod na tanong sa chat:

    ```text
    Show the top 10 products by revenue by store for the last quarter
    ```

    Pagkalipas ng ilang sandali, tutugon ang agent ng isang table na nagpapakita ng top 10 products ayon sa revenue para sa bawat store.

    !!! info
        Gumagamit ang agent ng LLM at tumatawag ng tatlong MCP Server tools upang kunin ang datos at ipakita ito sa isang table:

           1. **get_current_utc_date()**: Kinukuha ang kasalukuyang petsa at oras upang matukoy ng agent ang huling quarter relative sa kasalukuyang petsa.
           2. **get_multiple_table_schemas()**: Kinukuha ang schemas ng mga talahanayan sa database na kailangan ng LLM upang bumuo ng valid SQL.
           3. **execute_sales_query**: Nagpapatupad ng SQL query upang kunin ang top 10 products ayon sa revenue para sa huling quarter mula sa PostgreSQL database.

2. Bumuo ng pie chart. Kopyahin at i-paste ang sumusunod na tanong sa chat:

    ```text
    Show sales by store as a pie chart for this financial year
    ```

    Tutugon ang agent ng isang pie chart na nagpapakita ng distribusyon ng sales ayon sa store para sa kasalukuyang financial year.

    !!! info
        Maaaring parang mahika ito, kaya ano ang nangyayari sa likod ng mga eksena upang gumana ang lahat?

        Ipinapagana ng Foundry Agent Service ang sumusunod na mga hakbang:

        1. Tulad ng nakaraang tanong, tinutukoy ng agent kung mayroon na ito ng table schemas na kailangan para sa query. Kung wala, ginagamit nito ang **get_multiple_table_schemas()** tools upang kunin ang kasalukuyang petsa at ang database schema.
        2. Pagkatapos ay ginagamit ng agent ang **execute_sales_query** tool upang kunin ang sales
        3. Gamit ang ibinalik na datos, nagsusulat ang LLM ng Python code upang lumikha ng isang Pie Chart.
        4. Sa wakas, isinasagawa ng Code Interpreter ang Python code upang bumuo ng chart.

3. Magpatuloy sa pagtatanong tungkol sa Zava sales data upang makita ang Code Interpreter na gumagana. Narito ang ilang follow-up na tanong na maaari mong subukan:

    - ```Determine which products or categories drive sales. Show as a Bar Chart.```
    - ```What would be the impact of a shock event (e.g., 20% sales drop in one region) on global sales distribution? Show as a Grouped Bar Chart.```
        - Kasunod nito ang ```What if the shock event was 50%?```
    - ```Which regions have sales above or below the average? Show as a Bar Chart with Deviation from Average.```
    - ```Which regions have discounts above or below the average? Show as a Bar Chart with Deviation from Average.```
    - ```Simulate future sales by region using a Monte Carlo simulation to estimate confidence intervals. Show as a Line with Confidence Bands using vivid colors.```

## Iwanang Tumatakbo ang Agent App

Iwanang tumatakbo ang agent app dahil gagamitin mo ito sa susunod na lab upang palawakin pa ang agent gamit ang mas maraming tool at kakayahan.

*Isinalin gamit ang GitHub Copilot.*
