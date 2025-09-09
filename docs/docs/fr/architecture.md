## Technologies principales en un coup d'œil

- **Service d'Agent Azure AI Foundry**
  Héberge l'agent piloté par LLM ; orchestre les outils (y compris les serveurs MCP) ; gère le contexte, l'interpréteur de code et le streaming de tokens ; et fournit l'authentification, la journalisation et la mise à l'échelle.
- **Serveurs MCP**
  MCP (Model Context Protocol) est un standard ouvert qui donne aux LLM une interface unifiée vers les outils externes, les API et les données. Il standardise la découverte d'outils (comme OpenAPI pour REST) et améliore la composabilité en rendant les outils faciles à mettre à jour ou échanger selon l'évolution des besoins.
- **PostgreSQL + pgvector**
  Stocke les données relationnelles et les embeddings ; prend en charge les requêtes relationnelles (SQL) et sémantiques (vectorielles) (via pgvector), gouvernées par SQL et RLS.

**Ensemble :** le Service d'Agent route les intentions utilisateur ; le serveur MCP les traduit en appels d'outils/SQL ; PostgreSQL+pgvector répond aux questions sémantiques et analytiques.

## Architecture (haut niveau)

```plaintext
┌─────────────────────┐                         ┌─────────────────┐
│   App Agent Zava    │       stdio/https       │   Serveur MCP   │
│   (app.py)          │◄───────────────────────►│ (sales_analysis)│
│                     │    Transports MCP       └─────────────────┘
│ ┌─────────────────┐ │                                 │
│ │ Service         │ │                                 ▼
│ │ Agents Azure AI │ │                         ┌─────────────────┐
│ │ + Streaming     │ │                         │ Base de données │
│ │                 │ │                         │ Azure pour      │
│ └─────────────────┘ │                         │ PostgreSQL      │
└─────────────────────┘                         │   + pgvector    │
         │                                       └─────────────────┘
         ▼                                              |
┌─────────────────────┐                         ┌─────────────────┐
│ Azure OpenAI        │                         │ Base de données │
│ Déploiements de     │                         │ de ventes Zava  │
│ modèles             │                         │ avec recherche  │
│ - gpt-4o-mini       │                         │ sémantique      │
│ - text-embedding-3- │                         └─────────────────┘
│   small             │
└─────────────────────┘
```

## Avantages clés des serveurs MCP

- **Interopérabilité** – Connectez les agents IA aux outils compatibles MCP de n'importe quel fournisseur avec un code personnalisé minimal.
- **Hooks de sécurité** – Intégrez la connexion, les permissions et la journalisation des activités.
- **Réutilisabilité** – Construisez une fois, réutilisez dans tous les projets, clouds et environnements d'exécution.
- **Simplicité opérationnelle** – Un seul contrat réduit le code répétitif et la maintenance.

## Meilleures pratiques démontrées

- **APIs asynchrones :** Le service d'agents et PostgreSQL utilisent des APIs async ; idéal avec FastAPI/ASP.NET/Streamlit.
- **Streaming de tokens :** Améliore la latence perçue dans l'interface utilisateur.
- **Observabilité :** Support intégré de traçage et de métriques pour le monitoring et l'optimisation.
- **Sécurité de base de données :** PostgreSQL est sécurisé avec des privilèges d'agent restreints et la sécurité au niveau des lignes (RLS), limitant les agents aux seules données autorisées.
- **Interpréteur de code :** L'[Interpréteur de code du Service d'Agents Azure AI](https://learn.microsoft.com/azure/ai-services/agents/how-to/tools/code-interpreter?view=azure-python-preview&tabs=python&pivots=overview){:target="_blank"} exécute le code généré par LLM à la demande dans un environnement **sandboxé**, empêchant les actions au-delà de la portée de l'agent.

### Extensibilité

Le modèle d'atelier peut être adapté (ex : support client) en mettant à jour la base de données + les instructions d'agent dans Foundry.

## Architecture DevTunnel

Dans l'environnement de l'atelier, le Service d'Agent s'exécute dans Azure mais doit se connecter à votre serveur MCP qui s'exécute localement. DevTunnel crée un tunnel sécurisé qui expose votre serveur MCP local au Service d'Agent basé dans le cloud.

```plaintext
         Cloud Azure                            Développement Local
    ┌─────────────────────┐                  ┌─────────────────────┐
    │   App Agent Zava    │                  │                     │
    │   (Hébergé Azure)   │                  │  ┌─────────────────┐│
    │                     │                  │  │   Serveur MCP   ││
    │ ┌─────────────────┐ │                  │  │ (sales_analysis)││
    │ │ Service         │ │                  │  │ localhost:8000  ││
    │ │ Agents Azure AI │ │                  │  └─────────────────┘│
    │ └─────────────────┘ │                  │           │         │
    └─────────────────────┘                  │           ▼         │
              │                              │  ┌─────────────────┐│
              │ Requêtes HTTPS               │  │   PostgreSQL    ││
              ▼                              │  │   + pgvector    ││
    ┌─────────────────────┐                  │  └─────────────────┘│
    │   DevTunnel         │                  │                     │
    │   Point d'accès     │◄─────────────────┼──── Tunnel sécurisé │
    │   public            │  Redirection     │                     │
    │ (*.devtunnels.ms)   │  de port         │                     │
    └─────────────────────┘                  └─────────────────────┘
```

**Comment DevTunnel fonctionne dans l'atelier :**

1. **Développement local** : Vous exécutez le serveur MCP localement sur `localhost:8000`
2. **Création DevTunnel** : DevTunnel crée un point d'accès HTTPS public (ex : `https://abc123.devtunnels.ms`) connecté à `localhost:8000`.
3. **Intégration Azure** : Le Service d'Agent hébergé sur Azure se connecte au serveur MCP via le point d'accès DevTunnel.
4. **Opération transparente** : Le service d'agent fonctionne normalement, sans savoir qu'il accède au serveur MCP qui s'exécute localement via un tunnel.

Cette configuration vous permet de :

- Développer et déboguer localement tout en utilisant des services IA hébergés dans le cloud
- Tester des scénarios réalistes sans déployer le serveur MCP sur Azure

*Traduit en utilisant GitHub Copilot.*
