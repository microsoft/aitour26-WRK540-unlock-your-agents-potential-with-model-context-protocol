## Ce Que Vous Apprendrez

Dans ce laboratoire, vous activerez l'Interpréteur de Code pour analyser les données de vente et créer des graphiques en utilisant le langage naturel.

## Introduction

Dans ce laboratoire, vous étendrez l'Agent Azure AI avec deux outils :

- **Interpréteur de Code :** Permet à l'agent de générer et d'exécuter du code Python pour l'analyse de données et la visualisation.
- **Outils de Serveur MCP :** Permettent à l'agent d'accéder aux sources de données externes en utilisant les Outils MCP, dans notre cas les données dans une base de données PostgreSQL.

## Exercice de Laboratoire

### Activer l'Interpréteur de Code

Dans ce laboratoire, vous activerez l'Interpréteur de Code pour exécuter le code Python généré par le LLM pour analyser les données de vente de détail de Zava.

=== "Python"

    1. **Ouvrez** le `app.py`.
    2. **Décommentez** la ligne qui ajoute l'outil Interpréteur de Code à l'ensemble d'outils de l'agent dans la méthode `_setup_agent_tools` de la classe `AgentManager`. Cette ligne est actuellement commentée avec un `#` au début :

        ```python
        # code_interpreter = CodeInterpreterTool()
        # self.toolset.add(code_interpreter)
        ```

    3. **Examinez** le code dans le fichier `app.py`. Vous remarquerez que l'Interpréteur de Code et les outils de Serveur MCP sont ajoutés à l'ensemble d'outils de l'agent dans la méthode `_setup_agent_tools` de la classe `AgentManager`.

        ```python

        Après avoir décommenté, votre code devrait ressembler à ceci :

        ```python
        class AgentManager:
            """Manages Azure AI Agent lifecycle and dependencies."""

            async def _setup_agent_tools(self) -> None:
                """Setup MCP tools and code interpreter."""

                # Enable the code interpreter tool
                code_interpreter = CodeInterpreterTool()
                self.toolset.add(code_interpreter)

                print("Setting up Agent tools...")
                ...
        ```

=== "C#"

    TBD

## Démarrer l'Application Agent

1. Copiez le texte ci-dessous dans le presse-papiers :

    ```text
    Debug: Select and Start Debugging
    ```

2. Appuyez sur <kbd>F1</kbd> pour ouvrir la Palette de Commandes VS Code.
3. Collez le texte dans la Palette de Commandes et sélectionnez **Debug: Select and Start Debugging**.
4. Sélectionnez **🔁🤖Debug Compound: Agent and MCP (stdio)** dans la liste. Cela démarrera l'application agent et le client de chat web.

## Ouvrir le Client de Chat Web de l'Agent

1. Copiez le texte ci-dessous dans le presse-papiers :

    ```text
    Open Port in Browser
    ```

2. Appuyez sur <kbd>F1</kbd> pour ouvrir la Palette de Commandes VS Code.
3. Collez le texte dans la Palette de Commandes et sélectionnez **Open Port in Browser**.
4. Sélectionnez **8005** dans la liste. Cela ouvrira le client de chat web de l'agent dans votre navigateur.

### Commencer une Conversation avec l'Agent

Depuis le client de chat web, vous pouvez commencer une conversation avec l'agent. L'agent est conçu pour répondre aux questions sur les données de vente de Zava et générer des visualisations en utilisant l'Interpréteur de Code.

1. Analyse des ventes de produits. Copiez et collez la question suivante dans le chat :

    ```text
    Montrez les 10 meilleurs produits par chiffre d'affaires par magasin pour le dernier trimestre
    ```

    Après un moment, l'agent répondra avec un tableau montrant les 10 meilleurs produits par chiffre d'affaires pour chaque magasin.

    !!! info
        L'agent utilise le LLM qui appelle trois outils de Serveur MCP pour récupérer les données et les afficher dans un tableau :

           1. **get_current_utc_date()** : Obtient la date et l'heure actuelles pour que l'agent puisse déterminer le dernier trimestre par rapport à la date actuelle.
           2. **get_multiple_table_schemas()** : Obtient les schémas des tables dans la base de données requis par le LLM pour générer du SQL valide.
           3. **execute_sales_query** : Exécute une requête SQL pour récupérer les 10 meilleurs produits par chiffre d'affaires pour le dernier trimestre depuis la base de données PostgreSQL.

2. Générer un graphique en secteurs. Copiez et collez la question suivante dans le chat :

    ```text
    Montrez les ventes par magasin sous forme de graphique en secteurs pour cette année financière
    ```

    L'agent répondra avec un graphique en secteurs montrant la distribution des ventes par magasin pour l'année financière actuelle.

    !!! info
        Cela peut sembler magique, alors que se passe-t-il en coulisses pour faire fonctionner tout cela ?

        Le Service d'Agent Foundry orchestre les étapes suivantes :

        1. Comme la question précédente, l'agent détermine s'il a les schémas de table requis pour la requête. Si ce n'est pas le cas, il utilise les outils **get_multiple_table_schemas()** pour obtenir la date actuelle et le schéma de base de données.
        2. L'agent utilise ensuite l'outil **execute_sales_query** pour récupérer les ventes
        3. En utilisant les données retournées, le LLM écrit du code Python pour créer un Graphique en Secteurs.
        4. Finalement, l'Interpréteur de Code exécute le code Python pour générer le graphique.

3. Continuez à poser des questions sur les données de vente Zava pour voir l'Interpréteur de Code en action. Voici quelques questions de suivi que vous pourriez vouloir essayer :

    - ```Déterminez quels produits ou catégories stimulent les ventes. Montrez sous forme de Graphique en Barres.```
    - ```Quel serait l'impact d'un événement de choc (par exemple, 20% de baisse des ventes dans une région) sur la distribution globale des ventes ? Montrez sous forme de Graphique en Barres Groupées.```
        - Suivez avec ```Et si l'événement de choc était de 50% ?```
    - ```Quelles régions ont des ventes au-dessus ou en dessous de la moyenne ? Montrez sous forme de Graphique en Barres avec Déviation de la Moyenne.```
    - ```Quelles régions ont des remises au-dessus ou en dessous de la moyenne ? Montrez sous forme de Graphique en Barres avec Déviation de la Moyenne.```
    - ```Simulez les ventes futures par région en utilisant une simulation Monte Carlo pour estimer les intervalles de confiance. Montrez sous forme de Ligne avec Bandes de Confiance en utilisant des couleurs vives.```

<!-- ## Arrêter l'Application Agent

1. Revenez à l'éditeur VS Code.
1. Appuyez sur <kbd>Shift + F5</kbd> pour arrêter l'application agent. -->

## Laissez l'Application Agent Fonctionner

Laissez l'application agent fonctionner car vous l'utiliserez dans le prochain laboratoire pour étendre l'agent avec plus d'outils et de capacités.

*Traduit en utilisant GitHub Copilot et GPT-4o.*
