# Libérez le potentiel de votre agent avec Model Context Protocol et PostgreSQL

## Un atelier interactif de 60 minutes

Imaginez que vous êtes un directeur des ventes chez Zava, une entreprise de bricolage avec des magasins dans tout l'État de Washington et une présence en ligne croissante. Vous vous spécialisez dans l'équipement d'extérieur, les outils d'amélioration de la maison et les fournitures de bricolage.

Vous devez analyser les données de vente pour trouver les tendances, comprendre les préférences des clients et prendre des décisions commerciales éclairées. Pour vous aider, Zava a développé un agent conversationnel qui peut répondre aux questions sur vos données de vente.

![Agent d'analyse des ventes Zava](media/persona.png)

## Ce que vous allez apprendre dans l'atelier

Apprenez à construire un agent IA qui analyse les données de vente, répond aux questions sur les produits et aide les clients à trouver des produits. Sujets clés :

1. **Service d'Agent Azure AI Foundry** : Construisez et déployez des agents IA avec des outils intégrés et de l'observabilité.
2. **Model Context Protocol (MCP)** : Connecte le Service d'Agent à des outils et données externes via des protocoles standards de l'industrie pour améliorer la fonctionnalité de l'agent.
3. **PostgreSQL** : Utilisez PostgreSQL comme base de données vectorielle pour la recherche sémantique et implémentez la sécurité au niveau des lignes (RLS) pour protéger les données sensibles selon les rôles utilisateur.
4. **Azure AI Foundry** : Une plateforme de développement IA de niveau entreprise fournissant un accès unifié aux modèles, un monitoring compréhensif, des capacités de traçage distribué et une gouvernance prête pour la production pour les applications IA à grande échelle.

### Vous commencez tout juste votre parcours avec les agents IA ?

Nouveau dans les agents IA ? Commencez avec [Construisez votre agent code-first avec Azure AI Foundry](https://aka.ms/aitour/WRK552){:target="_blank"}. Vous construirez un agent code-first intégrant les LLM avec les bases de données, documents et Bing Search—une base solide pour des agents avancés comme Zava.

## Qu'est-ce qu'un agent IA alimenté par LLM ?

Un agent IA alimenté par LLM est un logiciel semi-autonome qui atteint des objectifs sans étapes prédéfinies. Au lieu de workflows codés en dur, il décide quoi faire basé sur les instructions et le contexte.

Exemple : Si un utilisateur demande "Montre les ventes totales par magasin sous forme de graphique circulaire", l'agent interprète la demande, suit le contexte et orchestre les bons outils pour produire le graphique—aucune logique préconstruite requise.

Cela déplace une grande partie de la logique applicative des développeurs vers le modèle. Des instructions claires et des outils fiables sont essentiels pour un comportement d'agent prévisible et des résultats.

## Introduction à Azure AI Foundry

[Azure AI Foundry](https://azure.microsoft.com/products/ai-foundry/){:target="_blank"} est la plateforme sécurisée et flexible de Microsoft pour concevoir, personnaliser et gérer les applications et agents IA. Tout—modèles, agents, outils et observabilité—vit derrière un seul portail, SDK et point de terminaison REST, pour que vous puissiez déployer vers le cloud ou la périphérie avec gouvernance et contrôles de coûts en place dès le premier jour.

![Architecture Azure AI Foundry](media/azure-ai-foundry.png)

*Traduit en utilisant GitHub Copilot.*
