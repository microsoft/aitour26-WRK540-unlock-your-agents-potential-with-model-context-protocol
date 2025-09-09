## Introduction

Le traçage vous aide à comprendre et déboguer le comportement de votre agent en montrant la séquence d'étapes, d'entrées et de sorties pendant l'exécution. Dans Azure AI Foundry, le traçage vous permet d'observer comment votre agent traite les demandes, appelle les outils et génère des réponses. Vous pouvez utiliser le portail Azure AI Foundry ou intégrer avec OpenTelemetry et Application Insights pour collecter et analyser les données de trace, facilitant ainsi le dépannage et l'optimisation de votre agent.

## Afficher les traces

Vous pouvez visualiser les traces de l'exécution de votre agent dans le portail Azure AI Foundry ou en utilisant OpenTelemetry. Les traces montreront la séquence d'étapes, les appels d'outils et les données échangées pendant l'exécution de l'agent. Cette information est cruciale pour déboguer et optimiser les performances de votre agent.

### Utiliser le portail Azure AI Foundry

Pour visualiser les traces dans le portail Azure AI Foundry, suivez ces étapes :

1. Naviguez vers le portail [Azure AI Foundry](https://ai.azure.com/).
2. Sélectionnez votre projet.
3. Sélectionnez l'onglet **Tracing** dans le menu de gauche.
4. Ici, vous pouvez voir les traces générées par votre agent.

   ![](media/ai-foundry-tracing.png)

### Approfondir les traces

1. Vous devrez peut-être cliquer sur le bouton **Refresh** pour voir les dernières traces car les traces peuvent prendre quelques moments à apparaître.
2. Sélectionnez la trace nommée `Zava Agent Initialization` pour voir les détails.
   ![](media/ai-foundry-trace-agent-init.png)
3. Sélectionnez la trace `create_agent Zava DIY Sales Agent` pour voir les détails du processus de création de l'agent. Dans la section `Input & outputs`, vous verrez les instructions de l'Agent.
4. Ensuite, sélectionnez la trace `Zava Agent Chat Request: Write an executive...` pour voir les détails de la demande de chat. Dans la section `Input & outputs`, vous verrez l'entrée utilisateur et la réponse de l'agent.

*Traduit en utilisant GitHub Copilot.*
