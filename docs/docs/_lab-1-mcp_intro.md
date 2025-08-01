## What You'll Learn

In this lab, you will:

- Configure and enable MCP tools for an AI agent
- Review and extend agent instructions for real-world scenarios
- Practice asking the agent questions about sales data, products, and inventory

!!! info "Prerequisites"
    This lab assumes you have completed Lab 0 and have the MCP server running in the background.

## Introduction

The Model Context Protocol (MCP) is a standard that connects Large Language Models (LLMs) with external tools and data sources, such as databases and APIs, through a consistent interface. This enables smarter, more extensible AI applications.

### Lab Exercise

!!! info "Prerequisites"
    Before starting this lab, make sure you have completed Lab 0 and have the MCP server running.

=== "Python"

    #### Configure the Agent

      1. Open the `app.py` and enable the agent MCP tools by uncommenting the following lines:

         Uncomment the following lines by removing the "# " characters

         ```python
         # INSTRUCTIONS_FILE = "instructions/mcp_server_tools.txt"

         # toolset.add(functions)
         ```

        !!! warning "Ensure you remove the space after the `#` character"
            The lines to be uncommented are not adjacent. When removing the `#` character, ensure you also delete the space that follows it.

      1. Review the code in the `app.py` file.

         After uncommenting, your code should look like this:

         ```python
         INSTRUCTIONS_FILE = "instructions/mcp_server_tools.txt"

         async def add_agent_tools() -> None:
            """Add tools for the agent."""
            global mcp_tools

            # Fetch and build MCP tools dynamically
            mcp_tools = await fetch_and_build_mcp_tools()

            # Add the MCP tools to the toolset
            toolset.add(mcp_tools)

            # Add the code interpreter tool
            # code_interpreter = CodeInterpreterTool()
            # toolset.add(code_interpreter)
         ```

=== "C#"

      TBD

### Review the Instructions

 1. Open the **shared/instructions/mcp_server_tools.txt** file.

    !!! tip "In VS Code, press Alt + Z (Windows/Linux) or Option + Z (Mac) to enable word wrap mode, making the instructions easier to read."

 2. Review how the instructions define the agent app’s behavior:

     - **Role definition**: The agent assists Zava users with sales data inquiries in a polite, professional, and friendly manner.
     - **Context**: Zava is an online retailer specializing in camping and sports gear.
     - **Tool description – “Sales Data Assistance”**:
         - Enables the agent to generate and run SQL queries.
         - Includes database schema details for query building.
         - Limits results to aggregated data with a maximum of 30 rows.
         - Formats output as Markdown tables.
     - **Response guidance**: Emphasizes actionable, relevant replies.
     - **User support tips**: Provides suggestions for assisting users.
     - **Safety and conduct**: Covers how to handle unclear, out-of-scope, or malicious queries.

     During the workshop, we’ll extend these instructions by introducing new tools to enhance the agent’s capabilities.

### Start a Conversation with the Agent

The agent supports rich streaming conversations with real-time responses. Start asking questions about Zava sales data.

1. **Help**

      Here is an example of the LLM response to the **help** query:

      Certainly! I’m here to assist with Zava sales data and product information. Could you clarify what you need help with? Here are some examples of questions you can ask:

      - "What are the sales by store?"
      - "What was last quarter's revenue?"
      - "What are the total shipping costs by store?"
      - "Can I download the sales data for a specific product?"

      Feel free to ask about sales, products, or inventory, and I'll do my best to assist!

    !!! tip ""
         The LLM will provide a list of starter questions that were defined in the instructions file. Try asking for help in your language, for example `help in Hindi`, `help in Italian`, or `help in Korean`.

2. **Example Queries to Try**:

      - **Sales Performance**: "Show me revenue by product category for 2024"
      - **Regional Analysis**: "Which stores performed best last quarter?"
      - **Customer Insights**: "Who are our top 10 customers by order value?"
      - **Product Search**: "Find products similar to camping equipment"
      - **Trend Analysis**: "Show me seasonal sales patterns"
      - **Inventory Reports**: "What's our current stock level by store?"

3. **Advanced Features**:

      - **Multi-language**: Ask questions in different languages for localized responses
      - **Data Export**: Request data in CSV format (presented as markdown tables)
      - **Complex Queries**: The agent can join multiple tables and perform sophisticated analysis
