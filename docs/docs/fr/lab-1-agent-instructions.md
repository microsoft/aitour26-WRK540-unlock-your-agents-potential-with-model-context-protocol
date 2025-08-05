## Ce Que Vous Apprendrez

Dans ce laboratoire, vous examinez et mettez à jour les instructions de l'agent pour inclure une règle sur l'année financière commençant le 1er juillet. Ceci est important pour que l'agent interprète et analyse correctement les données de vente.

## Introduction

Le but des instructions de l'agent est de définir le comportement de l'agent, incluant comment il interagit avec les utilisateurs, quels outils il peut utiliser, et comment il devrait répondre à différents types de requêtes. Dans ce laboratoire, vous examinerez les instructions existantes de l'agent et ferez une petite mise à jour pour s'assurer que l'agent interprète correctement l'année financière.

## Exercice de Laboratoire

### Ouvrir les Instructions de l'Agent

1. Depuis l'Explorateur VS Code, naviguez vers le dossier `shared/instructions`.
2. **Ouvrez** le fichier `mcp_server_tools_with_code_interpreter.txt`.

### Examiner les Instructions de l'Agent

Examinez comment les instructions définissent le comportement de l'application agent :

!!! tip "Dans VS Code, appuyez sur Alt + Z (Windows/Linux) ou Option + Z (Mac) pour activer le mode de retour à la ligne, rendant les instructions plus faciles à lire."

- **Rôle Principal :** Agent de vente pour Zava (détaillant DIY WA) avec un ton professionnel et amical utilisant des emojis et sans suppositions ou contenu non vérifié.
- **Règles de Base de Données :** Toujours obtenir les schémas d'abord (get_multiple_table_schemas()) avec LIMIT 20 obligatoire sur toutes les requêtes SELECT utilisant les noms exacts de tables/colonnes.
- **Visualisations :** Créer des graphiques UNIQUEMENT quand explicitement demandé en utilisant des déclencheurs comme "graphique", "diagramme", "visualiser", ou "montrer comme [type]" au format PNG téléchargé depuis le bac à sable sans chemins d'images markdown.
- **Réponses :** Par défaut aux tables Markdown avec support multi-langue et CSV disponible sur demande.
- **Sécurité :** Rester dans le scope des données de vente Zava uniquement avec des réponses exactes pour les requêtes hors scope/peu claires et rediriger les utilisateurs hostiles vers l'IT.
- **Contraintes Clés :** Pas de données inventées utilisant les outils seulement avec limite de 20 lignes et images PNG toujours.

### Mettre à Jour les Instructions de l'Agent

Copiez le texte ci-dessous et collez directement après la règle sur ne pas générer de contenu non vérifié ou faire des suppositions :

!!! tip "Cliquez sur l'icône de copie à droite pour copier le texte dans le presse-papiers."

```markdown
- L'année financière pour Zava commence le 1er janvier.
```

Les instructions mises à jour devraient ressembler à ceci :

```markdown
- Ne **générez pas de contenu non vérifié** ou ne faites pas de suppositions.
- L'année financière pour Zava commence le 1er janvier.
```

*Traduit en utilisant GitHub Copilot et GPT-4o.*
