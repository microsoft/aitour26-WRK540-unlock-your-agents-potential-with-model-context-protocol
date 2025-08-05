## O que Você Aprenderá

Neste laboratório, você habilitará o Interpretador de Código para analisar dados de vendas e criar gráficos usando linguagem natural.

## Introdução

Neste laboratório, você estenderá o Agente Azure AI com duas ferramentas:

- **Interpretador de Código:** Permite que o agente gere e execute código Python para análise e visualização de dados.
- **Ferramentas do Servidor MCP:** Permitem que o agente acesse fontes de dados externas usando Ferramentas MCP, em nosso caso dados em um banco de dados PostgreSQL.

## Exercício de Laboratório

### Habilitar o Interpretador de Código

Neste laboratório, você habilitará o Interpretador de Código para executar código Python gerado pelo LLM para analisar os dados de vendas de varejo da Zava.

=== "Python"

    1. **Abra** o `app.py`.
    2. **Descomente** a linha que adiciona a ferramenta Interpretador de Código ao conjunto de ferramentas do agente no método `_setup_agent_tools` da classe `AgentManager`. Esta linha está atualmente comentada com um `#` no início.:

        ```python
        # code_interpreter = CodeInterpreterTool()
        # self.toolset.add(code_interpreter)
        ```

    3. **Revise** o código no arquivo `app.py`. Você notará que as ferramentas Interpretador de Código e Servidor MCP são adicionadas ao conjunto de ferramentas do agente no método `_setup_agent_tools` da classe `AgentManager`.

        ```python

        Após descomentar, seu código deve ficar assim:

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

## Iniciar a Aplicação do Agente

1. Copie o texto abaixo para a área de transferência:

    ```text
    Debug: Select and Start Debugging
    ```

2. Pressione <kbd>F1</kbd> para abrir a Paleta de Comandos do VS Code.
3. Cole o texto na Paleta de Comandos e selecione **Debug: Select and Start Debugging**.
4. Selecione **🔁🤖Debug Compound: Agent and MCP (stdio)** da lista. Isso iniciará a aplicação do agente e o cliente de chat web.

## Abrir o Cliente de Chat Web do Agente

1. Copie o texto abaixo para a área de transferência:

    ```text
    Open Port in Browser
    ```

2. Pressione <kbd>F1</kbd> para abrir a Paleta de Comandos do VS Code.
3. Cole o texto na Paleta de Comandos e selecione **Open Port in Browser**.
4. Selecione **8005** da lista. Isso abrirá o cliente de chat web do agente em seu navegador.

### Iniciar uma Conversa com o Agente

Do cliente de chat web, você pode iniciar uma conversa com o agente. O agente é projetado para responder perguntas sobre os dados de vendas da Zava e gerar visualizações usando o Interpretador de Código.

1. Análise de vendas de produtos. Copie e cole a seguinte pergunta no chat:

    ```text
    Mostre os 10 principais produtos por receita por loja para o último trimestre
    ```

    Após um momento, o agente responderá com uma tabela mostrando os 10 principais produtos por receita para cada loja.

    !!! info
        O agente usa o LLM chama três ferramentas do Servidor MCP para buscar os dados e exibi-los em uma tabela:

           1. **get_current_utc_date()**: Obtém a data e hora atuais para que o agente possa determinar o último trimestre relativo à data atual.
           2. **get_multiple_table_schemas()**: Obtém os esquemas das tabelas no banco de dados necessários pelo LLM para gerar SQL válido.
           3. **execute_sales_query**: Executa uma consulta SQL para buscar os 10 principais produtos por receita do último trimestre do banco de dados PostgreSQL.

2. Gerar um gráfico de pizza. Copie e cole a seguinte pergunta no chat:

    ```text
    Mostre vendas por loja como gráfico de pizza para este ano fiscal
    ```

    O agente responderá com um gráfico de pizza mostrando a distribuição de vendas por loja para o ano fiscal atual.

    !!! info
        Isso pode parecer mágica, então o que está acontecendo nos bastidores para fazer tudo funcionar?

        O Serviço de Agente Foundry orquestra as seguintes etapas:

        1. Como a pergunta anterior, o agente determina se tem os esquemas de tabela necessários para a consulta. Se não, usa as ferramentas **get_multiple_table_schemas()** para obter a data atual e o esquema do banco de dados.
        2. O agente então usa a ferramenta **execute_sales_query** para buscar as vendas
        3. Usando os dados retornados, o LLM escreve código Python para criar um Gráfico de Pizza.
        4. Finalmente, o Interpretador de Código executa o código Python para gerar o gráfico.

3. Continue fazendo perguntas sobre os dados de vendas da Zava para ver o Interpretador de Código em ação. Aqui estão algumas perguntas de acompanhamento que você pode querer tentar:

    - ```Determine quais produtos ou categorias impulsionam as vendas. Mostre como Gráfico de Barras.```
    - ```Qual seria o impacto de um evento de choque (por exemplo, queda de 20% nas vendas em uma região) na distribuição global de vendas? Mostre como Gráfico de Barras Agrupadas.```
        - Acompanhe com ```E se o evento de choque fosse de 50%?```
    - ```Quais regiões têm vendas acima ou abaixo da média? Mostre como Gráfico de Barras com Desvio da Média.```
    - ```Quais regiões têm descontos acima ou abaixo da média? Mostre como Gráfico de Barras com Desvio da Média.```
    - ```Simule vendas futuras por região usando uma simulação Monte Carlo para estimar intervalos de confiança. Mostre como Linha com Bandas de Confiança usando cores vívidas.```

<!-- ## Stop the Agent App

1. Switch back to the VS Code editor.
1. Press <kbd>Shift + F5</kbd> to stop the agent app. -->

## Deixar a Aplicação do Agente Executando

Deixe a aplicação do agente executando pois você a usará no próximo laboratório para estender o agente com mais ferramentas e capacidades.

*Traduzido usando GitHub Copilot e GPT-4o.*
