Cette application d'atelier est conçue pour l'éducation et l'adaptation, et n'est pas destinée à un usage en production prêt à l'emploi. Néanmoins, elle démontre certaines meilleures pratiques pour la sécurité.

## Attaques SQL Malveillantes

Une préoccupation commune avec le SQL généré par LLM est le risque d'injection ou de requêtes nuisibles. Ces risques sont atténués en limitant les permissions de base de données.

Cette application utilise PostgreSQL avec des privilèges restreints pour l'agent et fonctionne dans un environnement sécurisé. La Sécurité au Niveau des Lignes (RLS) garantit que les agents accèdent uniquement aux données de leurs magasins assignés.

Dans les environnements d'entreprise, les données sont typiquement extraites dans une base de données ou entrepôt en lecture seule avec un schéma simplifié. Cela garantit un accès sécurisé, performant et en lecture seule pour l'agent.

## Sandboxing

Ceci utilise l'[Interpréteur de Code du Service d'Agents Azure AI](https://learn.microsoft.com/azure/ai-services/agents/how-to/tools/code-interpreter?view=azure-python-preview&tabs=python&pivots=overview){:target="_blank"} pour créer et exécuter du code à la demande. Le code s'exécute dans un environnement d'exécution sandboxé pour empêcher le code de prendre des actions qui sont au-delà de la portée de l'agent.

*Traduit en utilisant GitHub Copilot et GPT-4o.*
