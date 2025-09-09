## Participants à l'événement Microsoft

Les instructions de cette page supposent que vous participez à [Microsoft Event 2025](https://build.microsoft.com/){:target="_blank"} et avez accès à un environnement de lab pré-configuré. Cet environnement fournit un abonnement Azure avec tous les outils et ressources nécessaires pour compléter l'atelier.

## Introduction

Cet atelier est conçu pour vous enseigner le Service d'Agents Azure AI et le [SDK](https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme?context=%2Fazure%2Fai-services%2Fagents%2Fcontext%2Fcontext){:target="_blank"} associé. Il consiste en plusieurs labs, chacun mettant en évidence une fonctionnalité spécifique du Service d'Agents Azure AI. Les labs sont conçus pour être complétés dans l'ordre, car chacun s'appuie sur les connaissances et le travail du lab précédent.

## Sélectionner le langage de programmation de l'atelier

L'atelier est disponible en Python et C#. Assurez-vous de sélectionner le langage qui correspond à la salle de lab dans laquelle vous vous trouvez, en utilisant les onglets de sélection de langage. Note, ne changez pas de langage au milieu de l'atelier.

**Sélectionnez l'onglet de langage qui correspond à votre salle de lab :**

=== "Python"
    Le langage par défaut pour l'atelier est défini à **Python**.
=== "C#"
    Le langage par défaut pour l'atelier est défini à **C#**.

## S'authentifier avec Azure

Vous devez vous authentifier avec Azure pour que l'application agent puisse accéder au Service d'Agents Azure AI et aux modèles. Suivez ces étapes :

1. Ouvrez une fenêtre de terminal. L'application terminal est **épinglée** à la barre des tâches Windows 11.

    ![Ouvrir la fenêtre de terminal](../media/windows-taskbar.png){ width="300" }

2. Exécutez la commande suivante pour vous authentifier avec Azure :

    ```powershell
    az login
    ```

    !!! note
        Il vous sera demandé d'ouvrir un lien de navigateur et de vous connecter à votre compte Azure.

        1. Une fenêtre de navigateur s'ouvrira automatiquement, sélectionnez **Compte professionnel ou scolaire** puis sélectionnez **Continuer**.

        1. Utilisez le **Nom d'utilisateur** et le **Mot de passe** trouvés dans la **section supérieure** de l'onglet **Ressources** dans l'environnement de lab.

        2. Sélectionnez **Oui, toutes les applications**

3. Puis sélectionnez l'abonnement **Par défaut** depuis la ligne de commande, en sélectionnant **Entrée**.

4. Une fois connecté, exécutez la commande suivante pour attribuer le rôle **utilisateur** au groupe de ressources :

    ```powershell
    $subId = $(az account show --query id --output tsv) `
    ;$objectId = $(az ad signed-in-user show --query id -o tsv) `
    ; az role assignment create --role "f6c7c914-8db3-469d-8ca1-694a8f32e121" --assignee-object-id $objectId --scope /subscriptions/$subId/resourceGroups/"rg-agent-workshop" --assignee-principal-type 'User'
    ```

5. Laissez la fenêtre de terminal ouverte pour les étapes suivantes.

## Ouvrir l'atelier

Suivez ces étapes pour ouvrir l'atelier dans Visual Studio Code :

=== "Python"

      1. Depuis la fenêtre de terminal, exécutez les commandes suivantes pour cloner le dépôt de l'atelier, naviguer vers le dossier pertinent, configurer un environnement virtuel, l'activer et installer les packages requis :

          ```powershell
          git clone https://github.com/microsoft/build-your-first-agent-with-azure-ai-agent-service-workshop.git `
          ; cd build-your-first-agent-with-azure-ai-agent-service-workshop `
          ; python -m venv src/python/workshop/.venv `
          ; src\python\workshop\.venv\Scripts\activate `
          ; pip install -r src/python/workshop/requirements.txt `
          ; code --install-extension tomoki1207.pdf
          ```

      2. Ouvrir dans VS Code. Depuis la fenêtre de terminal, exécutez la commande suivante :

          ```powershell
          code .vscode\python-workspace.code-workspace
          ```

        !!! warning "Lorsque le projet s'ouvre dans VS Code, deux notifications apparaissent dans le coin inférieur droit. Cliquez sur ✖ pour fermer les deux notifications."

=== "C#"

    1. Depuis une fenêtre de terminal, exécutez les commandes suivantes pour cloner le dépôt de l'atelier :

        ```powershell
        git clone https://github.com/microsoft/build-your-first-agent-with-azure-ai-agent-service-workshop.git
        ```

    === "VS Code"

        1. Ouvrez l'atelier dans Visual Studio Code. Depuis la fenêtre de terminal, exécutez la commande suivante :

            ```powershell
            code build-your-first-agent-with-azure-ai-agent-service-workshop\.vscode\csharp-workspace.code-workspace
            ```

        !!! note "Lorsque le projet s'ouvre dans VS Code, une notification apparaîtra dans le coin inférieur droit pour installer l'extension C#. Cliquez sur **Installer** pour installer l'extension C#, car cela fournira les fonctionnalités nécessaires pour le développement C#."

    === "Visual Studio 2022"

        1. Ouvrez l'atelier dans Visual Studio 2022. Depuis la fenêtre de terminal, exécutez la commande suivante :

            ```powershell
            start build-your-first-agent-with-azure-ai-agent-service-workshop\src\csharp\workshop\AgentWorkshop.sln
            ```

            !!! note "On pourrait vous demander avec quel programme ouvrir la solution. Sélectionnez **Visual Studio 2022**."

## Point de terminaison du projet Azure AI Foundry

Ensuite, nous nous connectons à Azure AI Foundry pour récupérer le point de terminaison du projet, que l'application agent utilise pour se connecter au Service d'Agents Azure AI.

1. Naviguez vers le site web [Azure AI Foundry](https://ai.azure.com){:target="_blank"}.
2. Sélectionnez **Se connecter** et utilisez le **Nom d'utilisateur** et le **Mot de passe** trouvés dans la **section supérieure** de l'onglet **Ressources** dans l'environnement de lab. Cliquez sur les champs **Nom d'utilisateur** et **Mot de passe** pour remplir automatiquement les détails de connexion.
    ![Identifiants Azure](../media/azure-credentials.png){:width="500"}
3. Lisez l'introduction à Azure AI Foundry et cliquez sur **Compris**.
4. Naviguez vers [Toutes les ressources](https://ai.azure.com/AllResources){:target="_blank"} pour voir la liste des ressources IA qui ont été pré-provisionnées pour vous.
5. Sélectionnez le nom de ressource qui commence par **aip-** de type **Projet**.

    ![Sélectionner le projet](../media/ai-foundry-project.png){:width="500"}

6. Examinez le guide d'introduction et cliquez sur **Fermer**.
7. Depuis le menu latéral **Aperçu**, localisez la section **Points de terminaison et clés** -> **Bibliothèques** -> **Azure AI Foundry**, cliquez sur l'icône **Copier** pour copier le **point de terminaison du projet Azure AI Foundry**.

    ![Copier la chaîne de connexion](../media/project-connection-string.png){:width="500"}

=== "Python"

    ## Configurer l'atelier

    1. Revenez à l'atelier que vous avez ouvert dans VS Code.
    2. **Renommez** le fichier `.env.sample` en `.env`.

        - Sélectionnez le fichier **.env.sample** dans le panneau **Explorateur** de VS Code.
        - Cliquez droit sur le fichier et sélectionnez **Renommer**, ou appuyez sur <kbd>F2</kbd>.
        - Changez le nom du fichier en `.env` et appuyez sur <kbd>Entrée</kbd>.

    3. Collez le **Point de terminaison du projet** que vous avez copié depuis Azure AI Foundry dans le fichier `.env`.

        ```python
        PROJECT_ENDPOINT="<your_project_endpoint>"
        ```

        Votre fichier `.env` devrait ressembler à ceci mais avec votre point de terminaison de projet.

        ```python
        PROJECT_ENDPOINT="<your_project_endpoint>"
        MODEL_DEPLOYMENT_NAME="<your_model_deployment_name>"
        DEV_TUNNEL_URL="<your_dev_tunnel_url>"
        ```

    4. Sauvegardez le fichier `.env`.

    ## Structure du projet

    Assurez-vous de vous familiariser avec les **sous-dossiers** et **fichiers** clés avec lesquels vous travaillerez tout au long de l'atelier.

    5. Le fichier **app.py** : Le point d'entrée de l'application, contenant sa logique principale.
    6. Le fichier **sales_data.py** : La logique de fonction pour exécuter des requêtes SQL dynamiques contre la base de données SQLite.
    7. Le fichier **stream_event_handler.py** : Contient la logique du gestionnaire d'événements pour le streaming de tokens.
    8. Le dossier **shared/files** : Contient les fichiers créés par l'application agent.
    9. Le dossier **shared/instructions** : Contient les instructions transmises au LLM.

    ![Structure des dossiers de lab](../media/project-structure-self-guided-python.png)

=== "C#"

    ## Configurer l'atelier

    1. Ouvrez un terminal et naviguez vers le dossier **src/csharp/workshop/AgentWorkshop.Client**.

        ```powershell
        cd build-your-first-agent-with-azure-ai-agent-service-workshop\src\csharp\workshop\AgentWorkshop.Client
        ```

    2. Ajoutez le **Point de terminaison du projet** que vous avez copié depuis Azure AI Foundry aux secrets utilisateur.

        ```powershell
        dotnet user-secrets set "ConnectionStrings:AiAgentService" "<your_project_endpoint>"
        ```

    3. Ajoutez le **Nom de déploiement du modèle** aux secrets utilisateur.

        ```powershell
        dotnet user-secrets set "Azure:ModelName" "gpt-4o"
        ```

    4. Ajoutez l'**ID de connexion Bing** aux secrets utilisateur pour l'ancrage avec la recherche Bing.

        ```powershell
        $subId = $(az account show --query id --output tsv)
        $rgName = "rg-agent-workshop"
        $aiAccount = "<ai_account_name>" # Remplacez par le nom de compte IA réel
        $aiProject = "<ai_project_name>" # Remplacez par le nom de projet IA réel
        $bingConnectionId = "/subscriptions/$subId/resourceGroups/$rgName/providers/Microsoft.CognitiveServices/accounts/$aiAccount/projects/$aiProject/connections/groundingwithbingsearch"
        dotnet user-secrets set "Azure:BingConnectionId" "$bingConnectionId"
        ```

    ## Structure du projet

    Assurez-vous de vous familiariser avec les **sous-dossiers** et **fichiers** clés avec lesquels vous travaillerez tout au long de l'atelier.

    ### Le dossier workshop

    - Les fichiers **Lab1.cs, Lab2.cs, Lab3.cs** : Le point d'entrée pour chaque lab, contenant sa logique d'agent.
    - Le fichier **Program.cs** : Le point d'entrée de l'application, contenant sa logique principale.
    - Le fichier **SalesData.cs** : La logique de fonction pour exécuter des requêtes SQL dynamiques contre la base de données SQLite.

    ### Le dossier shared

    - Le dossier **files** : Contient les fichiers créés par l'application agent.
    - Le dossier **fonts** : Contient les polices multilingues utilisées par l'Interpréteur de Code.
    - Le dossier **instructions** : Contient les instructions transmises au LLM.

    ![Structure des dossiers de lab](../media/project-structure-self-guided-csharp.png)

## Conseils de pro

!!! tips
    1. Le **Menu Burger** dans le panneau de droite de l'environnement de lab offre des fonctionnalités supplémentaires, y compris la **Vue de fenêtre partagée** et l'option pour terminer le lab. La **Vue de fenêtre partagée** vous permet de maximiser l'environnement de lab en plein écran, optimisant l'espace d'écran. Le panneau **Instructions** et **Ressources** du lab s'ouvrira dans une fenêtre séparée.
    2. Si les instructions du lab sont lentes à défiler dans l'environnement de lab, essayez de copier l'URL des instructions et de l'ouvrir dans **le navigateur local de votre ordinateur** pour une expérience plus fluide.
    3. Si vous avez du mal à voir une image, **cliquez simplement sur l'image pour l'agrandir**.

*Traduit en utilisant GitHub Copilot.*
