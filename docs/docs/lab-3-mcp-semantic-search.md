## What You'll Learn

In this lab, you'll learn how to:

Enable semantic search capabilities in the Azure AI Agent using the Model Context Protocol (MCP) and the PostgreSQL database.

## Introduction

In this lab, you’ll add semantic search to the Azure AI Agent using the Model Context Protocol (MCP) and a PostgreSQL database. This upgrade allows the agent to understand the meaning behind user queries, not just match keywords, making its responses more accurate and helpful. Product names and descriptions have been converted into numerical vectors to enable this capability.

Semantic search helps the agent interpret user intent, while vectorization transforms text into numbers that machine learning models can process.

## Lab Exercise

From the previous lab you were able to ask the agent questions about sales data, but it was limited to exact matches. In this lab, you will extend the agent's capabilities by implementing semantic search using the Model Context Protocol (MCP). This will allow the agent to understand and respond to queries that are not exact matches, improving its ability to assist users with more complex questions.

1. Switch back to the Web Chat tab in your browser to continue.
1. Enter the following question in the chat:

    ```text
    How did different stores perform with 18A breakers?
    ```

    The agent will reply: “I couldn’t find any sales data for 18A breakers in our records. 😱 However, here are some suggestions for similar products you might want to explore.” This happens because the agent currently only matches queries by keywords and does not understand the semantic meaning of your question. The LLM may still make educated product suggestions.

## Implement Semantic Search

In this section, you will implement semantic search using the Model Context Protocol (MCP) to enhance the agent's capabilities.

1. Press <kbd>F1</kbd> to open the VS Code Command Palette.
2. Type **Open File** and select **File: Open File...**.
3. Paste the following path into the file picker and press <kbd>Enter</kbd>:

    ```text
    /workspace/src/python/mcp_server/sales_analysis/sales_analysis.py
    ```

4. Scroll down to the `semantic_search_products` method in the `SalesAnalysis` class. This method is responsible for performing semantic search on the sales data. You'll notice the @mcp.tool() decorator is commented out. This decorator is used to register the method as an MCP tool, allowing it to be called by the agent.

5. Uncomment the `@mcp.tool()` decorator by removing the `#` at the beginning of the line. This will enable the semantic search tool.

    ```python
    # @mcp.tool()
    async def semantic_search_products(
        ctx: Context,
        query_description: Annotated[str, Field(
        ...
    ```

6. Next, you need to enable the Agent instructions to use the semantic search tool. Switch back to the `app.py` file.
7. Scroll down to approximately line 30 and find the line `# INSTRUCTIONS_FILE = "instructions/mcp_server_tools_with_semantic_search.txt". Since this line is commented out, the agent won't use the semantic search tool.
8. Uncomment the line by removing the `#` at the beginning. This will enable the agent to use the semantic search tool.

    ```python
    INSTRUCTIONS_FILE = "instructions/mcp_server_tools_with_semantic_search.txt"
    ```

9. Save the file by pressing <kbd>Ctrl + S</kbd> (Windows/Linux) or <kbd>Cmd + S</kbd> (Mac).

## Review the Agent Instructions

1. Press <kbd>F1</kbd> to open the VS Code Command Palette.
2. Type **Open File** and select **File: Open File...**.
3. Paste the following path into the file picker and press <kbd>Enter</kbd>:

    ```text
    /workspace/src/shared/instructions/mcp_server_tools_with_semantic_search.txt
    ```

4. Review the instructions in the file. You'll see that the agent is now instructed to use the semantic search tool to answer questions about sales data.

## Start the Agent App with the Semantic Search Tool

1. From the VS Code editor, press <kbd>Shift + F5</kbd> to stop the agent app.
2. Restart the agent app by pressing <kbd>F5</kbd>. This will start the agent with the updated instructions and the semantic search tool enabled.
3. Switch back to the Web Chat tab in your browser.
4. Enter the following question in the chat:

    ```text
    How did different stores perform with 18A breakers?
    ```

    The agent should now be able to understand the semantic meaning of the question and respond accordingly with relevant sales data.

    !!! info "Note"
        How does this work? The MCP Semantic Search tool works as follows:

        1. The question is converted into a vector using the same OpenAI embedding model (text-embedding-3-small) as the product descriptions.
        2. This vector is used to search for similar product vectors in the PostgreSQL database.
        3. The agent receives the results and uses them to generate a response.
