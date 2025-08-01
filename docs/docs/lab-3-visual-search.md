## Introduction

In this lab, you will explore Visual Search using [Azure Database for PostgreSQL flexible server](https://learn.microsoft.com/en-us/azure/postgresql/){:target="_blank"} with the [PGVECTOR extension](https://learn.microsoft.com/azure/postgresql/flexible-server/how-to-use-pgvector). Zava's PostgreSQL database includes a `products_embeddings` table, which stores image vectors for all products Zava sells. These vectors allow us to perform image similarity searches directly in the database, enabling customers to find products by providing an image rather than keywords.

By leveraging PGVECTOR, you can efficiently compare image vectors and retrieve visually similar products. This capability is exposed to the AI agent through the MCP Server, allowing seamless integration of image-based product search into Zava's customer experience.

## Lab Exercise

=== "Python"

    1. Open the `product_search.py` file.

    2. Define a new instructions file for our agent and add the visual search tool in the agent's toolset. **Uncomment** the following lines by removing the **"# "** characters.

        ```python
        # INSTRUCTIONS_FILE = "instructions/mcp_server_tools_with_visual_search.txt"

        # visual_search_tool = VisualSearchTool()
        # toolset.add(visual_search_tool)
        ```

        !!! warning
            The lines to be uncommented are not adjacent. When removing the `#` character, ensure you also delete the space that follows it.

    3. Review the code in the `app.py` file.

        After uncommenting, your code should look like this:

        ```python
        INSTRUCTIONS_FILE = "instructions/mcp_server_tools.txt"
        INSTRUCTIONS_FILE = "instructions/mcp_server_tools_with_visual_search.txt"

        async def add_agent_tools() -> None:
            """Add tools for the agent."""
            global mcp_tools

            # Fetch and build MCP tools dynamically
            mcp_tools = await fetch_and_build_mcp_tools()

            # Add the MCP tools to the toolset
            toolset.add(mcp_tools)

            # Add the visual search tool
            visual_search_tool = VisualSearchTool()
            toolset.add(visual_search_tool)
        ```

=== "C#"
    TBD

## Run the Agent App

1. Press <kbd>F5</kbd> to run the app.
2. In the terminal, the app will start, and the agent app will prompt you to  **Select an image**.

### Start a Conversation with the Agent

Try these questions:

1. **Select an image**: Click the "Select an image" button in the terminal to choose an image file from your local machine. The agent will then perform a visual search using the selected image.
