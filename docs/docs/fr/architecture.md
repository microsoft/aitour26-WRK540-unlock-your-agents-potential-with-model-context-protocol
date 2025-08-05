## Architecture de la Solution

Dans cet atelier, vous créerez l'Agent de Vente Zava : un agent conversationnel conçu pour répondre aux questions sur les données de vente, générer des graphiques, fournir des recommandations de produits et prendre en charge les recherches de produits basées sur l'image pour l'activité de bricolage de détail de Zava.

## Composants de l'Application Agent

1. **Services Microsoft Azure**

    Cet agent est construit sur les services Microsoft Azure.

      - **Modèle IA générative** : Le LLM sous-jacent alimentant cette application est le LLM [Azure OpenAI gpt-4o-mini](https://learn.microsoft.com/azure/ai-foundry/openai/concepts/models?tabs=global-standard%2Cstandard-chat-completions#how-do-i-access-the-gpt-4o-and-gpt-4o-mini-models){:target="_blank"}.

      - **Plan de Contrôle** : L'application et ses composants architecturaux sont gérés et surveillés à l'aide du portail [Azure AI Foundry](https://ai.azure.com){:target="_blank"}, accessible via le navigateur.

2. **Azure AI Foundry (SDK)**

    L'atelier est proposé en [Python](https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme?view=azure-python-preview&context=%2Fazure%2Fai-services%2Fagents%2Fcontext%2Fcontext){:target="_blank"} en utilisant le SDK Azure AI Foundry. Le SDK prend en charge les fonctionnalités clés du service Azure AI Agents, incluant l'[Interpréteur de Code](https://learn.microsoft.com/azure/ai-services/agents/how-to/tools/code-interpreter?view=azure-python-preview&tabs=python&pivots=overview){:target="_blank"} et l'intégration du [Model Context Protocol (MCP)](https://modelcontextprotocol.io/){:target="_blank"}.

3. **Base de Données**

    L'application est alimentée par la Base de Données de Ventes Zava, un [serveur flexible Azure Database for PostgreSQL](https://www.postgresql.org/){:target="_blank"} avec l'extension pgvector contenant des données de vente complètes pour les opérations de bricolage de détail de Zava.

    La base de données prend en charge les requêtes complexes pour les données de ventes, d'inventaire et de clients. La Sécurité au Niveau des Lignes (RLS) garantit que les agents n'accèdent qu'aux magasins qui leur sont assignés.

4. **Serveur MCP**

    Le serveur Model Context Protocol (MCP) est un service Python personnalisé qui agit comme un pont entre l'agent et la base de données PostgreSQL. Il gère :

     - **Découverte du Schéma de Base de Données** : Récupère automatiquement les schémas de base de données pour aider l'agent à comprendre les données disponibles.
     - **Génération de Requêtes** : Transforme les demandes en langage naturel en requêtes SQL.
     - **Exécution d'Outils** : Exécute les requêtes SQL et retourne les résultats dans un format que l'agent peut utiliser.
     - **Services de Temps** : Fournit des données liées au temps pour générer des rapports sensibles au temps.

## Extension de la Solution de l'Atelier

L'atelier est facilement adaptable à des cas d'usage comme le support client en mettant à jour la base de données et en personnalisant les instructions du Service d'Agent Foundry.

## Bonnes Pratiques Démontrées dans l'Application

L'application démontre également certaines bonnes pratiques pour l'efficacité et l'expérience utilisateur.

- **APIs Asynchrones** :
  Dans l'exemple de l'atelier, le Service d'Agent Foundry et PostgreSQL utilisent tous deux des APIs asynchrones, optimisant l'efficacité des ressources et l'évolutivité. Ce choix de conception devient particulièrement avantageux lors du déploiement de l'application avec des frameworks web asynchrones comme FastAPI, ASP.NET ou Streamlit.

- **Streaming de Tokens** :
  Le streaming de tokens est implémenté pour améliorer l'expérience utilisateur en réduisant les temps de réponse perçus pour l'application d'agent alimentée par LLM.

- **Observabilité** :
  L'application inclut des [traces](https://learn.microsoft.com/azure/ai-foundry/agents/concepts/tracing){:target="_blank"} et des [métriques](https://learn.microsoft.com/azure/ai-foundry/agents/how-to/metrics){:target="_blank"} intégrées pour surveiller les performances de l'agent, les modèles d'utilisation et la latence. Cela vous permet d'identifier les problèmes et d'optimiser l'agent au fil du temps.

*Traduit en utilisant GitHub Copilot et GPT-4o.*
