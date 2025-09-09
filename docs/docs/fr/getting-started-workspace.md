Il y a deux espaces de travail VS Code dans l'atelier, un pour Python et un pour C#. L'espace de travail contient le code source et tous les fichiers nécessaires pour compléter les labs pour chaque langage. Choisissez l'espace de travail qui correspond au langage avec lequel vous souhaitez travailler.

=== "Python"

    1. **Copiez** le chemin suivant dans le presse-papiers :

        ```text
        /workspace/.vscode/python-workspace.code-workspace
        ```
    1. Dans le menu VS Code, sélectionnez **Fichier** puis **Ouvrir l'espace de travail depuis un fichier**.
    3. Remplacez et **collez** le nom de chemin copié et sélectionnez **OK**.


    ## Structure du projet

    Familiarisez-vous avec les **dossiers** et **fichiers** clés dans l'espace de travail avec lequel vous travaillerez tout au long de l'atelier.

    ### Le dossier "workshop"

    - Le fichier **app.py** : Le point d'entrée de l'application, contenant sa logique principale.

    Notez la variable **INSTRUCTIONS_FILE**—elle définit quel fichier d'instructions l'agent utilise. Vous mettrez à jour cette variable dans un lab ultérieur.

    - Le fichier **resources.txt** : Contient les ressources utilisées par l'application agent.
    - Le fichier **.env** : Contient les variables d'environnement utilisées par l'application agent.

    ### Le dossier "mcp_server"

    - Le fichier **sales_analysis.py** : Le serveur MCP avec des outils pour l'analyse des ventes.

    ### Le dossier "shared/instructions"

    - Le dossier **instructions** : Contient les instructions transmises au LLM.

    ![Structure des dossiers de lab](media/project-structure-self-guided-python.png)

=== "C#"

    1. Dans Visual Studio Code, allez à **Fichier** > **Ouvrir l'espace de travail depuis un fichier**.
    2. Remplacez le chemin par défaut par le suivant :

        ```text
        /workspace/.vscode/csharp-workspace.code-workspace
        ```

    3. Sélectionnez **OK** pour ouvrir l'espace de travail.

    ## Structure du projet

    Le projet utilise [Aspire](http://aka.ms/dotnet-aspire) pour simplifier la construction de l'application agent, la gestion du serveur MCP et l'orchestration de toutes les dépendances externes. La solution est composée de quatre projets, tous préfixés par `McpAgentWorkshop` :

    * `AppHost` : L'orchestrateur Aspire et projet de lancement pour l'atelier.
    * `McpServer` : Le projet serveur MCP.
    * `ServiceDefaults` : Configuration par défaut pour les services, comme la journalisation et la télémétrie.
    * `WorkshopApi` : L'API Agent pour l'atelier. La logique principale de l'application se trouve dans la classe `AgentService`.

    En plus des projets .NET dans la solution, il y a un dossier `shared` (visible comme un Dossier de Solution, et via l'explorateur de fichiers), qui contient :

    * `instructions` : Les instructions transmises au LLM.
    * `scripts` : Scripts shell d'aide pour diverses tâches, ceux-ci seront référencés lorsque nécessaire.
    * `webapp` : L'application client front-end. Note : Il s'agit d'une application Python, dont Aspire gérera le cycle de vie.

    ![Structure des dossiers de lab](media/project-structure-self-guided-csharp.png)

*Traduit en utilisant GitHub Copilot.*
