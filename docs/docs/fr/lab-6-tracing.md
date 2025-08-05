**TBC : Ce label amènera l'utilisateur à mettre à jour le fichier d'instructions de l'agent pour supprimer les emojis ennuyeux que l'agent utilise dans ses réponses.**

## Introduction

Le traçage vous aide à comprendre et déboguer le comportement de votre agent en montrant la séquence d'étapes, d'entrées et de sorties pendant l'exécution. Dans Azure AI Foundry, le traçage vous permet d'observer comment votre agent traite les demandes, appelle les outils et génère les réponses. Vous pouvez utiliser le portail Azure AI Foundry ou intégrer avec OpenTelemetry et Application Insights pour collecter et analyser les données de trace, facilitant le dépannage et l'optimisation de votre agent.

<!-- ## Exercice de Laboratoire

=== "Python"

      1. Ouvrez le fichier `app.py`.
      2. Changez la variable `AZURE_TELEMETRY_ENABLED` à `True` pour activer le traçage :

         ```python
         AZURE_TELEMETRY_ENABLED = True
         ```

        !!! info "Note"
            Ce paramètre active la télémétrie pour votre agent. Dans la fonction `initialize` dans `app.py`, le client de télémétrie est configuré pour envoyer des données à Azure Monitor.

            ```python
             if AZURE_TELEMETRY_ENABLED:
                 configure_azure_monitor(connection_string=await self.project_client.telemetry.get_connection_string())
            ```         

=== "C#"

      tbd -->

## Exécuter l'Application Agent

1. Appuyez sur <kbd>F5</kbd> pour exécuter l'application.
2. Sélectionnez **Preview in Editor** pour ouvrir l'application agent dans un nouvel onglet d'éditeur.

### Commencer une Conversation avec l'Agent

Copiez et collez le prompt suivant dans l'application agent pour commencer une conversation :

```plaintext
Rédigez un rapport exécutif qui analyse les 5 meilleures catégories de produits et compare les performances de la boutique en ligne par rapport à la moyenne des magasins physiques.
```

## Voir les Traces

Vous pouvez voir les traces de l'exécution de votre agent dans le portail Azure AI Foundry ou en utilisant OpenTelemetry. Les traces montreront la séquence d'étapes, les appels d'outils et les données échangées pendant l'exécution de l'agent. Cette information est cruciale pour déboguer et optimiser les performances de votre agent.

### Utilisation du Portail Azure AI Foundry

Pour voir les traces dans le portail Azure AI Foundry, suivez ces étapes :

1. Naviguez vers le portail **[Azure AI Foundry](https://ai.azure.com/)**.
2. Sélectionnez votre projet.
3. Sélectionnez l'onglet **Tracing** dans le menu de gauche.
4. Ici, vous pouvez voir les traces générées par votre agent.

   ![](media/ai-foundry-tracing.png)

### Exploration Détaillée des Traces

1. Vous devrez peut-être cliquer sur le bouton **Refresh** pour voir les dernières traces car les traces peuvent prendre quelques instants à apparaître.
2. Sélectionnez la trace nommée `Zava Agent Initialization` pour voir les détails.
   ![](media/ai-foundry-trace-agent-init.png)
3. Sélectionnez la trace `creare_agent Zava DIY Sales Agent` pour voir les détails du processus de création de l'agent. Dans la section `Input & outputs`, vous verrez les instructions de l'Agent.
4. Ensuite, sélectionnez la trace `Zava Agent Chat Request: Write an executive...` pour voir les détails de la demande de chat. Dans la section `Input & outputs`, vous verrez l'entrée utilisateur et la réponse de l'agent.

<!-- https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/continuous-evaluation-agents -->

*Traduit en utilisant GitHub Copilot et GPT-4o.*
