## O que Você Aprenderá

Neste laboratório, você habilita capacidades de busca semântica no Agente Azure AI usando o Protocolo de Contexto de Modelo (MCP) e o banco de dados PostgreSQL.

## Introdução

Este laboratório atualiza o Agente Azure AI com busca semântica usando Protocolo de Contexto de Modelo (MCP) e PostgreSQL. Nomes e descrições de produtos foram convertidos em vetores com o modelo de embedding OpenAI (text-embedding-3-small) e armazenados no banco de dados. Isso permite que o agente entenda a intenção do usuário e forneça respostas mais precisas.

## Exercício de Laboratório

Do laboratório anterior você pode fazer perguntas ao agente sobre dados de vendas, mas estava limitado a correspondências exatas. Neste laboratório, você estende as capacidades do agente implementando busca semântica usando o Protocolo de Contexto de Modelo (MCP). Isso permitirá que o agente entenda e responda a consultas que não são correspondências exatas, melhorando sua capacidade de ajudar usuários com perguntas mais complexas.

1. Cole a seguinte pergunta na aba Web Chat em seu navegador:

    ```text
    Como as diferentes lojas performaram com disjuntores 18A?
    ```

    O agente responde: "Não consegui encontrar dados de vendas para disjuntores 18A em nossos registros. 😱 No entanto, aqui estão algumas sugestões para produtos similares que você pode querer explorar." Isso acontece porque o agente depende apenas de consultas correspondentes por palavras-chave e não entende o significado semântico da sua pergunta. O LLM ainda pode fazer sugestões educadas de produtos a partir de qualquer contexto de produto que já possa ter.

## Implementar Busca Semântica

Nesta seção, você implementará busca semântica usando o Protocolo de Contexto de Modelo (MCP) para aprimorar as capacidades do agente.

1. Pressione <kbd>F1</kbd> para **abrir** a Paleta de Comandos do VS Code.
2. Digite **Open File** e selecione **File: Open File...**.
3. **Cole** o seguinte caminho no seletor de arquivos e pressione <kbd>Enter</kbd>:

    ```text
    /workspace/src/python/mcp_server/sales_analysis/sales_analysis.py
    ```

4. Role para baixo até aproximadamente a linha 100 e procure pelo método `semantic_search_products`. Este método é responsável por realizar busca semântica nos dados de vendas. Você notará que o decorador **@mcp.tool()** está comentado. Este decorador é usado para registrar o método como uma ferramenta MCP, permitindo que seja chamado pelo agente.

5. Descomente o decorador `@mcp.tool()` removendo o `#` no início da linha. Isso habilitará a ferramenta de busca semântica.

    ```python
    # @mcp.tool()
    async def semantic_search_products(
        ctx: Context,
        query_description: Annotated[str, Field(
        ...
    ```

6. Em seguida, você precisa habilitar as instruções do Agente para usar a ferramenta de busca semântica. Volte para o arquivo `app.py`.
7. Role para baixo até aproximadamente a linha 30 e encontre a linha `# INSTRUCTIONS_FILE = "instructions/mcp_server_tools_with_semantic_search.txt".
8. Descomente a linha removendo o `#` no início. Isso habilitará o agente a usar a ferramenta de busca semântica.

    ```python
    INSTRUCTIONS_FILE = "instructions/mcp_server_tools_with_semantic_search.txt"
    ```

## Revisar as Instruções do Agente

1. Pressione <kbd>F1</kbd> para abrir a Paleta de Comandos do VS Code.
2. Digite **Open File** e selecione **File: Open File...**.
3. Cole o seguinte caminho no seletor de arquivos e pressione <kbd>Enter</kbd>:

    ```text
    /workspace/src/shared/instructions/mcp_server_tools_with_semantic_search.txt
    ```

4. Revise as instruções no arquivo. Essas instruções instruem o agente a usar a ferramenta de busca semântica para responder perguntas sobre dados de vendas.

## Iniciar a Aplicação do Agente com a Ferramenta de Busca Semântica

1. **Pare** a aplicação atual do agente pressionando <kbd>Shift + F5</kbd>.
2. **Reinicie** a aplicação do agente pressionando <kbd>F5</kbd>. Isso iniciará o agente com as instruções atualizadas e a ferramenta de busca semântica habilitada.
3. Volte para a aba **Web Chat** em seu navegador.
4. Digite a seguinte pergunta no chat:

    ```text
    Como as diferentes lojas performaram com disjuntores 18A?
    ```

    O agente agora entende o significado semântico da pergunta e responde adequadamente com dados de vendas relevantes.

    !!! info "Nota"
        A ferramenta de Busca Semântica MCP funciona da seguinte forma:

        1. A pergunta é convertida em um vetor usando o mesmo modelo de embedding OpenAI (text-embedding-3-small) que as descrições de produtos.
        2. Este vetor é usado para procurar vetores de produtos similares no banco de dados PostgreSQL.
        3. O agente recebe os resultados e os usa para gerar uma resposta.

*Traduzido usando GitHub Copilot e GPT-4o.*
