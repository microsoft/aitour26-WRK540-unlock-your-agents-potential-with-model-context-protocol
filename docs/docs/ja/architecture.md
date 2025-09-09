## 技術の概観

- **Azure AI Foundry Agent Service**
  LLM駆動エージェントをホスト；ツール（MCPサーバーを含む）を統制；コンテキスト、Code Interpreter、トークンストリーミングを管理；認証、ログ、スケーリングを提供します。
- **MCPサーバー**
  MCP（Model Context Protocol）は、LLMに外部ツール、API、データへの統一インターフェイスを提供するオープンスタンダードです。ツール発見を標準化し（RESTのOpenAPIのように）、ニーズの進化に合わせてツールを更新または交換しやすくすることで、構成性を向上させます。
- **PostgreSQL + pgvector**
  リレーショナルデータと埋め込みを格納；リレーショナル（SQL）とセマンティック（ベクトル）クエリ（pgvectorを介して）の両方をサポートし、SQLとRLSで統制されます。

**組み合わせ：** Agent Serviceがユーザーの意図をルーティング；MCPサーバーがそれらをツール/SQL呼び出しに変換；PostgreSQL+pgvectorがセマンティックおよび分析的な質問に回答します。

## アーキテクチャ（高レベル）

```plaintext
┌─────────────────────┐                         ┌─────────────────┐
│   Zava Agent App    │       stdio/https       │   MCP Server    │
│   (app.py)          │◄───────────────────────►│ (sales_analysis)│
│                     │      MCP Transports     └─────────────────┘
│ ┌─────────────────┐ │                                 │
│ │ Azure AI        │ │                                 ▼
│ │ Agents Service  │ │                         ┌─────────────────┐
│ │ + Streaming     │ │                         │ Azure Database  │
│ │                 │ │                         │ for PostgreSQL  │
│ └─────────────────┘ │                         │   + pgvector    │
└─────────────────────┘                         └─────────────────┘
         │                                              |
         ▼                                              ▼
┌─────────────────────┐                         ┌─────────────────┐
│ Azure OpenAI        │                         │ Zava Sales      │
│ Model Deployments   │                         │ Database with   │
│ - gpt-4o-mini       │                         │ Semantic Search │
│ - text-embedding-3- │                         └─────────────────┘
│   small             │
└─────────────────────┘
```

## MCPサーバーの主要な利点

- **相互運用性** – AIエージェントを最小限のカスタムコードで任意のベンダーのMCP対応ツールに接続。
- **セキュリティフック** – サインイン、権限、アクティビティログを統合。
- **再利用性** – 一度構築すれば、プロジェクト、クラウド、ランタイム間で再利用可能。
- **運用の簡素化** – 単一の契約により、ボイラープレートとメンテナンスを削減。

## 実証されたベストプラクティス

- **非同期API:** エージェントサービスとPostgreSQLは非同期APIを使用；FastAPI/ASP.NET/Streamlitに最適。
- **トークンストリーミング:** UIでの体感遅延を改善。
- **可観測性:** 監視と最適化をサポートする組み込みトレースとメトリクス。
- **データベースセキュリティ:** PostgreSQLは制限されたエージェント権限と行レベルセキュリティ（RLS）でセキュア化され、エージェントを認可されたデータのみに制限。
- **Code Interpreter:** [Azure AI Agents Service Code Interpreter](https://learn.microsoft.com/azure/ai-services/agents/how-to/tools/code-interpreter?view=azure-python-preview&tabs=python&pivots=overview){:target="_blank"}は、LLMが生成したコードを**サンドボックス**環境でオンデマンドで実行し、エージェントのスコープを超えたアクションを防止。

### 拡張性

ワークショップパターンは、Foundryでデータベース+エージェントの指示を更新することで（例：カスタマーサポートに）適応できます。

## DevTunnelアーキテクチャ

ワークショップ環境では、Agent ServiceはAzureで実行されますが、ローカルで実行されているMCPサーバーに接続する必要があります。DevTunnelは、ローカルのMCPサーバーをクラウドベースのAgent Serviceに公開するセキュアなトンネルを作成します。

```plaintext
          Azure Cloud                           Local Development
    ┌─────────────────────┐                  ┌─────────────────────┐
    │   Zava Agent App    │                  │                     │
    │   (Azure-hosted)    │                  │  ┌─────────────────┐│
    │                     │                  │  │   MCP Server    ││
    │ ┌─────────────────┐ │                  │  │ (sales_analysis)││
    │ │ Azure AI        │ │                  │  │ localhost:8000  ││
    │ │ Agents Service  │ │                  │  └─────────────────┘│
    │ └─────────────────┘ │                  │           │         │
    └─────────────────────┘                  │           ▼         │
              │                              │  ┌─────────────────┐│
              │ HTTPS requests               │  │   PostgreSQL    ││
              ▼                              │  │   + pgvector    ││
    ┌─────────────────────┐                  │  └─────────────────┘│
    │   DevTunnel         │                  │                     │
    │   Public Endpoint   │◄─────────────────┼──── Secure Tunnel   │
    │ (*.devtunnels.ms)   │    Port Forward  │                     │
    └─────────────────────┘                  └─────────────────────┘
```

**ワークショップでのDevTunnelの動作:**

1. **ローカル開発**: MCPサーバーを`localhost:8000`でローカル実行
2. **DevTunnelの作成**: DevTunnelが`localhost:8000`に接続されたパブリックHTTPSエンドポイント（例：`https://abc123.devtunnels.ms`）を作成。
3. **Azure統合**: Azure-hosted Agent ServiceがDevTunnelエンドポイントを通してMCPサーバーに接続。
4. **透過的な動作**: エージェントサービスは通常通り動作し、トンネルを通してローカルで実行されているMCPサーバーにアクセスしていることを認識しません。

この設定により以下が可能になります：

- クラウドホスト型AIサービスを使用しながらローカルで開発・デバッグ
- MCPサーバーをAzureにデプロイすることなく現実的なシナリオをテスト
