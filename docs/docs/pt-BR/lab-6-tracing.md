**TBC: Este rótulo fará com que o usuário atualize o arquivo de instruções do agente para remover os emojis chatos que o agente usa em suas respostas.**

## Introdução

O rastreamento ajuda você a entender e depurar o comportamento do seu agente mostrando a sequência de etapas, entradas e saídas durante a execução. No Azure AI Foundry, o rastreamento permite observar como seu agente processa solicitações, chama ferramentas e gera respostas. Você pode usar o portal Azure AI Foundry ou integrar com OpenTelemetry e Application Insights para coletar e analisar dados de rastreamento, tornando mais fácil solucionar problemas e otimizar seu agente.

<!-- ## Exercício de Laboratório

=== "Python"

      1. Abra o arquivo `app.py`.
      2. Altere a variável `AZURE_TELEMETRY_ENABLED` para `True` para habilitar rastreamento:

         ```python
         AZURE_TELEMETRY_ENABLED = True
         ```

        !!! info "Nota"
            Esta configuração habilita telemetria para seu agente. Na função `initialize` em `app.py`, o cliente de telemetria é configurado para enviar dados ao Azure Monitor.

            ```python
             if AZURE_TELEMETRY_ENABLED:
                 configure_azure_monitor(connection_string=await self.project_client.telemetry.get_connection_string())
            ```         

=== "C#"

      tbd -->

## Executar a Aplicação do Agente

1. Pressione <kbd>F5</kbd> para executar a aplicação.
2. Selecione **Preview in Editor** para abrir a aplicação do agente em uma nova aba do editor.

### Iniciar uma Conversa com o Agente

Copie e cole o seguinte prompt na aplicação do agente para iniciar uma conversa:

```plaintext
Escreva um relatório executivo que analise as 5 principais categorias de produtos e compare o desempenho da loja online versus a média das lojas físicas.
```

## Visualizar Rastreamentos

Você pode visualizar os rastreamentos da execução do seu agente no portal Azure AI Foundry ou usando OpenTelemetry. Os rastreamentos mostrarão a sequência de etapas, chamadas de ferramentas e dados trocados durante a execução do agente. Esta informação é crucial para depuração e otimização do desempenho do seu agente.

### Usando o Portal Azure AI Foundry

Para visualizar rastreamentos no portal Azure AI Foundry, siga estes passos:

1. Navegue para o portal **[Azure AI Foundry](https://ai.azure.com/)**.
2. Selecione seu projeto.
3. Selecione a aba **Tracing** no menu à esquerda.
4. Aqui, você pode ver os rastreamentos gerados pelo seu agente.

   ![](media/ai-foundry-tracing.png)

### Aprofundando nos Rastreamentos

1. Você pode precisar clicar no botão **Refresh** para ver os rastreamentos mais recentes, pois os rastreamentos podem levar alguns momentos para aparecer.
2. Selecione o rastreamento chamado `Zava Agent Initialization` para visualizar os detalhes.
   ![](media/ai-foundry-trace-agent-init.png)
3. Selecione o rastreamento `creare_agent Zava DIY Sales Agent` para visualizar os detalhes do processo de criação do agente. Na seção `Input & outputs`, você verá as instruções do Agente.
4. Em seguida, selecione o rastreamento `Zava Agent Chat Request: Write an executive...` para visualizar os detalhes da solicitação de chat. Na seção `Input & outputs`, você verá a entrada do usuário e a resposta do agente.

<!-- https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/continuous-evaluation-agents -->

*Traduzido usando GitHub Copilot e GPT-4o.*
