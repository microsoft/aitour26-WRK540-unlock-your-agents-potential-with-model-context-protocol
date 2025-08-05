## Projeto Azure AI Foundry

## Modelos necessários para Zava DIY

## Geração de Dados Sintéticos para Zava DIY

Zava DIY é uma ferramenta projetada para ajudar desenvolvedores a criar dados sintéticos para fins de teste e desenvolvimento. Permite aos usuários gerar conjuntos de dados realistas que podem ser usados em várias aplicações, garantindo que os dados atendam requisitos específicos sem comprometer a privacidade ou segurança.

O banco de dados inclui:

- **8 lojas** em todo o Estado de Washington, cada uma com inventário único e dados de vendas
- **50.000+ registros de clientes** em todo o Estado de Washington e online
- **400+ produtos DIY** incluindo ferramentas, equipamentos para atividades ao ar livre e suprimentos para melhoria residencial
- **400+ imagens de produtos** vinculadas ao banco de dados para buscas baseadas em imagem
- **200.000+ transações de pedidos** com histórico detalhado de vendas
- **3.000+ itens de inventário** em múltiplas lojas
- **Embeddings de imagem** para imagens de produtos permitindo buscas de similaridade alimentadas por IA (codificadas usando [openai/clip-vit-base-patch32](https://huggingface.co/openai/clip-vit-base-patch32/blob/main/README.md){:target="_blank"})
- **Embeddings de texto** para descrições de produtos aprimorando as capacidades de busca e recomendação [openai/text-embedding-3-small](https://ai.azure.com/catalog/models/text-embedding-3-small){:target="_blank"}

O banco de dados suporta consultas complexas e análises, possibilitando acesso eficiente a dados de vendas, inventário e clientes. A Segurança em Nível de Linha (RLS) do PostgreSQL restringe agentes apenas aos dados de suas lojas atribuídas, garantindo segurança e privacidade.

*Traduzido usando GitHub Copilot e GPT-4o.*
