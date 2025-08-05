Esta aplicação de workshop é projetada para educação e adaptação, e não é destinada para uso em produção fora da caixa. No entanto, ela demonstra algumas melhores práticas para segurança.

## Ataques SQL Maliciosos

Uma preocupação comum com SQL gerado por LLM é o risco de injeção ou consultas prejudiciais. Esses riscos são mitigados limitando permissões de banco de dados.

Esta aplicação usa PostgreSQL com privilégios restritos para o agente e executa em um ambiente seguro. A Segurança em Nível de Linha (RLS) garante que agentes acessem apenas dados de suas lojas atribuídas.

Em configurações empresariais, dados são tipicamente extraídos para um banco de dados ou warehouse somente leitura com esquema simplificado. Isso garante acesso seguro, performático e somente leitura para o agente.

## Sandboxing

Isso usa o [Interpretador de Código do Serviço de Agentes Azure AI](https://learn.microsoft.com/azure/ai-services/agents/how-to/tools/code-interpreter?view=azure-python-preview&tabs=python&pivots=overview){:target="_blank"} para criar e executar código sob demanda. O código executa em um ambiente de execução sandboxed para prevenir que o código tome ações que estão além do escopo do agente.

*Traduzido usando GitHub Copilot e GPT-4o.*
