## Introduction

!!! note "Le traçage avec le Tableau de bord Aspire n'est pris en charge que dans la version C# de l'atelier."

Jusqu'à présent pour notre traçage, nous nous sommes concentrés sur la façon de visualiser ceci via les tableaux de bord Azure AI Foundry, ce qui peut être une interruption dans le flux de travail lors du développement local. En plus de cela, nous pouvons tirer parti du Tableau de bord Aspire pour visualiser les traces générées par notre application en temps réel, et comment une action s'étend sur plusieurs ressources dans notre système.

## Exécuter l'application Agent

Lancez l'application en appuyant sur <kbd>F5</kbd> et attendez que le Tableau de bord Aspire apparaisse dans votre navigateur. Cela montrera une liste complète des ressources dans l'atelier.

![Tableau de bord Aspire](../media/lab-7-dashboard.png)

Comme avec les étapes de lab précédentes, ouvrez le **Workshop Frontend** et entrez une invite dans le chat, telle que :

```plaintext
Rédigez un rapport exécutif qui analyse les 5 principales catégories de produits et compare les performances du magasin en ligne par rapport à la moyenne des magasins physiques.
```

## Visualiser les traces

Pour voir les traces générées par votre application, naviguez vers l'onglet **Traces** dans le Tableau de bord Aspire. Ici, vous pouvez voir une liste de toutes les traces qui ont été capturées, en commençant par leur originateur.

![Aperçu des traces](../media/lab-7-trace-overview.png)

La dernière entrée dans la capture d'écran ci-dessus montre l'événement depuis le **dotnet-front-end** effectuant un `GET` vers `/chat/stream`. La colonne **Span** montre alors les ressources sur lesquelles cette trace s'étend, `dotnet-front-end`, `dotnet-agent-app`, `ai-foundry`, `dotnet-mcp-server`, et `pg`.

Chaque ressource a un numéro associé, qui est le nombre de _spans_ qui ont eu lieu pour cette ressource. Nous pouvons également noter un indicateur d'erreur sur les ressources `dotnet-mcp-server` et `pg`, ce qui indiquerait qu'une erreur s'est produite sur ces ressources.

Cliquer sur la trace vous montrera une vue détaillée de la chronologie de la trace :

![Chronologie des traces](../media/lab-7-trace-timeline.png)

À partir d'ici, nous pouvons voir les spans individuels, l'ordre dans lequel ils se sont produits, leur durée, et comment les événements se sont déroulés à travers les ressources dans notre application.

Cliquer sur un span individuel vous montrera plus de détails sur ce span spécifique :

![Détails du span](../media/lab-7-span-details.png)

Essayez d'expérimenter avec différentes invites et de simuler des erreurs, pour observer comment les traces changent dans le Tableau de bord Aspire.

## Lecture supplémentaire

- [Documentation Aspire](https://aka.ms/aspire-docs)
- [Documentation de télémétrie Aspire](https://learn.microsoft.com/dotnet/aspire/fundamentals/telemetry)

*Traduit en utilisant GitHub Copilot.*
