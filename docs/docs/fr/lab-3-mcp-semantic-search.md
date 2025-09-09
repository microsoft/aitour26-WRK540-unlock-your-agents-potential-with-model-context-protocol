## Ce que vous allez apprendre

Dans ce lab, vous activez les capacités de recherche sémantique dans l'Agent Azure AI en utilisant le serveur MCP et la base de données PostgreSQL avec l'extension [PostgreSQL Vector](https://github.com/pgvector/pgvector){:target="\_blank"} activée.

## Introduction

Ce lab met à niveau l'Agent Azure AI avec la recherche sémantique en utilisant le serveur MCP et PostgreSQL.

Tous les noms et descriptions de produits de Zava ont été convertis en vecteurs avec le modèle d'embedding OpenAI (text-embedding-3-small) et stockés dans la base de données. Cela permet à l'agent de comprendre l'intention de l'utilisateur et de fournir des réponses plus précises.

??? info "Pour les développeurs : Comment fonctionne la recherche sémantique PostgreSQL ?"

    ### Vectorisation des descriptions et noms de produits

    Pour en savoir plus sur la façon dont les noms et descriptions de produits Zava ont été vectorisés, voir le [README du générateur de base de données PostgreSQL Zava DIY](https://github.com/microsoft/aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol/tree/main/data/database){:target="_blank"}.

    === "Python"

        ### Le LLM appelle l'outil du serveur MCP

        Basé sur la requête de l'utilisateur et les instructions fournies, le LLM décide d'appeler l'outil du serveur MCP `semantic_search_products` pour trouver des produits pertinents.

        La séquence d'événements suivante se produit :

        1. L'outil MCP `semantic_search_products` est invoqué avec la description de requête de l'utilisateur.
        1. Le serveur MCP génère un vecteur pour la requête en utilisant le modèle d'embedding OpenAI (text-embedding-3-small). Voir le code pour vectoriser la requête dans la méthode `generate_query_embedding`.
        1. Le serveur MCP effectue ensuite une recherche sémantique contre la base de données PostgreSQL pour trouver des produits avec des vecteurs similaires.

        ### Aperçu de la recherche sémantique PostgreSQL

        L'outil du serveur MCP `semantic_search_products` exécute alors une requête SQL qui utilise la requête vectorisée pour trouver les vecteurs de produits les plus similaires dans la base de données. La requête SQL utilise l'opérateur `<->` fourni par l'extension pgvector pour calculer la distance entre les vecteurs.

        ```python
        async def search_products_by_similarity(
            self, query_embedding: list[float], 
                rls_user_id: str, 
                max_rows: int = 20, 
                similarity_threshold: float = 30.0
        ) -> str:
                ...
                query = f"""
                    SELECT 
                        p.*,
                        (pde.description_embedding <=> $1::vector) as similarity_distance
                    FROM {SCHEMA_NAME}.product_description_embeddings pde
                    JOIN {SCHEMA_NAME}.products p ON pde.product_id = p.product_id
                    WHERE (pde.description_embedding <=> $1::vector) <= $3
                    ORDER BY similarity_distance
                    LIMIT $2
                """

                rows = await conn.fetch(query, embedding_str, max_rows, distance_threshold)
                ...
        ```

    === "C#"

        ### Le LLM appelle l'outil du serveur MCP

        Basé sur la requête de l'utilisateur et les instructions fournies, le LLM décide d'appeler l'outil du serveur MCP `semantic_search_products` pour trouver des produits pertinents.

        La séquence d'événements suivante se produit :

        1. L'outil MCP `semantic_search_products` est invoqué avec la description de requête de l'utilisateur.
        2. Le serveur MCP génère un vecteur pour la requête en utilisant le modèle d'embedding OpenAI (text-embedding-3-small). Voir la méthode `GenerateVectorAsync` dans le fichier `EmbeddingGeneratorExtensions.cs`.
        3. Le serveur MCP effectue ensuite une recherche sémantique contre la base de données PostgreSQL pour trouver des produits avec des vecteurs similaires.

        ### Aperçu de la recherche sémantique PostgreSQL

        L'outil du serveur MCP `semantic_search_products` exécute alors une requête SQL qui utilise la requête vectorisée pour trouver les vecteurs de produits les plus similaires dans la base de données. La requête SQL utilise l'opérateur `<->` fourni par l'extension pgvector pour calculer la distance entre les vecteurs.

        ```csharp
        public async Task<IEnumerable<SemanticSearchResult>> SemanticSearchProductsAsync(
        ...
            await using var searchCmd = new NpgsqlCommand("""
            SELECT 
                p.*,
                (pde.description_embedding <=> $1::vector) as similarity_distance
            FROM retail.product_description_embeddings pde
            JOIN retail.products p ON pde.product_id = p.product_id
            WHERE (pde.description_embedding <=> $1::vector) <= $3
            ORDER BY similarity_distance
            LIMIT $2
            """, connection);
            searchCmd.Parameters.AddWithValue(new Vector(embeddings));
            searchCmd.Parameters.AddWithValue(maxRows);
            searchCmd.Parameters.AddWithValue(distanceThreshold);

            await using var reader = await searchCmd.ExecuteReaderAsync();
            var results = new List<SemanticSearchResult>();
        ```

## Exercice de lab

Depuis le lab précédent, vous pouvez poser à l'agent des questions sur les données de vente, mais il était limité aux correspondances exactes. Dans ce lab, vous étendez les capacités de l'agent en implémentant la recherche sémantique en utilisant le Model Context Protocol (MCP). Cela permettra à l'agent de comprendre et répondre aux requêtes qui ne sont pas des correspondances exactes, améliorant sa capacité à aider les utilisateurs avec des questions plus complexes.

1. Collez la question suivante dans l'onglet Web Chat dans votre navigateur :

   ```text
   Quels disjoncteurs de 18 ampères vendons-nous ?
   ```

   L'agent répond avec quelque chose de similaire à ce message :

   _"Je n'ai pas pu trouver de disjoncteurs spécifiques de 18 ampères dans notre inventaire. Cependant, nous pourrions avoir d'autres types de disjoncteurs disponibles. Aimeriez-vous que je recherche des disjoncteurs généraux ou d'autres produits connexes ? 😊"_

## Arrêter l'application Agent

Depuis VS Code, arrêtez l'application agent en appuyant sur <kbd>Shift + F5</kbd>.

=== "Python"

    ## Implémenter la recherche sémantique

    Dans cette section, vous allez implémenter la recherche sémantique en utilisant le Model Context Protocol (MCP) pour améliorer les capacités de l'agent.

    1. Appuyez sur <kbd>F1</kbd> pour **ouvrir** la Palette de Commandes VS Code.
    2. Tapez **Open File** et sélectionnez **File: Open File...**.
    3. **Collez** le chemin suivant dans le sélecteur de fichier et appuyez sur <kbd>Entrée</kbd> :

        ```text
        /workspace/src/python/mcp_server/sales_analysis/sales_analysis.py
        ```

    4. Faites défiler vers la ligne 70 environ et cherchez la méthode `semantic_search_products`. Cette méthode est responsable de l'exécution de la recherche sémantique sur les données de vente. Vous remarquerez que le décorateur **@mcp.tool()** est commenté. Ce décorateur est utilisé pour enregistrer la méthode comme un outil MCP, permettant qu'elle soit appelée par l'agent.

    5. Décommentez le décorateur `@mcp.tool()` en supprimant le `#` au début de la ligne. Cela activera l'outil de recherche sémantique.

        ```python
        # @mcp.tool()
        async def semantic_search_products(
            ctx: Context,
            query_description: Annotated[str, Field(
            ...
        ```

    6. Ensuite, vous devez activer les instructions de l'Agent pour utiliser l'outil de recherche sémantique. Revenez au fichier `app.py`.
    7. Faites défiler vers la ligne 30 environ et trouvez la ligne `# INSTRUCTIONS_FILE = "instructions/mcp_server_tools_with_semantic_search.txt"`.
    8. Décommentez la ligne en supprimant le `#` au début. Cela permettra à l'agent d'utiliser l'outil de recherche sémantique.

        ```python
        INSTRUCTIONS_FILE = "instructions/mcp_server_tools_with_semantic_search.txt"
        ```

=== "C#"

    ## Implémenter la recherche sémantique

    Dans cette section, vous allez implémenter la recherche sémantique en utilisant le Model Context Protocol (MCP) pour améliorer les capacités de l'agent.

    1. Ouvrez le fichier `McpHost.cs` du projet `McpAgentWorkshop.WorkshopApi`.
    1. Localisez où les autres outils MCP sont enregistrés avec le serveur MCP, et enregistrez la classe `SemanticSearchTools` comme un outil MCP.

        ```csharp
        builder.Services.AddMcpTool<SemanticSearchTools>();
        ```

        !!! info "Note"
            Lisez l'implémentation de `SemanticSearchTools` pour apprendre comment le serveur MCP effectuera la recherche.

    1. Ensuite, vous devez activer les instructions de l'Agent pour utiliser l'outil de recherche sémantique. Revenez à la classe `AgentService` et changez la constante `InstructionsFile` à `mcp_server_tools_with_semantic_search.txt`.

## Examiner les instructions de l'agent

1. Appuyez sur <kbd>F1</kbd> pour ouvrir la Palette de Commandes VS Code.
2. Tapez **Open File** et sélectionnez **File: Open File...**.
3. Collez le chemin suivant dans le sélecteur de fichier et appuyez sur <kbd>Entrée</kbd> :

   ```text
   /workspace/src/shared/instructions/mcp_server_tools_with_semantic_search.txt
   ```

4. Examinez les instructions dans le fichier. Ces instructions instruisent l'agent d'utiliser l'outil de recherche sémantique pour répondre aux questions sur les données de vente.

## Démarrer l'application Agent avec l'outil de recherche sémantique

1. **Démarrez** l'application agent en appuyant sur <kbd>F5</kbd>. Cela démarrera l'agent avec les instructions mises à jour et l'outil de recherche sémantique activé.
2. Ouvrez le **Web Chat** dans votre navigateur.
3. Entrez la question suivante dans le chat :

    ```text
    Quels disjoncteurs de 18 ampères vendons-nous ?
    ```

    L'agent comprend maintenant le sens sémantique de la question et répond en conséquence avec des données de vente pertinentes.

    !!! info "Note"
        L'outil de recherche sémantique MCP fonctionne comme suit :

        1. La question est convertie en vecteur en utilisant le même modèle d'embedding OpenAI (text-embedding-3-small) que les descriptions de produits.
        2. Ce vecteur est utilisé pour rechercher des vecteurs de produits similaires dans la base de données PostgreSQL.
        3. L'agent reçoit les résultats et les utilise pour générer une réponse.

## Rédiger un rapport exécutif

La dernière invitation pour cet atelier est la suivante :

```plaintext
Rédigez un rapport exécutif sur la performance de vente de différents magasins pour ces disjoncteurs.
```

## Laisser l'application Agent en fonctionnement

Laissez l'application agent en fonctionnement car vous l'utiliserez dans le prochain lab pour explorer l'accès sécurisé aux données de l'agent.

*Traduit en utilisant GitHub Copilot.*
