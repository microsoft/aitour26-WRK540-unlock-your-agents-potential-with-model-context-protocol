## O que Você Aprenderá

Neste laboratório, você revisará e atualizará as instruções do agente para incluir uma regra sobre o ano fiscal começando em 1º de julho. Isso é importante para o agente interpretar e analisar corretamente os dados de vendas.

## Introdução

O propósito das instruções do agente é definir o comportamento do agente, incluindo como ele interage com usuários, quais ferramentas pode usar e como deve responder a diferentes tipos de consultas. Neste laboratório, você revisará as instruções existentes do agente e fará uma pequena atualização para garantir que o agente interprete corretamente o ano fiscal.

## Exercício de Laboratório

### Abrir as Instruções do Agente

1. No Explorador do VS Code, navegue até a pasta `shared/instructions`.
2. **Abra** o arquivo `mcp_server_tools_with_code_interpreter.txt`.

### Revisar as Instruções do Agente

Revise como as instruções definem o comportamento da aplicação do agente:

!!! tip "No VS Code, pressione Alt + Z (Windows/Linux) ou Option + Z (Mac) para habilitar o modo de quebra de linha, tornando as instruções mais fáceis de ler."

- **Papel Principal:** Agente de vendas para Zava (varejista DIY de WA) com tom profissional e amigável usando emojis e sem suposições ou conteúdo não verificado.
- **Regras de Banco de Dados:** Sempre obter esquemas primeiro (get_multiple_table_schemas()) com LIMIT 20 obrigatório em todas as consultas SELECT usando nomes exatos de tabela/coluna.
- **Visualizações:** Criar gráficos APENAS quando explicitamente solicitado usando gatilhos como "gráfico", "chart", "visualizar" ou "mostrar como [tipo]" em formato PNG baixado da sandbox sem caminhos de imagem markdown.
- **Respostas:** Padrão para tabelas Markdown com suporte multilíngue e CSV disponível mediante solicitação.
- **Segurança:** Permanecer no escopo apenas dos dados de vendas Zava com respostas exatas para consultas fora do escopo/pouco claras e redirecionar usuários hostis para TI.
- **Restrições Principais:** Nenhum dado inventado usando ferramentas apenas com limite de 20 linhas e imagens PNG sempre.

### Atualizar as Instruções do Agente

Copie o texto abaixo e cole diretamente após a regra sobre não gerar conteúdo não verificado ou fazer suposições:

!!! tip "Clique no ícone de cópia à direita para copiar o texto para a área de transferência."

```markdown
- O ano fiscal para Zava começa em 1º de janeiro.
```

As instruções atualizadas devem ficar assim:

```markdown
- **Não gere conteúdo não verificado** ou faça suposições.
- O ano fiscal para Zava começa em 1º de janeiro.
```

*Traduzido usando GitHub Copilot e GPT-4o.*
