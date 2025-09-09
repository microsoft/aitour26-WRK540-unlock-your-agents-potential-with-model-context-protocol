## Ce que vous allez apprendre

Dans ce lab, vous sécuriserez les données de l'agent en utilisant le Model Context Protocol (MCP) et la sécurité au niveau des lignes PostgreSQL (RLS). L'agent a un accès en lecture seule à la base de données et les données sont protégées par des rôles d'utilisateur (siège social et directeur de magasin) pour s'assurer que seuls les utilisateurs autorisés peuvent accéder aux informations spécifiques.

## Introduction

La base de données PostgreSQL utilise la sécurité au niveau des lignes (RLS) pour contrôler l'accès aux données par rôle d'utilisateur. Le client de chat web utilise par défaut le rôle `Siège social` (accès complet aux données), mais passer au rôle `Directeur de magasin` restreint l'accès aux données spécifiques au rôle uniquement.

Le serveur MCP fournit à l'agent l'accès à la base de données Zava. Lorsque le service d'agent traite les demandes des utilisateurs, le rôle utilisateur (UUID) est transmis au serveur MCP via les en-têtes de ressources des outils MCP pour s'assurer que la sécurité basée sur les rôles est appliquée.

En fonctionnement normal, un directeur de magasin s'authentifierait avec l'agent et son rôle d'utilisateur serait défini en conséquence. Mais c'est un atelier, et nous allons sélectionner manuellement un rôle.

??? info "Pour les développeurs : Comment fonctionne la sécurité au niveau des lignes PostgreSQL ?"

    ### Aperçu de la sécurité RLS PostgreSQL

    La sécurité au niveau des lignes (RLS) filtre automatiquement les lignes de base de données basé sur les permissions utilisateur. Cela permet à plusieurs utilisateurs de partager les mêmes tables de base de données tout en ne voyant que les données qu'ils sont autorisés à accéder.
    
    Dans ce système, les utilisateurs du siège social voient toutes les données de tous les magasins, tandis que les directeurs de magasin sont restreints à voir uniquement les informations de leur propre magasin. L'exemple ci-dessous montre comment les politiques RLS sont implémentées pour la table `retail.orders`, avec des politiques identiques appliquées aux tables `retail.order_items`, `retail.inventory`, et `retail.customers`.

    ```sql
    CREATE POLICY store_manager_orders ON retail.orders
    FOR ALL TO PUBLIC
    USING (
        -- Le siège social voit toutes les données
        current_setting('app.current_rls_user_id', true) = '00000000-0000-0000-0000-000000000000'
        OR
        -- Les directeurs de magasin ne voient que les données de leur magasin
        EXISTS (SELECT 1 FROM retail.stores s WHERE s.store_id = retail.orders.store_id 
                AND s.rls_user_id::text = current_setting('app.current_rls_user_id', true))
    );
    ```

    **Résultat :** Les directeurs de magasin ne voient que les données de leur magasin, tandis que le siège social voit tout - le tout en utilisant la même base de données et les mêmes tables.

    === "Python"

        Vous trouverez le code responsable de définir le rôle utilisateur dans le fichier `workshop/chat_manager.py`.

        ```python
        if request.rls_user_id:
            # Create dynamic tool resources with RLS user ID header
            mcp_tool_resource = MCPToolResource(
                server_label="ZavaSalesAnalysisMcpServer",
                headers={"x-rls-user-id": request.rls_user_id},
                require_approval="never",
            )
            tool_resources.mcp = [mcp_tool_resource]
        ```

        Le code pour récupérer l'ID utilisateur RLS se trouve dans `mcp_server/sales_analysis/sales_analysis.py`. Si le serveur ne détecte pas l'en-tête RLS, il utilise par défaut le rôle Siège social. Cette solution de repli est destinée uniquement à l'usage de l'atelier et ne devrait pas être appliquée en production.

        ```python
        def get_rls_user_id(ctx: Context) -> str:
            """Get the Row Level Security User ID from the request context."""

            rls_user_id = get_header(ctx, "x-rls-user-id")
            if rls_user_id is None:
                # Default to a placeholder if not provided
                rls_user_id = "00000000-0000-0000-0000-000000000000"
            return rls_user_id
        ```

    === "C#"

        Vous trouverez le code responsable de définir le rôle utilisateur sur les requêtes au serveur MCP dans la classe `AgentService`.

        ```csharp
        var mcpToolResource = new MCPToolResource(ZavaMcpToolLabel, new Dictionary<string, string>
        {
            { "x-rls-user-id", request.RlsUserId }
        });
        var toolResources = new ToolResources();
        toolResources.Mcp.Add(mcpToolResource);
        ```

        La `MCPToolResource` est ensuite ajoutée à la collection `ToolResources`, qui est fournie à l'exécution en streaming en utilisant la propriété `CreateRunStreamingOptions.ToolResources`, c'est parce que l'ID utilisateur RLS est une valeur dynamique du client (différents utilisateurs "connectés" peuvent avoir différents ID), nous devons nous assurer qu'il est défini sur l'_exécution_ du thread plutôt que lorsque l'agent est créé.

        Comme l'ID utilisateur RLS est défini comme un en-tête pour que l'agent le transmette au serveur MCP, ceci est accessible depuis le `HttpContext` sur la requête, qui peut être accessible depuis un `IHttpContextAccessor`, qui est injecté dans les méthodes d'outils MCP. Une méthode d'extension a été créée, `HttpContextAccessorExtensions.GetRequestUserId`, qui peut être utilisée dans un outil :

        ```csharp
        public async Task<string> ExecuteSalesQueryAsync(
            NpgsqlConnection connection,
            ILogger<SalesTools> logger,
            IHttpContextAccessor httpContextAccessor,
            [Description("A well-formed PostgreSQL query.")] string query
        )
        {
            ...

            var rlsUserId = httpContextAccessor.GetRequestUserId();

            ...
        }
        ```

    ### Définir l'ID utilisateur RLS Postgres

    Maintenant que le serveur MCP a l'ID utilisateur RLS, il doit être défini sur la connexion PostgreSQL.

    === "Python"

        La solution Python définit l'ID utilisateur RLS sur chaque connexion PostgreSQL en appelant `set_config()` dans la méthode `execute_query` dans `mcp_server/sales_analysis/sales_analysis_postgres.py`.

        ```python
        ...
        conn = await self.get_connection()
        await conn.execute("SELECT set_config('app.current_rls_user_id', $1, false)", rls_user_id)

        rows = await conn.fetch(sql_query)
        ...
        ```

    === "C#"

        La solution C# définit l'ID utilisateur RLS sur la connexion PostgreSQL en exécutant une commande SQL pour définir la variable de contexte RLS immédiatement après l'ouverture de la connexion dans la méthode `ExecuteSalesQueryAsync` dans `SalesTools.cs`.

        ```csharp
        ...
        await using var cmd = new NpgsqlCommand("SELECT set_config('app.current_rls_user_id', @rlsUserId, false)", connection);
        cmd.Parameters.AddWithValue("rlsUserId", rlsUserId ?? string.Empty);
        await cmd.ExecuteNonQueryAsync();

        await using var queryCmd = new NpgsqlCommand(query, connection);
        await using var reader = await queryCmd.ExecuteReaderAsync();
        ...
        ```

