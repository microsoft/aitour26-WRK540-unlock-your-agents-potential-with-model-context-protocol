## Ce que vous apprendrez

Dans ce laboratoire, vous activerez l'Interpréteur de Code pour analyser les données de vente et créer des graphiques en utilisant le langage naturel.

## Introduction

Dans ce laboratoire, vous étendrez l'Agent IA Azure avec deux outils :

- **Interpréteur de Code :** Permet à l'agent de générer et d'exécuter du code Python pour l'analyse de données et la visualisation.
- **Outils du Serveur MCP :** Permettent à l'agent d'accéder aux sources de données externes en utilisant les Outils MCP, dans notre cas des données dans une base de données PostgreSQL.

## Exercice de Laboratoire

### Activer l'Interpréteur de Code et le Serveur MCP

Dans ce laboratoire, vous activerez deux outils puissants qui travaillent ensemble : l'Interpréteur de Code (qui exécute du code Python généré par IA pour l'analyse de données et la visualisation) et le Serveur MCP (qui fournit un accès sécurisé aux données de vente de Zava stockées dans PostgreSQL).

=== "Python"

    1. **Ouvrez** le fichier `app.py`.
    2. **Faites défiler jusqu'à la ligne 67** et trouvez les lignes qui ajoutent l'outil Interpréteur de Code et les outils du Serveur MCP au jeu d'outils de l'agent. Ces lignes sont actuellement commentées avec des caractères **# plus espace** au début.
    3. **Décommentez** les lignes suivantes :

        !!! warning "L'indentation compte en Python !"
            Lors du décommentage, supprimez à la fois le symbole `#` ET l'espace qui le suit. Cela garantit que le code maintient une indentation Python appropriée et s'aligne correctement avec le code environnant.

        ```python
        # self.toolset.add(code_interpreter_tool)
        # self.toolset.add(mcp_server_tools)
        ```

        !!! info "Que fait ce code ?"
            - **Outil Interpréteur de Code** : Permet à l'agent d'exécuter du code Python pour l'analyse de données et la visualisation.
            - **Outils du Serveur MCP** : Fournit l'accès aux sources de données externes avec des outils spécifiques autorisés et aucune approbation humaine requise. Pour les applications de production, considérez l'activation de l'autorisation humaine dans la boucle pour les opérations sensibles.

    4. **Examinez** le code que vous avez décommenté. Le code devrait ressembler exactement à ceci :

        Après décommentage, votre code devrait ressembler à ceci :

        ```python
        async def _setup_agent_tools(self) -> None:
            """Setup MCP tools and code interpreter."""
            logger.info("Setting up Agent tools...")
            self.toolset = AsyncToolSet()

            code_interpreter_tool = CodeInterpreterTool()

            mcp_server_tools = McpTool(
                server_label="ZavaSalesAnalysisMcpServer",
                server_url=Config.DEV_TUNNEL_URL,
                allowed_tools=[
                    "get_multiple_table_schemas",
                    "execute_sales_query",
                    "get_current_utc_date",
                    "semantic_search_products",
                ],
            )
            mcp_server_tools.set_approval_mode("never")  # No human in the loop

            self.toolset.add(code_interpreter_tool)
            self.toolset.add(mcp_server_tools)
        ```

    ## Démarrer l'Application de l'Agent

    1. Copiez le texte ci-dessous dans le presse-papiers :

    ```text
    Debug: Select and Start Debugging
    ```

    1. Appuyez sur <kbd>F1</kbd> pour ouvrir la Palette de Commandes de VS Code.
    1. Collez le texte dans la Palette de Commandes et sélectionnez **Debug: Select and Start Debugging**.
    1. Sélectionnez **🌎🤖Debug Compound: Agent and MCP (http)** dans la liste. Cela démarrera l'application de l'agent et le client de chat web.

    Cela démarre les processus suivants :

    1.  DevTunnel (workshop) Task
    2.  Web Chat (workshop)
    3.  Agent Manager (workshop)
    4.  MCP Server (workshop)

    Dans VS Code, vous verrez ceux-ci s'exécuter dans le panneau TERMINAL.

    ![L'image montre les processus en cours d'exécution dans le panneau TERMINAL de VS Code](../media/vs-code-processes.png)

    ## Ouvrir le Client de Chat Web de l'Agent

    === "@Participants à l'Événement"

        Sélectionnez le lien suivant pour ouvrir l'application de Chat Web dans le navigateur.

        [Ouvrir Chat Web](http://localhost:8005){:target="_blank"}

    === "Apprenants Auto-guidés"

        ## Rendre le Port 8005 Public

        Vous devez rendre public le port 8005 pour pouvoir accéder au client de chat web dans votre navigateur.

        1. Sélectionnez l'onglet **Ports** dans le panneau inférieur de VS Code.
        2. Faites un clic droit sur le port **Web Chat App (8005)** et sélectionnez **Port Visibility**.
        3. Sélectionnez **Public**.

        ![](../media/make-port-public.png)


        ## Ouvrir le Client de Chat Web dans le Navigateur

        1.  Copiez le texte ci-dessous dans le presse-papiers :

        ```text
        Open Port in Browser
        ```

        2.  Appuyez sur <kbd>F1</kbd> pour ouvrir la Palette de Commandes de VS Code.
        3.  Collez le texte dans la Palette de Commandes et sélectionnez **Open Port in Browser**.
        4.  Sélectionnez **8005** dans la liste. Cela ouvrira le client de chat web de l'agent dans votre navigateur.

    ![](../media/agent_web_chat.png)

=== "C#"

    1. **Ouvrez** `AgentService.cs` du dossier `Services` du projet `McpAgentWorkshop.WorkshopApi`.
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

    ## Démarrer l'Application de l'Agent

    4. Appuyez sur <kbd>F1</kbd> pour ouvrir la Palette de Commandes de VS Code.
    5. Sélectionnez **Debug Aspire** comme configuration de lancement.

    Une fois le débogueur lancé, une fenêtre de navigateur s'ouvrira avec le tableau de bord Aspire. Une fois que toutes les ressources ont démarré, vous pouvez lancer l'application web de l'atelier en cliquant sur le lien **Workshop Frontend**.

    ![Tableau de bord Aspire](../media//lab-2-start-agent-aspire-dashboard.png)

    !!! tip "Dépannage"
        Si le navigateur ne se charge pas, essayez de rafraîchir la page de force (Ctrl + F5 ou Cmd + Shift + R). Si cela ne se charge toujours pas, consultez le [guide de dépannage](./dotnet-troubleshooting.md).

## Démarrer une Conversation avec l'Agent

Depuis le client de chat web, vous pouvez démarrer une conversation avec l'agent. L'agent est conçu pour répondre aux questions sur les données de vente de Zava et générer des visualisations en utilisant l'Interpréteur de Code.

1.  Analyse des ventes de produits. Copiez et collez la question suivante dans le chat :

    ```text
    Show the top 10 products by revenue by store for the last quarter
    ```

    Après un moment, l'agent répondra avec un tableau montrant les 10 produits principaux par revenus pour chaque magasin.

    !!! info
        L'agent utilise le LLM qui appelle trois outils du Serveur MCP pour récupérer les données et les afficher dans un tableau :

        1. **get_current_utc_date()** : Obtient la date et l'heure actuelles pour que l'agent puisse déterminer le dernier trimestre par rapport à la date actuelle.
        2. **get_multiple_table_schemas()** : Obtient les schémas des tables dans la base de données requis par le LLM pour générer du SQL valide.
        3. **execute_sales_query** : Exécute une requête SQL pour récupérer les 10 produits principaux par revenus pour le dernier trimestre depuis la base de données PostgreSQL.

    !!! tip
        === "Python"

            Revenez à VS Code et sélectionnez **MCP Server (workspace)** dans le panneau TERMINAL et vous verrez les appels effectués au Serveur MCP par le Service d'Agent Azure AI Foundry.

            ![](../media/mcp-server-in-action.png)

        === "C#"

            Dans le tableau de bord Aspire, vous pouvez sélectionner les journaux pour la ressource `dotnet-mcp-server` pour voir les appels effectués au Serveur MCP par le Service d'Agent Azure AI Foundry.

            Vous pouvez également ouvrir la vue de trace et trouver la trace de bout en bout de l'application, de l'entrée utilisateur dans le chat web, jusqu'aux appels d'agent et aux appels d'outils MCP.

            ![Aperçu de la trace](../media/lab-7-trace-overview.png)

2.  Générer un graphique en secteurs. Copiez et collez la question suivante dans le chat :

    ```text
    Show sales by store as a pie chart for this financial year
    ```

    L'agent répondra avec un graphique en secteurs montrant la distribution des ventes par magasin pour l'année fiscale actuelle.

    !!! info
        Cela peut sembler magique, alors que se passe-t-il en coulisses pour que tout fonctionne ?

        Le Service d'Agent Foundry orchestre les étapes suivantes :

        1. Comme pour la question précédente, l'agent détermine s'il dispose des schémas de table requis pour la requête. Si ce n'est pas le cas, il utilise les outils **get_multiple_table_schemas()** pour obtenir la date actuelle et le schéma de la base de données.
        2. L'agent utilise ensuite l'outil **execute_sales_query** pour récupérer les ventes
        3. En utilisant les données retournées, le LLM écrit du code Python pour créer un Graphique en Secteurs.
        4. Enfin, l'Interpréteur de Code exécute le code Python pour générer le graphique.

3.  Continuez à poser des questions sur les données de vente de Zava pour voir l'Interpréteur de Code en action. Voici quelques questions de suivi que vous pourriez vouloir essayer :

    - `Determine which products or categories drive sales. Show as a Bar Chart.`
    - `What would be the impact of a shock event (e.g., 20% sales drop in one region) on global sales distribution? Show as a Grouped Bar Chart.`
      - Suivi avec `What if the shock event was 50%?`
    - `Which regions have sales above or below the average? Show as a Bar Chart with Deviation from Average.`
    - `Which regions have discounts above or below the average? Show as a Bar Chart with Deviation from Average.`
    - `Simulate future sales by region using a Monte Carlo simulation to estimate confidence intervals. Show as a Line with Confidence Bands using vivid colors.`

<!-- ## Stop the Agent App

1. Switch back to the VS Code editor.
1. Press <kbd>Shift + F5</kbd> to stop the agent app. -->

## Laisser l'Application de l'Agent en Cours d'Exécution

Laissez l'application de l'agent en cours d'exécution car vous l'utiliserez dans le prochain laboratoire pour étendre l'agent avec plus d'outils et de capacités.

*Traduit en utilisant GitHub Copilot.*
