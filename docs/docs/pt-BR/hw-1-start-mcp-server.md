## O que Você Aprenderá

Neste laboratório, você irá:

- Usar DevTunnel para tornar seu servidor MCP local acessível aos serviços de agente baseados em nuvem
- Configurar seu ambiente para experimentação prática com o Protocolo de Contexto de Modelo

## Introdução

O servidor do Protocolo de Contexto de Modelo (MCP) é um componente crucial que gerencia a comunicação entre Modelos de Linguagem Grande (LLMs) e ferramentas e fontes de dados externas. Você executará o servidor MCP em sua máquina local, mas o Serviço de Agente Azure AI Foundry requer acesso à internet para se conectar a ele. Para tornar seu servidor MCP local acessível pela internet, você usará um DevTunnel. Isso permite que o Serviço de Agente se comunique com seu servidor MCP como se estivesse rodando como um serviço no Azure.

## Opções de interface para MCP

O MCP suporta duas interfaces principais para conectar LLMs com ferramentas:

- **Transporte HTTP Streamable**: Para APIs e serviços baseados na web.
- **Transporte Stdio**: Para scripts locais e ferramentas de linha de comando.

Este laboratório usa a interface de transporte HTTP Streamable para integrar com o Serviço de Agente Azure AI Foundry.

!!! note
    Normalmente, você implantaria o servidor MCP em um ambiente de produção, mas para este workshop, você o executará localmente em seu ambiente de desenvolvimento. Isso permite testar e interagir com as ferramentas MCP sem precisar de uma implantação completa.

### Iniciar um DevTunnel para o Servidor MCP

1. Em um novo terminal, autentique o DevTunnel. Será solicitado que você faça login com sua conta Azure, use a mesma conta que usou para fazer login no Serviço de Agente Azure AI Foundry ou Portal Azure. Execute o seguinte comando:

    ```bash
    devtunnel login
    ```

1. Em seguida, no terminal onde o servidor MCP está executando, inicie um DevTunnel executando:

    ```bash
    devtunnel host -p 8000 --allow-anonymous
    ```

    Isso produzirá uma URL que você precisará para o agente se conectar ao servidor MCP. A saída será similar a:

    ```text
    Hosting port: 8000
    Connect via browser: https://<tunnel-id>-8000.aue.devtunnels.ms
    Inspect network activity: https://<tunnel-id>-8000-inspect.aue.devtunnels.ms
    ```

## Atualizar a Variável de Ambiente DevTunnel

1. Copie a URL **Connect via browser** para a área de transferência - você precisará dela no próximo laboratório para configurar o agente.
2. Abra o arquivo `.env` na pasta workshop.
3. Atualize a variável `DEV_TUNNEL_URL` com a URL copiada.

    ```text
    DEV_TUNNEL_URL=https://<tunnel-id>-8000.aue.devtunnels.ms
    ```

## Iniciar a Aplicação do Agente

1. Copie o texto abaixo para a área de transferência:

    ```text
    Debug: Select and Start Debugging
    ```

2. Pressione <kbd>F1</kbd> para abrir a Paleta de Comandos do VS Code.
3. Cole o texto na Paleta de Comandos e selecione **Debug: Select and Start Debugging**.
4. Selecione **🌎🤖Debug Compound: Agent and MCP (http)** da lista. Isso iniciará a aplicação do agente e o cliente de chat web.

## Iniciar uma conversa com o Agente

Mude para a aba **Web Chat** em seu navegador. Você deve ver a aplicação do agente executando e pronta para aceitar perguntas.

### Depuração com DevTunnel

Você pode usar o DevTunnel para depurar o servidor MCP e a aplicação do agente. Isso permite inspecionar a atividade de rede e solucionar problemas em tempo real.

1. Selecione a URL **Inspect network activity** da saída do DevTunnel.
2. Isso abrirá uma nova aba em seu navegador onde você pode ver a atividade de rede do servidor MCP e da aplicação do agente.
3. Você pode usar isso para depurar quaisquer problemas que surjam durante o workshop.

Você também pode definir pontos de interrupção no código do servidor MCP e no código da aplicação do agente para depurar problemas específicos. Para fazer isso:

1. Abra o arquivo `sales_analysis.py` na pasta `mcp_server`.
2. Defina um ponto de interrupção clicando na margem ao lado do número da linha onde você deseja pausar a execução.
3. Quando a execução atingir o ponto de interrupção, você pode inspecionar variáveis, percorrer o código e avaliar expressões no Console de Depuração.

*Traduzido usando GitHub Copilot e GPT-4o.*
