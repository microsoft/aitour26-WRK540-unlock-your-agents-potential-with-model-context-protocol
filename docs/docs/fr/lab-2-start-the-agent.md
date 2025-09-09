## Ce que vous allez apprendre

Dans ce lab, vous activerez l'Interpréteur de Code pour analyser les données de vente et créer des graphiques en utilisant le langage naturel.

## Introduction

Dans ce lab, vous étendrez l'Agent Azure AI avec deux outils :

- **Interpréteur de Code :** Permet à l'agent de générer et d'exécuter du code Python pour l'analyse de données et la visualisation.
- **Outils de serveur MCP :** Permettent à l'agent d'accéder aux sources de données externes en utilisant les outils MCP, dans notre cas les données dans une base de données PostgreSQL.

## Exercice de lab

### Activer l'Interpréteur de Code et le serveur MCP

Dans ce lab, vous activerez deux outils puissants qui fonctionnent ensemble : l'Interpréteur de Code (qui exécute le code Python généré par l'IA pour l'analyse de données et la visualisation) et le Serveur MCP (qui fournit un accès sécurisé aux données de vente de Zava stockées dans PostgreSQL).

=== "Python"

    1. **Ouvrez** le fichier `app.py`.
    2. **Faites défiler vers la ligne 50 environ** et trouvez la ligne qui ajoute l'Interpréteur de Code et les outils MCP au jeu d'outils de l'agent. Ces lignes sont actuellement commentées avec un `#` au début.
    3. **Décommentez** les lignes suivantes :

        ```python
        
        # code_interpreter = CodeInterpreterTool()
        # self.toolset.add(code_interpreter)
        
        # mcp_tools = McpTool(
        #     server_label="ZavaSalesAnalysisMcpServer",
        #     server_url=Config.DEV_TUNNEL_URL,
        #     allowed_tools=[
        #         "get_multiple_table_schemas",
        #         "execute_sales_query",
        #         "get_current_utc_date",
        #         "semantic_search_products",
        #     ],
        # )

        # mcp_tools.set_approval_mode("never")  # No human in the loop
        # self.toolset.add(mcp_tools)
        ```

        !!! info "Que fait ce code ?"
            - **Interpréteur de Code** : Permet à l'agent d'exécuter du code Python pour l'analyse de données et la visualisation.
            - **Outils de serveur MCP** : Fournit l'accès aux sources de données externes avec des outils autorisés spécifiques et aucune approbation humaine requise. Pour les applications de production, considérez l'activation de l'autorisation humaine dans la boucle pour les opérations sensibles.

    4. **Examinez** le code que vous avez décommenté. Le code devrait ressembler exactement à ceci :

        ```python

        Après avoir décommenté, votre code devrait ressembler à ceci :

        ```python
        class AgentManager:
            """Manages Azure AI Agent lifecycle and dependencies."""

            async def _setup_agent_tools(self) -> None:
                """Setup MCP tools and code interpreter."""
                logger.info("Setting up Agent tools...")
                self.toolset = AsyncToolSet()

                code_interpreter = CodeInterpreterTool()
                self.toolset.add(code_interpreter)

                mcp_tools = McpTool(
                    server_label="ZavaSalesAnalysisMcpServer",
                    server_url=Config.DEV_TUNNEL_URL,
                    allowed_tools=[
                        "get_multiple_table_schemas",
                        "execute_sales_query",
                        "get_current_utc_date",
                        "semantic_search_products",
                    ],
                )

                mcp_tools.set_approval_mode("never")  # No human in the loop
                self.toolset.add(mcp_tools)
        ```

    ## Démarrer l'application Agent

    1. Copiez le texte ci-dessous dans le presse-papiers :

    ```text
    Debug: Select and Start Debugging
    ```

    1. Appuyez sur <kbd>F1</kbd> pour ouvrir la Palette de Commandes VS Code.
    1. Collez le texte dans la Palette de Commandes et sélectionnez **Debug: Select and Start Debugging**.
    1. Sélectionnez **🌎🤖Debug Compound: Agent and MCP (http)** dans la liste. Cela démarrera l'application agent et le client de chat web.

    Ceci démarre les processus suivants :

    1.  Tâche DevTunnel (workshop)
    2.  Web Chat (workshop)
    3.  Agent Manager (workshop)
    4.  MCP Server (workshop)

    Dans VS Code, vous verrez ces processus s'exécuter dans le panneau TERMINAL.

    ![L'image montre les processus en cours d'exécution dans le panneau TERMINAL de VS Code](../media/vs-code-processes.png)

    ## Ouvrir le client de chat web de l'agent

    === "@Participants à l'événement"

        Sélectionnez le lien suivant pour ouvrir l'application Web Chat dans le navigateur.

        [Ouvrir Web Chat](http://localhost:8005){:target="_blank"}

    === "Apprenants auto-guidés"

        ## Rendre le port 8005 public

        Vous devez rendre le port 8005 public pour pouvoir accéder au client de chat web dans votre navigateur.

        1. Sélectionnez l'onglet **Ports** dans le panneau inférieur de VS Code.
        2. Cliquez droit sur le port **Web Chat App (8005)** et sélectionnez **Port Visibility**.
        3. Sélectionnez **Public**.

        ![](../media/make-port-public.png)


        ## Ouvrir le client de chat web dans le navigateur

        1.  Copiez le texte ci-dessous dans le presse-papiers :

        ```text
        Open Port in Browser
        ```

        2.  Appuyez sur <kbd>F1</kbd> pour ouvrir la Palette de Commandes VS Code.
        3.  Collez le texte dans la Palette de Commandes et sélectionnez **Open Port in Browser**.
        4.  Sélectionnez **8005** dans la liste. Cela ouvrira le client de chat web de l'agent dans votre navigateur.

    ![](../media/agent_web_chat.png)

=== "C#"

    1. **Ouvrez** `AgentService.cs` depuis le dossier `Services` du projet `McpAgentWorkshop.WorkshopApi`.
    2. Naviguez vers la méthode `InitialiseAgentAsync`.
    3. **Décommentez** les lignes suivantes :

        ```csharp
        // var mcpTool = new MCPToolDefinition(
        //     ZavaMcpToolLabel,
        //     devtunnelUrl + "mcp");

        // var codeInterpreterTool = new CodeInterpreterToolDefinition();

        // IEnumerable<ToolDefinition> tools = [mcpTool, codeInterpreterTool];

        // persistentAgent = await persistentAgentsClient.Administration.CreateAgentAsync(
        //         name: AgentName,
        //         model: configuration.GetValue<string>("MODEL_DEPLOYMENT_NAME"),
        //         instructions: instructionsContent,
        //         temperature: modelTemperature,
        //         tools: tools);

        // logger.LogInformation("Agent created with ID: {AgentId}", persistentAgent.Id);
        ```

    ## Démarrer l'application Agent

    4. Appuyez sur <kbd>F1</kbd> pour ouvrir la Palette de Commandes VS Code.
    5. Sélectionnez **Debug Aspire** comme configuration de lancement.

    Une fois le débogueur lancé, une fenêtre de navigateur s'ouvrira avec le tableau de bord Aspire. Une fois que toutes les ressources ont démarré, vous pouvez lancer l'application web de l'atelier en cliquant sur le lien **Workshop Frontend**.

    ![Tableau de bord Aspire](../media//lab-2-start-agent-aspire-dashboard.png)

    !!! tip "Dépannage"
        Si le navigateur ne se charge pas, essayez d'actualiser la page de force (Ctrl + F5 ou Cmd + Shift + R). S'il ne se charge toujours pas, référez-vous au [guide de dépannage](./dotnet-troubleshooting.md).

## Commencer une conversation avec l'agent

Depuis le client de chat web, vous pouvez commencer une conversation avec l'agent. L'agent est conçu pour répondre aux questions sur les données de vente de Zava et générer des visualisations en utilisant l'Interpréteur de Code.

1.  Analyse des ventes de produits. Copiez et collez la question suivante dans le chat :

    ```text
    Montre les 10 meilleurs produits par revenus par magasin pour le dernier trimestre
    ```

    Après un moment, l'agent répondra avec un tableau montrant les 10 meilleurs produits par revenus pour chaque magasin.

    !!! info
        L'agent utilise le LLM pour appeler trois outils de serveur MCP pour récupérer les données et les afficher dans un tableau :

        1. **get_current_utc_date()** : Obtient la date et l'heure actuelles pour que l'agent puisse déterminer le dernier trimestre par rapport à la date actuelle.
        2. **get_multiple_table_schemas()** : Obtient les schémas des tables dans la base de données requises par le LLM pour générer un SQL valide.
        3. **execute_sales_query** : Exécute une requête SQL pour récupérer les 10 meilleurs produits par revenus pour le dernier trimestre depuis la base de données PostgreSQL.

    !!! tip
        === "Python"

            Revenez à VS Code et sélectionnez **MCP Server (workspace)** dans le panneau TERMINAL et vous verrez les appels effectués au serveur MCP par le Service d'Agent Azure AI Foundry.

            ![](../media/mcp-server-in-action.png)

        === "C#"

            Dans le tableau de bord Aspire, vous pouvez sélectionner les logs pour la ressource `dotnet-mcp-server` pour voir les appels effectués au serveur MCP par le Service d'Agent Azure AI Foundry.

            Vous pouvez également ouvrir la vue de trace et trouver la trace de bout en bout de l'application, depuis l'entrée utilisateur dans le chat web, jusqu'aux appels d'agent et appels d'outils MCP.

            ![Aperçu des traces](../media/lab-7-trace-overview.png)

2.  Générer un graphique circulaire. Copiez et collez la question suivante dans le chat :

    ```text
    Montre les ventes par magasin sous forme de graphique circulaire pour cette année financière
    ```

    L'agent répondra avec un graphique circulaire montrant la distribution des ventes par magasin pour l'année financière actuelle.

    !!! info
        Cela peut sembler magique, alors que se passe-t-il en coulisses pour que tout fonctionne ?

        Le Service d'Agent Foundry orchestre les étapes suivantes :

        1. Comme la question précédente, l'agent détermine s'il a les schémas de table requis pour la requête. Sinon, il utilise les outils **get_multiple_table_schemas()** pour obtenir la date actuelle et le schéma de base de données.
        2. L'agent utilise ensuite l'outil **execute_sales_query** pour récupérer les ventes
        3. En utilisant les données retournées, le LLM écrit du code Python pour créer un graphique circulaire.
        4. Finalement, l'Interpréteur de Code exécute le code Python pour générer le graphique.

3.  Continuez à poser des questions sur les données de vente Zava pour voir l'Interpréteur de Code en action. Voici quelques questions de suivi que vous pourriez essayer :

    - `Détermine quels produits ou catégories stimulent les ventes. Montre sous forme de graphique à barres.`
    - `Quel serait l'impact d'un événement de choc (par ex., une baisse de 20% des ventes dans une région) sur la distribution globale des ventes ? Montre sous forme de graphique à barres groupées.`
      - Suivi avec `Et si l'événement de choc était de 50% ?`
    - `Quelles régions ont des ventes au-dessus ou en-dessous de la moyenne ? Montre sous forme de graphique à barres avec déviation de la moyenne.`
    - `Quelles régions ont des remises au-dessus ou en-dessous de la moyenne ? Montre sous forme de graphique à barres avec déviation de la moyenne.`
    - `Simule les ventes futures par région en utilisant une simulation Monte Carlo pour estimer les intervalles de confiance. Montre sous forme de ligne avec bandes de confiance utilisant des couleurs vives.`

<!-- ## Arrêter l'application Agent

1. Revenez à l'éditeur VS Code.
1. Appuyez sur <kbd>Shift + F5</kbd> pour arrêter l'application agent. -->

## Laisser l'application Agent en fonctionnement

Laissez l'application agent en fonctionnement car vous l'utiliserez dans le prochain lab pour étendre l'agent avec plus d'outils et de capacités.

*Traduit en utilisant GitHub Copilot.*
