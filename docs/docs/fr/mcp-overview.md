MCP (Model Context Protocol) est un standard ouvert qui permet aux agents IA d'accéder aux outils externes, APIs et sources de données via une interface unifiée. Il standardise la découverte et l'accès aux outils, similaire à OpenAPI pour les services REST. MCP améliore la composabilité et l'agilité des systèmes IA en simplifiant les mises à jour ou remplacements d'outils IA à mesure que vos besoins métier évoluent.

# Avantages Clés

- **Interopérabilité** – Connectez les agents IA aux outils compatibles MCP de n'importe quel fournisseur avec un code personnalisé minimal.  
- **Crochets de sécurité** – Intégrez la connexion, les permissions et la journalisation d'activité.  
- **Réutilisabilité** – Construisez une fois, réutilisez à travers les projets, clouds et runtimes.  
- **Simplicité opérationnelle** – Un contrat unique réduit le code générique et la maintenance.

# Architecture

```
┌─────────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Agent Azure AI    │    │   Client MCP    │    │   Serveur MCP   │
│   (main.py)         │◄──►│ (mcp_client.py) │◄──►│ (mcp_server_sales_analysis.py) │
│                     │    └─────────────────┘    └─────────────────┘
│ ┌─────────────────┐ │                                   │
│ │ Service         │ │                                   ▼
│ │ Agents Azure AI │ │                           ┌─────────────────┐
│ │ + Streaming     │ │                           │ Azure Database  │
│ │                 │ │                           │ for PostgreSQL  │
│ └─────────────────┘ │                           │       +         │
└─────────────────────┘                           │    pgvector     │
         │                                        └─────────────────┘
         ▼                                                │
┌─────────────────────┐                           ┌─────────────────┐
│ Déploiement Modèle  │                           │ 8 Tables        │
│ Azure OpenAI        │                           │ Normalisées     │
│ (GPT-4, etc.)       │                           │ avec Index de   │
└─────────────────────┘                           │ Performance     │
                                                  └─────────────────┘
```

# Comment Ça Fonctionne

MCP utilise un modèle client-serveur pour les interactions d'agents IA avec les ressources externes :

- **Hôte MCP :** Runtime ou plateforme exécutant l'agent IA (par exemple, Service d'Agent Azure AI Foundry).  
- **Client MCP :** SDK convertissant les appels d'outils d'agent IA en requêtes MCP.  
- **Serveur MCP :** Enregistre les outils, exécute les requêtes, retourne des résultats JSON. Prend en charge l'authentification, l'autorisation et la journalisation.

### Composants sur le Serveur MCP

- **Ressources :** Sources de données comme les bases de données, APIs, magasins de fichiers.  
- **Outils :** Fonctions ou APIs enregistrées exécutées à la demande.  
- **Prompts (optionnel) :** Modèles versionnés pour la réutilisation.  
- **Politiques (optionnel) :** Limites et vérifications de sécurité (taux, profondeur, authentification).

### Transports MCP

- **HTTP/HTTPS :** Protocoles web standards avec support de streaming.  
- **stdio :** Transport léger local ou conteneurisé partageant le runtime.

Cet atelier utilise stdio pour la communication MCP locale. Les déploiements de production utilisent HTTPS pour l'évolutivité et la sécurité.

# Cas d'Usage

Dans cet atelier, le serveur MCP relie l'Agent Azure AI aux données de vente de Zava. Quand vous posez des questions sur les produits, ventes ou inventaire :

1. L'agent IA génère des requêtes Serveur MCP.  
2. Le Serveur MCP :  
    - Fournit des informations de schéma pour des requêtes précises.  
    - Exécute des requêtes SQL, retourne des données structurées.  
    - Offre des services de temps pour les rapports sensibles au temps.

Cela permet des insights en temps réel sur les opérations de vente de Zava de manière efficace.

*Traduit en utilisant GitHub Copilot et GPT-4o.*
