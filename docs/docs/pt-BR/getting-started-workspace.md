## Abrindo o Workspace de Linguagem

Existem dois workspaces no workshop, um para Python e um para C#. O workspace contém o código-fonte e todos os arquivos necessários para completar os laboratórios para cada linguagem. Escolha o workspace que corresponde à linguagem com a qual você deseja trabalhar.

=== "Python"

    1. Copie o seguinte comando para sua área de transferência:

        ```text
        File: Open Workspace from File...
        ```
    2. Mude para o Visual Studio Code, pressione <kbd>F1</kbd> para abrir a Paleta de Comandos.
    3. Cole o comando na Paleta de Comandos e selecione **Open Workspace from File...**.
    4. Copie e cole o seguinte caminho no seletor de arquivos e pressione <kbd>Enter</kbd>:

        ```text
        /workspace/.vscode/python-workspace.code-workspace
        ```

    ## Estrutura do Projeto

    Certifique-se de se familiarizar com as **pastas** e **arquivos** principais com os quais você trabalhará durante todo o workshop.

    ### A pasta workshop

    - O arquivo **app.py**: O ponto de entrada para a aplicação, contendo sua lógica principal.
  
    Note a variável **INSTRUCTIONS_FILE**—ela define qual arquivo de instruções o agente usa. Você atualizará esta variável em um laboratório posterior.

    - O arquivo **resources.txt**: Contém os recursos usados pela aplicação do agente.
    - O arquivo **.env**: Contém as variáveis de ambiente usadas pela aplicação do agente.

    ### A pasta mcp_server

    - O arquivo **sales_analysis.py**: O Servidor MCP com ferramentas para análise de vendas.

    ### A pasta shared

    - A pasta **instructions**: Contém as instruções passadas para o LLM.

    ![Estrutura da pasta do laboratório](media/project-structure-self-guided-python.png)

=== "C#"

    1. No Visual Studio Code, vá para **File** > **Open Workspace from File**.
    2. Substitua o caminho padrão pelo seguinte:

        ```text
        /workspace/.vscode/csharp-workspace.code-workspace
        ```

    3. Selecione **OK** para abrir o workspace.

    ## Estrutura do Projeto

    Certifique-se de se familiarizar com as **pastas** e **arquivos** principais com os quais você trabalhará durante todo o workshop.

    ### A pasta workshop

    - Os arquivos **Lab1.cs, Lab2.cs, Lab3.cs**: O ponto de entrada para cada laboratório, contendo sua lógica de agente.
    - O arquivo **Program.cs**: O ponto de entrada para a aplicação, contendo sua lógica principal.
    - O arquivo **SalesData.cs**: A lógica de função para executar consultas SQL dinâmicas contra o banco de dados SQLite.

    ### A pasta shared

    - A pasta **files**: Contém os arquivos criados pela aplicação do agente.
    - A pasta **fonts**: Contém as fontes multilíngues usadas pelo Interpretador de Código.
    - A pasta **instructions**: Contém as instruções passadas para o LLM.

    ![Estrutura da pasta do laboratório](media/project-structure-self-guided-csharp.png)

*Traduzido usando GitHub Copilot e GPT-4o.*
