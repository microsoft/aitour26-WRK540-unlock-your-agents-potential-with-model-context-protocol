## आप क्या सीखेंगे

इस लैब में आप Code Interpreter सक्षम करेंगे ताकि बिक्री डेटा विश्लेषण और चार्ट प्राकृतिक भाषा से बन सकें।

## परिचय

आप Azure AI एजेंट में दो टूल जोड़ेंगे:

- **Code Interpreter:** LLM द्वारा जनित Python कोड चलाने हेतु।
- **MCP Server tools:** बाहरी डेटा (हमारे केस में PostgreSQL) तक पहुँच।

## लैब अभ्यास

### Code Interpreter सक्षम करें

=== "Python"

    1. `app.py` खोलें।
    2. `AgentManager` क्लास की `_setup_agent_tools` विधि में Code Interpreter जोड़ने वाली लाइन को अनकमेंट करें:

        ```python
        # code_interpreter = CodeInterpreterTool()
        # self.toolset.add(code_interpreter)
        ```

    3. अनकमेंट करने के बाद उदाहरण:

        ```python
        class AgentManager:
            async def _setup_agent_tools(self) -> None:
                code_interpreter = CodeInterpreterTool()
                self.toolset.add(code_interpreter)
                print("Setting up Agent tools...")
        ```

=== "C#"

    TBD

## एजेंट ऐप शुरू करें

1. नीचे का पाठ कॉपी करें:

    ```text
    Debug: Select and Start Debugging
    ```

2. <kbd>F1</kbd> दबाएँ।
3. पेस्ट करें और चुनें।
4. **🔁🤖Debug Compound: Agent and MCP (stdio)** चुनें।

## एजेंट वेब चैट खोलें

1. नीचे कॉपी करें:

    ```text
    Open Port in Browser
    ```

2. <kbd>F1</kbd>।
3. पेस्ट करें चयन करें **Open Port in Browser**।
4. **8005** चुनें।

### बातचीत शुरू करें

पहला प्रश्न:

```text
Show the top 10 products by revenue by store for the last quarter
```

!!! info
        एजेंट तीन MCP टूल कॉल करता है:

           1. **get_current_utc_date()**
           2. **get_multiple_table_schemas()**
           3. **execute_sales_query**

दूसरा प्रश्न (Pie Chart):

```text
Show sales by store as a pie chart for this financial year
```

!!! info
        चरण: स्कीमा जाँच, क्वेरी, Python कोड जनरेशन, Code Interpreter निष्पादन।

अधिक प्रश्न सुझाए:

- ```Determine which products or categories drive sales. Show as a Bar Chart.```
- ```What would be the impact of a shock event (e.g., 20% sales drop in one region) on global sales distribution? Show as a Grouped Bar Chart.```
- ```Which regions have sales above or below the average? Show as a Bar Chart with Deviation from Average.```
- ```Which regions have discounts above or below the average? Show as a Bar Chart with Deviation from Average.```
- ```Simulate future sales by region using a Monte Carlo simulation...```

## एजेंट चालू रखें

अगली लैब के लिए एजेंट चलते रहने दें।

*GitHub Copilot द्वारा अनुवादित.*
