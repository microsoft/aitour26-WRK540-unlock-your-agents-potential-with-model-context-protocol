## Ce que vous allez apprendre

Dans ce lab, vous examinerez et mettrez à jour les instructions de l'agent pour inclure une règle concernant l'année financière commençant le 1er juillet. Ceci est important pour que l'agent interprète et analyse correctement les données de vente.

## Introduction

Le but des instructions d'agent est de définir le comportement de l'agent, y compris comment il interagit avec les utilisateurs, quels outils il peut utiliser et comment il devrait répondre à différents types de requêtes. Dans ce lab, vous examinerez les instructions d'agent existantes et ferez une petite mise à jour pour vous assurer que l'agent interprète correctement l'année financière.

## Exercice de lab

### Ouvrir les instructions de l'agent

1. Dans l'Explorateur VS Code, naviguez vers le dossier `shared/instructions`.
2. **Ouvrez** le fichier `mcp_server_tools_with_code_interpreter.txt`.

### Examiner les instructions de l'agent

Examinez comment les instructions définissent le comportement de l'application agent :

!!! tip "Dans VS Code, appuyez sur Alt + Z (Windows/Linux) ou Option + Z (Mac) pour activer le mode de retour à la ligne, rendant les instructions plus faciles à lire."

- **Rôle principal :** Agent de vente pour Zava (détaillant DIY WA) avec un ton professionnel et amical utilisant des emojis et sans suppositions ou contenu non vérifié.
- **Règles de base de données :** Toujours obtenir les schémas d'abord (get_multiple_table_schemas()) avec LIMIT 20 obligatoire sur toutes les requêtes SELECT utilisant les noms exacts de table/colonne.
- **Visualisations :** Créer des graphiques SEULEMENT lorsque explicitement demandé en utilisant des déclencheurs comme "graphique", "graphe", "visualiser", ou "montrer comme [type]" au format PNG téléchargé depuis le sandbox sans chemins d'images markdown.
- **Réponses :** Par défaut aux tableaux Markdown avec support multi-langue et CSV disponible sur demande.
- **Sécurité :** Rester dans le périmètre des données de vente Zava uniquement avec des réponses exactes pour les requêtes hors périmètre/peu claires et rediriger les utilisateurs hostiles vers l'IT.
- **Contraintes clés :** Aucune donnée inventée utilisant les outils uniquement avec limite de 20 lignes et images PNG toujours.

### Mettre à jour les instructions de l'agent

Copiez le texte ci-dessous et collez directement après la règle concernant ne pas générer de contenu non vérifié ou faire des suppositions :

!!! tip "Cliquez sur l'icône de copie à droite pour copier le texte dans le presse-papiers."

```markdown
- **L'année financière (AF) commence le 1er juillet** (T1=Jul–Sep, T2=Oct–Déc, T3=Jan–Mar, T4=Avr–Juin).
```

Les instructions mises à jour devraient ressembler à ceci :

```markdown
- Utilisez **uniquement** les sorties d'outils vérifiées ; **jamais** inventer des données ou suppositions.
- **L'année financière (AF) commence le 1er juillet** (T1=Jul–Sep, T2=Oct–Déc, T3=Jan–Mar, T4=Avr–Juin).
```

*Traduit en utilisant GitHub Copilot.*
