# Security Concerns

This workshop application is designed for education and adaptation, and is not intended for production use out-of-the-box. Nonetheless, it does demonstrate some best practices for security.

## Malicious SQL Attacks

A common concern with LLM-generated SQL is the risk of injection or harmful queries. These risks are mitigated by limiting database permissions.

This app uses PostgreSQL with restricted privileges for the agent and runs in a secure environment. Row-Level Security (RLS) ensures agents access only data for their assigned stores.

In enterprise settings, data is typically extracted into a read-only database or warehouse with a simplified schema. This ensures secure, performant, and read-only access for the agent.

## Sandboxing

This uses the [Azure AI Agents Service Code Interpreter](https://learn.microsoft.com/azure/ai-services/agents/how-to/tools/code-interpreter?view=azure-python-preview&tabs=python&pivots=overview){:target="_blank"} to create and run code on demand. The code runs in a sandboxed execution environment to prevent the code taking actions that are beyond the scope of the agent.
