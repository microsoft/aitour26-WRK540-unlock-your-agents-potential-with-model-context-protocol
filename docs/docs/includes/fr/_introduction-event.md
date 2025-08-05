## Participants à l'Événement Microsoft

Les instructions sur cette page supposent que vous participez à [Microsoft Event 2025](https://build.microsoft.com/){:target="_blank"} et avez accès à un environnement de laboratoire pré-configuré. Cet environnement fournit un abonnement Azure avec tous les outils et ressources nécessaires pour compléter l'atelier.

## Introduction

Cet atelier est conçu pour vous enseigner le Service d'Agents Azure AI et le [SDK](https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme?context=%2Fazure%2Fai-services%2Fagents%2Fcontext%2Fcontext){:target="_blank"} associé. Il consiste en plusieurs laboratoires, chacun mettant en évidence une fonctionnalité spécifique du Service d'Agents Azure AI. Les laboratoires sont destinés à être complétés dans l'ordre, car chacun s'appuie sur les connaissances et le travail du laboratoire précédent.

## Sélectionner le Langage de Programmation de l'Atelier

L'atelier est disponible en Python et C#. Veuillez vous assurer de sélectionner le langage qui correspond à la salle de laboratoire dans laquelle vous vous trouvez, en utilisant les onglets de sélection de langage. Note, ne changez pas de langage en cours d'atelier.

**Sélectionnez l'onglet de langage qui correspond à votre salle de laboratoire :**

=== "Python"
    Le langage par défaut pour l'atelier est défini sur **Python**.
=== "C#"
    Le langage par défaut pour l'atelier est défini sur **C#**.

## S'Authentifier avec Azure

Vous devez vous authentifier avec Azure pour que l'application agent puisse accéder au Service d'Agents Azure AI et aux modèles. Suivez ces étapes :

1. Ouvrez une fenêtre de terminal. L'application terminal est **épinglée** à la barre des tâches Windows 11.

    ![Ouvrir la fenêtre de terminal](../media/windows-taskbar.png){ width="300" }

2. Exécutez la commande suivante pour vous authentifier avec Azure :

    ```powershell
    az login
    ```

    !!! note
        Vous serez invité à ouvrir un lien de navigateur et à vous connecter à votre compte Azure.

        1. Une fenêtre de navigateur s'ouvrira automatiquement, sélectionnez **Compte professionnel ou scolaire** et cliquez sur **Suivant**.

        1. Utilisez le **Nom d'utilisateur** et le **Mot de passe** trouvés dans la **section supérieure** de l'onglet **Ressources** dans l'environnement de laboratoire.

        2. Sélectionnez **OK**, puis **Terminé**.

3. Ensuite, sélectionnez l'abonnement **Par défaut** depuis la ligne de commande, en cliquant sur **Entrée**.

4. Une fois connecté, exécutez la commande suivante pour assigner le rôle **utilisateur** au groupe de ressources :

    ```powershell
    $subId = $(az account show --query id --output tsv) `
    ;$objectId = $(az ad signed-in-user show --query id -o tsv) `
    ; az role assignment create --role "f6c7c914-8db3-469d-8ca1-694a8f32e121" --assignee-object-id $objectId --scope /subscriptions/$subId/resourceGroups/"rg-agent-workshop" --assignee-principal-type 'User'
    ```

5. Laissez la fenêtre de terminal ouverte pour les étapes suivantes.

## Ouvrir l'Atelier

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

        !!! warning "Quand le projet s'ouvre dans VS Code, deux notifications apparaissent dans le coin inférieur droit. Cliquez sur ✖ pour fermer les deux notifications."

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

        !!! note "Quand le projet s'ouvre dans VS Code, une notification apparaîtra dans le coin inférieur droit pour installer l'extension C#. Cliquez sur **Installer** pour installer l'extension C#, car cela fournira les fonctionnalités nécessaires pour le développement C#."

    === "Visual Studio 2022"

        1. Ouvrez l'atelier dans Visual Studio 2022. Depuis la fenêtre de terminal, exécutez la commande suivante :

            ```powershell
            start build-your-first-agent-with-azure-ai-agent-service-workshop\src\csharp\workshop\AgentWorkshop.sln
            ```

            !!! note "Il se peut qu'on vous demande avec quel programme ouvrir la solution. Sélectionnez **Visual Studio 2022**."

## Point de Terminaison du Projet Azure AI Foundry

Ensuite, nous nous connectons à Azure AI Foundry pour récupérer le point de terminaison du projet, que l'application agent utilise pour se connecter au Service d'Agents Azure AI.

1. Naviguez vers le site web [Azure AI Foundry](https://ai.azure.com){:target="_blank"}.
2. Sélectionnez **Se connecter** et utilisez le **Nom d'utilisateur** et le **Mot de passe** trouvés dans la **section supérieure** de l'onglet **Ressources** dans l'environnement de laboratoire. Cliquez sur les champs **Nom d'utilisateur** et **Mot de passe** pour remplir automatiquement les détails de connexion.
    ![Identifiants Azure](../media/azure-credentials.png){:width="500"}
3. Lisez l'introduction à Azure AI Foundry et cliquez sur **Compris**.
4. Naviguez vers [Toutes les Ressources](https://ai.azure.com/AllResources){:target="_blank"} pour voir la liste des ressources IA qui ont été pré-provisionnées pour vous.
5. Sélectionnez le nom de ressource qui commence par **aip-** de type **Projet**.

    ![Sélectionner le projet](../media/ai-foundry-project.png){:width="500"}

6. Examinez le guide d'introduction et cliquez sur **Fermer**.
7. Depuis le menu latéral **Vue d'ensemble**, localisez la section **Points de terminaison et clés** -> **Bibliothèques** -> **Azure AI Foundry**, cliquez sur l'icône **Copier** pour copier le **point de terminaison du projet Azure AI Foundry**.

    ![Copier la chaîne de connexion](../media/project-connection-string.png){:width="500"}

=== "Python"

    ## Configurer l'Atelier

    1. Revenez à l'atelier que vous avez ouvert dans VS Code.
    2. **Renommez** le fichier `.env.sample` en `.env`.

        - Sélectionnez le fichier **.env.sample** dans le panneau **Explorateur** de VS Code.
        - Cliquez droit sur le fichier et sélectionnez **Renommer**, ou appuyez sur <kbd>F2</kbd>.
        - Changez le nom du fichier en `.env` et appuyez sur <kbd>Entrée</kbd>.

    3. Collez le **Point de terminaison du projet** que vous avez copié depuis Azure AI Foundry dans le fichier `.env`.

        ```python
        PROJECT_ENDPOINT="<votre_point_de_terminaison_projet>"
        ```

        Votre fichier `.env` devrait ressembler à ceci mais avec votre point de terminaison de projet.

        ```python
        PROJECT_ENDPOINT="<votre_point_de_terminaison_projet>"
        MODEL_DEPLOYMENT_NAME="<votre_nom_déploiement_modèle>"
        DEV_TUNNEL_URL="<votre_url_dev_tunnel>"
        ```

    4. Sauvegardez le fichier `.env`.

    ## Structure du Projet

    Assurez-vous de vous familiariser avec les **sous-dossiers** et **fichiers** clés avec lesquels vous travaillerez tout au long de l'atelier.

    5. Le fichier **app.py** : Le point d'entrée de l'application, contenant sa logique principale.
    6. Le fichier **sales_data.py** : La logique de fonction pour exécuter des requêtes SQL dynamiques contre la base de données SQLite.
    7. Le fichier **stream_event_handler.py** : Contient la logique du gestionnaire d'événements pour le streaming de tokens.
    8. Le dossier **shared/files** : Contient les fichiers créés par l'application agent.
    9. Le dossier **shared/instructions** : Contient les instructions transmises au LLM.

    ![Structure des dossiers du laboratoire](../media/project-structure-self-guided-python.png)

=== "C#"

    ## Configurer l'Atelier

    1. Ouvrez un terminal et naviguez vers le dossier **src/csharp/workshop/AgentWorkshop.Client**.

        ```powershell
        cd build-your-first-agent-with-azure-ai-agent-service-workshop\src\csharp\workshop\AgentWorkshop.Client
        ```

    2. Ajoutez le **Point de terminaison du projet** que vous avez copié depuis Azure AI Foundry aux secrets utilisateur.

        ```powershell
        dotnet user-secrets set "ConnectionStrings:AiAgentService" "<votre_point_de_terminaison_projet>"
        ```

    3. Ajoutez le **Nom de déploiement du modèle** aux secrets utilisateur.

        ```powershell
        dotnet user-secrets set "Azure:ModelName" "gpt-4o"
        ```

    4. Ajoutez l'**ID de connexion Bing** aux secrets utilisateur pour l'ancrage avec la recherche Bing.

        ```powershell
        $subId = $(az account show --query id --output tsv)
        $rgName = "rg-agent-workshop"
        $aiAccount = "<nom_compte_ai>" # Remplacez par le nom réel du compte AI
        $aiProject = "<nom_projet_ai>" # Remplacez par le nom réel du projet AI
        $bingConnectionId = "/subscriptions/$subId/resourceGroups/$rgName/providers/Microsoft.CognitiveServices/accounts/$aiAccount/projects/$aiProject/connections/groundingwithbingsearch"
        dotnet user-secrets set "Azure:BingConnectionId" "$bingConnectionId"
        ```

    ## Structure du Projet

    Assurez-vous de vous familiariser avec les **sous-dossiers** et **fichiers** clés avec lesquels vous travaillerez tout au long de l'atelier.

*Traduit en utilisant GitHub Copilot et GPT-4o.*
