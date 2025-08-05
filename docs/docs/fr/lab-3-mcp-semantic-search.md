## Ce Que Vous Apprendrez

Dans ce laboratoire, vous activez les capacités de recherche sémantique dans l'Agent Azure AI en utilisant le Model Context Protocol (MCP) et la base de données PostgreSQL.

## Introduction

Ce laboratoire met à niveau l'Agent Azure AI avec la recherche sémantique en utilisant le Model Context Protocol (MCP) et PostgreSQL. Les noms et descriptions de produits ont été convertis en vecteurs avec le modèle d'embedding OpenAI (text-embedding-3-small) et stockés dans la base de données. Cela permet à l'agent de comprendre l'intention de l'utilisateur et de fournir des réponses plus précises.

## Exercice de Laboratoire

Du laboratoire précédent, vous pouvez poser des questions à l'agent sur les données de vente, mais il était limité aux correspondances exactes. Dans ce laboratoire, vous étendez les capacités de l'agent en implémentant la recherche sémantique en utilisant le Model Context Protocol (MCP). Cela permettra à l'agent de comprendre et de répondre aux requêtes qui ne sont pas des correspondances exactes, améliorant sa capacité à aider les utilisateurs avec des questions plus complexes.

1. Collez la question suivante dans l'onglet Web Chat de votre navigateur :

    ```text
    Comment les différents magasins ont-ils performé avec les disjoncteurs 18A ?
    ```

    L'agent répond : "Je n'ai pas pu trouver de données de vente pour les disjoncteurs 18A dans nos enregistrements. 😱 Cependant, voici quelques suggestions de produits similaires que vous pourriez vouloir explorer." Cela arrive parce que l'agent s'appuie uniquement sur la correspondance des requêtes par mots-clés et ne comprend pas le sens sémantique de votre question. Le LLM peut encore faire des suggestions de produits éclairées à partir de tout contexte de produit qu'il pourrait déjà avoir.

## Implémenter la Recherche Sémantique

Dans cette section, vous implémenterez la recherche sémantique en utilisant le Model Context Protocol (MCP) pour améliorer les capacités de l'agent.

1. Appuyez sur <kbd>F1</kbd> pour **ouvrir** la Palette de Commandes VS Code.
2. Tapez **Open File** et sélectionnez **File: Open File...**.
3. **Collez** le chemin suivant dans le sélecteur de fichiers et appuyez sur <kbd>Entrée</kbd> :

    ```text
    /workspace/src/python/mcp_server/sales_analysis/sales_analysis.py
    ```

4. Faites défiler vers le bas jusqu'à la ligne 100 environ et cherchez la méthode `semantic_search_products`. Cette méthode est responsable de l'exécution de la recherche sémantique sur les données de vente. Vous remarquerez que le décorateur **@mcp.tool()** est commenté. Ce décorateur est utilisé pour enregistrer la méthode comme un outil MCP, permettant qu'elle soit appelée par l'agent.

5. Décommentez le décorateur `@mcp.tool()` en supprimant le `#` au début de la ligne. Cela activera l'outil de recherche sémantique.

    ```python
    # @mcp.tool()
    async def semantic_search_products(
        ctx: Context,
        query_description: Annotated[str, Field(
        ...
    ```

6. Ensuite, vous devez activer les instructions de l'Agent pour utiliser l'outil de recherche sémantique. Revenez au fichier `app.py`.
7. Faites défiler vers le bas jusqu'à la ligne 30 environ et trouvez la ligne `# INSTRUCTIONS_FILE = "instructions/mcp_server_tools_with_semantic_search.txt"`.
8. Décommentez la ligne en supprimant le `#` au début. Cela permettra à l'agent d'utiliser l'outil de recherche sémantique.

    ```python
    INSTRUCTIONS_FILE = "instructions/mcp_server_tools_with_semantic_search.txt"
    ```

## Examiner les Instructions de l'Agent

1. Appuyez sur <kbd>F1</kbd> pour ouvrir la Palette de Commandes VS Code.
2. Tapez **Open File** et sélectionnez **File: Open File...**.
3. Collez le chemin suivant dans le sélecteur de fichiers et appuyez sur <kbd>Entrée</kbd> :

    ```text
    /workspace/src/shared/instructions/mcp_server_tools_with_semantic_search.txt
    ```

4. Examinez les instructions dans le fichier. Ces instructions demandent à l'agent d'utiliser l'outil de recherche sémantique pour répondre aux questions sur les données de vente.

## Démarrer l'Application Agent avec l'Outil de Recherche Sémantique

1. **Arrêtez** l'application agent actuelle en appuyant sur <kbd>Shift + F5</kbd>.
2. **Redémarrez** l'application agent en appuyant sur <kbd>F5</kbd>. Cela démarrera l'agent avec les instructions mises à jour et l'outil de recherche sémantique activé.
3. Revenez à l'onglet **Web Chat** dans votre navigateur.
4. Entrez la question suivante dans le chat :

    ```text
    Comment les différents magasins ont-ils performé avec les disjoncteurs 18A ?
    ```

    L'agent comprend maintenant le sens sémantique de la question et répond en conséquence avec les données de vente pertinentes.

    !!! info "Note"
        L'outil de Recherche Sémantique MCP fonctionne comme suit :

        1. La question est convertie en vecteur en utilisant le même modèle d'embedding OpenAI (text-embedding-3-small) que les descriptions de produits.
        2. Ce vecteur est utilisé pour rechercher des vecteurs de produits similaires dans la base de données PostgreSQL.
        3. L'agent reçoit les résultats et les utilise pour générer une réponse.

*Traduit en utilisant GitHub Copilot et GPT-4o.*