## Exercice de lab

### Rôle Siège social

Par défaut, le client web fonctionne avec le rôle `Siège social`, qui a un accès complet à toutes les données.

1. Entrez la requête suivante dans le chat :

   ```text
   Montre les ventes par magasin
   ```

   Vous verrez que les données de tous les magasins sont retournées. Parfait.

### Sélectionner un rôle Directeur de magasin

1. Revenez à l'onglet Web Chat de l'Agent dans votre navigateur.
2. Sélectionnez l'icône `paramètres` dans le coin supérieur droit de la page.
3. Sélectionnez un `Emplacement de magasin` dans le menu déroulant.
4. Sélectionnez `Sauvegarder` et maintenant l'agent fonctionnera avec les permissions d'accès aux données de l'emplacement de magasin sélectionné.

   ![](../media/select_store_manager_role.png)

Maintenant l'agent n'aura accès qu'aux données pour l'emplacement de magasin sélectionné.

!!! info "Note"
    Changer l'utilisateur réinitialisera la session de chat, car le contexte est lié à l'utilisateur.

Essayez la requête suivante :

```text
Montre les ventes par magasin
```

Vous remarquerez que l'agent ne retourne que les données pour l'emplacement de magasin sélectionné. Cela démontre comment l'accès aux données de l'agent est restreint basé sur le rôle de directeur de magasin sélectionné.

![](../media/select_seattle_store_role.png)

*Traduit en utilisant GitHub Copilot.*
