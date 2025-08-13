## What You'll Learn

In this lab, you review and update the agent instructions to include a rule about the financial year starting on July 1. This is important for the agent to correctly interpret and analyze sales data.

## Introduction

The purpose of agent instructions is to define the agent's behavior, including how it interacts with users, what tools it can use, and how it should respond to different types of queries. In this lab, you will review the existing agent instructions and make a small update to ensure the agent correctly interprets the financial year.

## Lab Exercise

### Open the Agent Instructions

1. From the VS Code Explorer, navigate to the `shared/instructions` folder.
2. **Open** the `mcp_server_tools_with_code_interpreter.txt` file.

### Review the Agent Instructions

Review how the instructions define the agent app’s behavior:

!!! tip "In VS Code, press Alt + Z (Windows/Linux) or Option + Z (Mac) to enable word wrap mode, making the instructions easier to read."

- **Core Role:** Sales agent for Zava (WA DIY retailer) with professional, friendly tone using emojis and no assumptions or unverified content.
- **Database Rules:** Always get schemas first (get_multiple_table_schemas()) with mandatory LIMIT 20 on all SELECT queries using exact table/column names.
- **Visualizations:** Create charts ONLY when explicitly requested using triggers like "chart", "graph", "visualize", or "show as [type]" in PNG format downloaded from sandbox with no markdown image paths.
- **Responses:** Default to Markdown tables with multi-language support and CSV available on request.
- **Safety:** Stay in scope of Zava sales data only with exact responses for out-of-scope/unclear queries and redirect hostile users to IT.
- **Key Constraints:** No made-up data using tools only with 20-row limit and PNG images always.

### Update the Agent Instructions

Copy the text below and paste directly after the rule about not generating unverified content or making assumptions:

!!! tip "Click the copy icon to the right to copy the text to the clipboard."

```markdown
- **Financial year (FY) starts Jan 1** (Q1=Jan–Mar, Q2=Apr–Jun, Q3=Jul–Sep, Q4=Oct–Dec).
```

The updated instructions should look like this:

```markdown
- Use **only** verified tool outputs; **never** invent data or assumptions.
- **Financial year (FY) starts Jan 1** (Q1=Jan–Mar, Q2=Apr–Jun, Q3=Jul–Sep, Q4=Oct–Dec).
```
