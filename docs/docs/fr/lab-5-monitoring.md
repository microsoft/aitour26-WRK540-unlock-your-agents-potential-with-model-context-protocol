## Introduction

La surveillance maintient votre Service d'Agent Azure AI Foundry disponible, performant et fiable. Azure Monitor collecte les métriques et logs, fournit des insights en temps réel et envoie des alertes. Utilisez les tableaux de bord et alertes personnalisées pour suivre les métriques clés, analyser les tendances et répondre de manière proactive. Accédez à la surveillance via le portail Azure, CLI, API REST ou bibliothèques client.

## Exercice de lab

1. Dans l'explorateur de fichiers VS Code, ouvrez le fichier `resources.txt` dans le dossier `workshop`.
1. **Copiez** la valeur pour la clé `AI Project Name` dans le presse-papiers.
1. Naviguez vers la page [Portail Azure AI Foundry](https://ai.azure.com){:target="_blank"}.
1. Sélectionnez votre projet dans la liste des projets foundry.

## Ouvrir le tableau de bord de surveillance

1. Dans le `resources.txt`, copiez la valeur pour `Application Insights Name` dans le presse-papiers.
1. Revenez au portail AI Foundry, sélectionnez la section **Monitoring** dans le menu de gauche.
1. Collez le `Application Insights Name` copié dans la liste déroulante `Application Insights resource name`.
1. Sélectionnez la ressource **Application Insights** dans la liste déroulante.
1. Sélectionnez **Connect**.

### Explorer le tableau de bord de surveillance

Familiarisez-vous avec les informations disponibles sur le tableau de bord `Application analytics`.

!!!tip "Vous pouvez sélectionner des plages de dates pour filtrer les données affichées dans les outils de surveillance."

![L'image montre le tableau de bord de surveillance des applications](../media/monitor_usage.png)

### Surveiller l'utilisation des ressources

Vous pouvez creuser plus profondément, sélectionnez `Resource Usage` pour voir les métriques détaillées sur la consommation de ressources de votre projet IA. Encore une fois, vous pouvez filtrer les données par plage de temps.

![L'image montre le tableau de bord de surveillance de l'utilisation des ressources](../media/monitor_resource_usage.png)

*Traduit en utilisant GitHub Copilot.*
