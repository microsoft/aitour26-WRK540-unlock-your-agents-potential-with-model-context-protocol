## Ce que vous allez apprendre

Dans ce lab, vous allez :

- Utiliser DevTunnel pour rendre votre serveur MCP local accessible aux services d'agent basés dans le cloud
- Configurer votre environnement pour l'expérimentation pratique avec le Model Context Protocol

## Introduction

Le serveur Model Context Protocol (MCP) est un composant crucial qui gère la communication entre les Large Language Models (LLM) et les outils et sources de données externes. Vous exécuterez le serveur MCP sur votre machine locale, mais le Service d'Agent Azure AI Foundry nécessite un accès internet pour s'y connecter. Pour rendre votre serveur MCP local accessible depuis internet, vous utiliserez un DevTunnel. Cela permet au Service d'Agent de communiquer avec votre serveur MCP comme s'il s'exécutait en tant que service dans Azure.

## Options d'interface pour MCP

MCP prend en charge deux interfaces principales pour connecter les LLM avec les outils :

- **Transport HTTP en streaming** : Pour les API et services web.
- **Transport Stdio** : Pour les scripts locaux et outils en ligne de commande.

Ce lab utilise l'interface de transport HTTP en streaming pour s'intégrer avec le Service d'Agent Azure AI Foundry.

!!! note
    Normalement, vous déploieriez le serveur MCP dans un environnement de production, mais pour cet atelier, vous l'exécuterez localement dans votre environnement de développement. Cela vous permet de tester et d'interagir avec les outils MCP sans avoir besoin d'un déploiement complet.

### Démarrer un DevTunnel pour le serveur MCP

1. Dans un nouveau terminal, authentifiez DevTunnel. Il vous sera demandé de vous connecter avec votre compte Azure, utilisez le même compte que vous avez utilisé pour vous connecter au Service d'Agent Azure AI Foundry ou au Portail Azure. Exécutez la commande suivante :

    ```bash
    devtunnel login
    ```

1. Ensuite, dans le terminal où le serveur MCP s'exécute, démarrez un DevTunnel en exécutant :

    ```bash
    devtunnel host -p 8000 --allow-anonymous
    ```

    Cela produira une URL dont vous aurez besoin pour que l'agent se connecte au serveur MCP. La sortie sera similaire à :

    ```text
    Hosting port: 8000
    Connect via browser: https://<tunnel-id>-8000.aue.devtunnels.ms
    Inspect network activity: https://<tunnel-id>-8000-inspect.aue.devtunnels.ms
    ```

## Mettre à jour la variable d'environnement DevTunnel

1. Copiez l'URL **Connect via browser** dans le presse-papiers - vous en aurez besoin dans le prochain lab pour configurer l'agent.
2. Ouvrez le fichier `.env` dans le dossier workshop.
3. Mettez à jour la variable `DEV_TUNNEL_URL` avec l'URL copiée.

    ```text
    DEV_TUNNEL_URL=https://<tunnel-id>-8000.aue.devtunnels.ms
    ```

## Démarrer l'application Agent

1. Copiez le texte ci-dessous dans le presse-papiers :

    ```text
    Debug: Select and Start Debugging
    ```

2. Appuyez sur <kbd>F1</kbd> pour ouvrir la Palette de Commandes VS Code.
3. Collez le texte dans la Palette de Commandes et sélectionnez **Debug: Select and Start Debugging**.
4. Sélectionnez **🌎🤖Debug Compound: Agent and MCP (http)** dans la liste. Cela démarrera l'application agent et le client de chat web.

## Commencer une conversation avec l'Agent

Basculez vers l'onglet **Web Chat** dans votre navigateur. Vous devriez voir l'application agent en cours d'exécution et prête à accepter des questions.

### Débogage avec DevTunnel

Vous pouvez utiliser DevTunnel pour déboguer le serveur MCP et l'application agent. Cela vous permet d'inspecter l'activité réseau et de résoudre les problèmes en temps réel.

1. Sélectionnez l'URL **Inspect network activity** de la sortie DevTunnel.
2. Cela ouvrira un nouvel onglet dans votre navigateur où vous pourrez voir l'activité réseau du serveur MCP et de l'application agent.
3. Vous pouvez utiliser cela pour déboguer tout problème qui survient pendant l'atelier.

Vous pouvez également définir des points d'arrêt dans le code du serveur MCP et le code de l'application agent pour déboguer des problèmes spécifiques. Pour ce faire :

1. Ouvrez le fichier `sales_analysis.py` dans le dossier `mcp_server`.
2. Définissez un point d'arrêt en cliquant dans la gouttière à côté du numéro de ligne où vous voulez suspendre l'exécution.
3. Lorsque l'exécution atteint le point d'arrêt, vous pouvez inspecter les variables, parcourir le code étape par étape et évaluer des expressions dans la Console de Débogage.

*Traduit en utilisant GitHub Copilot.*
