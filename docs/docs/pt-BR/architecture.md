## Arquitetura da Solução

Neste workshop, você criará o Agente de Vendas Zava: um agente conversacional projetado para responder perguntas sobre dados de vendas, gerar gráficos para o negócio de varejo DIY da Zava.

## Componentes da Aplicação do Agente

1. **Serviços Microsoft Azure**

    Este agente é construído nos serviços Microsoft Azure.

      - **Modelo de IA Generativa**: O LLM subjacente que alimenta esta aplicação é o [Azure OpenAI gpt-4o-mini](https://learn.microsoft.com/azure/ai-foundry/openai/concepts/models?tabs=global-standard%2Cstandard-chat-completions#how-do-i-access-the-gpt-4o-and-gpt-4o-mini-models){:target="_blank"} LLM.

      - **Plano de Controle**: A aplicação e seus componentes arquitetônicos são gerenciados e monitorados usando o portal [Azure AI Foundry](https://ai.azure.com){:target="_blank"}, acessível via navegador.

2. **Azure AI Foundry (SDK)**

    O workshop é oferecido em [Python](https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme?view=azure-python-preview&context=%2Fazure%2Fai-services%2Fagents%2Fcontext%2Fcontext){:target="_blank"} usando o SDK Azure AI Foundry. O SDK suporta recursos principais do serviço Azure AI Agents, incluindo [Interpretador de Código](https://learn.microsoft.com/azure/ai-services/agents/how-to/tools/code-interpreter?view=azure-python-preview&tabs=python&pivots=overview){:target="_blank"} e integração com [Protocolo de Contexto de Modelo (MCP)](https://modelcontextprotocol.io/){:target="_blank"}.

3. **Banco de Dados**

    A aplicação é alimentada pelo Banco de Dados de Vendas Zava, um [servidor flexível Azure Database for PostgreSQL](https://www.postgresql.org/){:target="_blank"} com extensão pgvector contendo dados abrangentes de vendas para as operações de varejo DIY da Zava.

    O banco de dados suporta consultas complexas para dados de vendas, inventário e clientes. A Segurança em Nível de Linha (RLS) garante que agentes acessem apenas suas lojas atribuídas.

4. **Servidor MCP**

    O servidor do Protocolo de Contexto de Modelo (MCP) é um serviço Python personalizado que atua como uma ponte entre o agente e o banco de dados PostgreSQL. Ele gerencia:

     - **Descoberta de Esquema de Banco de Dados**: Recupera automaticamente esquemas de banco de dados para ajudar o agente a entender os dados disponíveis.
     - **Geração de Consultas**: Transforma solicitações em linguagem natural em consultas SQL.
     - **Execução de Ferramentas**: Executa consultas SQL e retorna resultados em um formato que o agente pode usar.
     - **Serviços de Tempo**: Fornece dados relacionados ao tempo para gerar relatórios sensíveis ao tempo.

## Expandindo a Solução do Workshop

O workshop é facilmente adaptável para casos de uso como suporte ao cliente atualizando o banco de dados e personalizando instruções do Serviço de Agente Foundry.

## Melhores Práticas Demonstradas na Aplicação

A aplicação também demonstra algumas melhores práticas para eficiência e experiência do usuário.

- **APIs Assíncronas**:
  Na amostra do workshop, tanto o Serviço de Agente Foundry quanto o PostgreSQL usam APIs assíncronas, otimizando eficiência de recursos e escalabilidade. Esta escolha de design torna-se especialmente vantajosa ao implantar a aplicação com frameworks web assíncronos como FastAPI, ASP.NET ou Streamlit.

- **Streaming de Tokens**:
  O streaming de tokens é implementado para melhorar a experiência do usuário reduzindo tempos de resposta percebidos para a aplicação de agente alimentada por LLM.

- **Observabilidade**:
  A aplicação inclui [rastreamento](https://learn.microsoft.com/azure/ai-foundry/agents/concepts/tracing){:target="_blank"} e [métricas](https://learn.microsoft.com/azure/ai-foundry/agents/how-to/metrics){:target="_blank"} integrados para monitorar desempenho do agente, padrões de uso e latência. Isso permite identificar problemas e otimizar o agente ao longo do tempo.

*Traduzido usando GitHub Copilot e GPT-4o.*
