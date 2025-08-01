## What You'll Learn

In this lab, you will:

- Enable the MCP time service in the MCP server
- Understand how to register new tools using the @mcp.tool() decorator
- Configure the agent to handle time-related queries
- Use natural language to ask time-based questions about sales data
- Explore how the LLM uses current time context to interpret relative date queries

## Introduction

In this lab, we will extend the MCP server to include a time service. This service will allow us to retrieve the current time for use in our Sales Assistant application. For example, the LLM can use the services to determine the current time and respond to user queries that are time related, such as "what were the sales last week?" or "what were last quarters sales?".

The time service will be implemented as a new tool in the MCP server, which can be called by the LLM to get the current time.

## Lab Exercise

Enable the MCP time service by uncommenting the `get_current_utc_date` function in the `mcp_server_sales_analysis.py` file. This function will return the current UTC date and time in ISO format, which can be used by the LLM to answer time-related queries.

=== "Python"

    1. Open the `mcp_server_sales_analysis.py` file in the `src/python/mcp_server` directory.
    2. Uncomment the **@mcp.tool()** decorator for the `get_current_utc_date` function. This decorator registers the function as an MCP tool that can be called by the LLM. After uncommenting, your code should look like this:

        ```python
        @mcp.tool()
        async def get_current_utc_date() -> str:
            """Get the current UTC date and time in ISO format.

            Returns the current date and time in UTC timezone, useful for date-based queries,
            filtering recent data, or understanding the current context for time-sensitive analysis.

            Returns:
                Current UTC date and time in ISO format (YYYY-MM-DDTHH:MM:SS.fffffZ)
            """
            try:
                current_utc = datetime.now(timezone.utc)
                return f"Current UTC Date/Time: {current_utc.isoformat()}"
            except Exception as e:
                return f"Error retrieving current UTC date: {e!s}"
        ```

    3. Review the function's docstring to understand its purpose and how it can be used.
    4. Save the change to the file

=== "C#"

    tbd

## Run the Agent App

1. Press <kbd>F5</kbd> to run the app.
2. Select **Preview in Editor** to open the agent app in a new editor tab.

### Start a Conversation with the Agent

Copy and paste the following prompt into the agent app to start a conversation:

```plaintext
what were the sales last week?
```
