## Attendre que la Construction du Codespace soit Terminée

Avant de procéder, assurez-vous que votre Codespace ou Dev Container est entièrement construit et prêt. Cela peut prendre plusieurs minutes, selon votre connexion internet et les ressources téléchargées.

## S'Authentifier avec Azure

Authentifiez-vous avec Azure pour permettre à l'application agent d'accéder au Service d'Agents Azure AI et aux modèles. Suivez ces étapes :

1. Confirmez que l'environnement de l'atelier est prêt et ouvert dans VS Code.
2. Depuis VS Code, ouvrez un terminal via **Terminal** > **New Terminal** dans VS Code, puis exécutez :

    ```shell
    az login --use-device-code
    ```

    !!! note
        Vous serez invité à ouvrir un navigateur et à vous connecter à Azure. Copiez le code d'authentification et :

        1. Choisissez votre type de compte et cliquez sur **Suivant**.
        2. Connectez-vous avec vos identifiants Azure.
        3. Collez le code.
        4. Cliquez sur **OK**, puis **Terminé**.

    !!! warning
        Si vous avez plusieurs locataires Azure, spécifiez le bon en utilisant :

        ```shell
        az login --use-device-code --tenant <tenant_id>
        ```

3. Ensuite, sélectionnez l'abonnement approprié depuis la ligne de commande.
4. Laissez la fenêtre de terminal ouverte pour les étapes suivantes.

## Déployer les Ressources Azure

Ce déploiement crée les ressources suivantes dans votre abonnement Azure sous le groupe de ressources **rg-zava-agent-wks-nnnn** :

- Un **hub Azure AI Foundry** nommé **fdy-zava-agent-wks-nnnn**
- Un **projet Azure AI Foundry** nommé **prj-zava-agent-wks-nnnn**
- Deux modèles sont déployés : **gpt-4o-mini** et **text-embedding-3-small**. [Voir les tarifs.](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/){:target="_blank"}

!!! warning "Assurez-vous d'avoir au moins un quota de 120K TPM pour le SKU Global Standard gpt-4o-mini, car l'agent fait des appels fréquents au modèle. Vérifiez votre quota dans le [Centre de Gestion AI Foundry](https://ai.azure.com/managementCenter/quota){:target="_blank"}."

Nous avons fourni un script bash pour automatiser le déploiement des ressources requises pour l'atelier.

### Déploiement Automatisé

Le script `deploy.sh` déploie les ressources dans la région `westus` par défaut. Pour exécuter le script :

```bash
cd infra && ./deploy.sh
```

<!-- !!! note "Sur Windows, exécutez `deploy.ps1` au lieu de `deploy.sh`" -->

### Configuration de l'Atelier

=== "Python"

    #### Configuration des Ressources Azure

    Le script de déploiement génère le fichier **.env**, qui contient les points de terminaison du projet et du modèle, les noms de déploiement du modèle, et la chaîne de connexion Application Insights. Le fichier .env sera automatiquement sauvegardé dans le dossier `src/python/workshop`.
    
    Votre fichier **.env** ressemblera à ce qui suit, mis à jour avec vos valeurs :

    ```python
    PROJECT_ENDPOINT="<votre_point_de_terminaison_projet>"
    GPT_MODEL_DEPLOYMENT_NAME="<votre_nom_déploiement_modèle>"
    EMBEDDING_MODEL_DEPLOYMENT_NAME="<votre_nom_déploiement_modèle_embedding>"
    APPLICATIONINSIGHTS_CONNECTION_STRING="<votre_chaîne_connexion_application_insights>"
    DEV_TUNNEL_URL="<votre_url_dev_tunnel>"
    AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED="true"
    AZURE_OPENAI_ENDPOINT="<votre_point_de_terminaison_azure_openai>"
    ```

    #### Noms des Ressources Azure

    Vous trouverez également un fichier nommé `resources.txt` dans le dossier `workshop`. Ce fichier contient les noms des ressources Azure créées pendant le déploiement.

    Il ressemblera à ce qui suit :

    ```plaintext
    Ressources Azure AI Foundry :
    - Nom du Groupe de Ressources : rg-zava-agent-wks-nnnn
    - Nom du Projet AI : prj-zava-agent-wks-nnnn
    - Nom de la Ressource Foundry : fdy-zava-agent-wks-nnnn
    - Nom d'Application Insights : appi-zava-agent-wks-nnnn
    ```

=== "C#"

    Le script stocke de manière sécurisée les variables du projet en utilisant le Secret Manager pour les [secrets de développement ASP.NET Core](https://learn.microsoft.com/aspnet/core/security/app-secrets){:target="_blank"}.

    Vous pouvez voir les secrets en exécutant la commande suivante après avoir ouvert l'espace de travail C# dans VS Code :

    ```bash
    dotnet user-secrets list
    ```

*Traduit en utilisant GitHub Copilot et GPT-4o.*
