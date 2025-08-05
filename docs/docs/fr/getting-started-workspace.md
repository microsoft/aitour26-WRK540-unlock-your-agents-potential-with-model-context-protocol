## Ouvrir l'Espace de Travail du Langage

Il y a deux espaces de travail dans l'atelier, un pour Python et un pour C#. L'espace de travail contient le code source et tous les fichiers nécessaires pour compléter les laboratoires pour chaque langage. Choisissez l'espace de travail qui correspond au langage avec lequel vous voulez travailler.

=== "Python"

    1. Copiez la commande suivante dans votre presse-papiers :

        ```text
        File: Open Workspace from File...
        ```
    2. Basculez vers Visual Studio Code, appuyez sur <kbd>F1</kbd> pour ouvrir la Palette de Commandes.
    3. Collez la commande dans la Palette de Commandes et sélectionnez **Open Workspace from File...**.
    4. Copiez et collez le chemin suivant dans le sélecteur de fichiers et appuyez sur <kbd>Entrée</kbd> :

        ```text
        /workspace/.vscode/python-workspace.code-workspace
        ```

    ## Structure du Projet

    Assurez-vous de vous familiariser avec les **dossiers** et **fichiers** clés avec lesquels vous travaillerez tout au long de l'atelier.

    ### Le dossier workshop

    - Le fichier **app.py** : Le point d'entrée de l'application, contenant sa logique principale.
  
    Notez la variable **INSTRUCTIONS_FILE**—elle définit quel fichier d'instructions l'agent utilise. Vous mettrez à jour cette variable dans un laboratoire ultérieur.

    - Le fichier **resources.txt** : Contient les ressources utilisées par l'application agent.
    - Le fichier **.env** : Contient les variables d'environnement utilisées par l'application agent.

    ### Le dossier mcp_server

    - Le fichier **sales_analysis.py** : Le Serveur MCP avec des outils pour l'analyse des ventes.

    ### Le dossier shared

    - Le dossier **instructions** : Contient les instructions transmises au LLM.

    ![Structure des dossiers du laboratoire](media/project-structure-self-guided-python.png)

=== "C#"

    1. Dans Visual Studio Code, allez dans **File** > **Open Workspace from File**.
    2. Remplacez le chemin par défaut par le suivant :

        ```text
        /workspace/.vscode/csharp-workspace.code-workspace
        ```

    3. Sélectionnez **OK** pour ouvrir l'espace de travail.

    ## Structure du Projet

    Assurez-vous de vous familiariser avec les **dossiers** et **fichiers** clés avec lesquels vous travaillerez tout au long de l'atelier.

    ### Le dossier workshop

    - Les fichiers **Lab1.cs, Lab2.cs, Lab3.cs** : Le point d'entrée pour chaque laboratoire, contenant sa logique d'agent.
    - Le fichier **Program.cs** : Le point d'entrée de l'application, contenant sa logique principale.
    - Le fichier **SalesData.cs** : La logique de fonction pour exécuter des requêtes SQL dynamiques contre la base de données SQLite.

    ### Le dossier shared

    - Le dossier **files** : Contient les fichiers créés par l'application agent.
    - Le dossier **fonts** : Contient les polices multilingues utilisées par l'Interpréteur de Code.
    - Le dossier **instructions** : Contient les instructions transmises au LLM.

    ![Structure des dossiers du laboratoire](media/project-structure-self-guided-csharp.png)

*Traduit en utilisant GitHub Copilot et GPT-4o.*
