## ソリューションアーキテクチャ

このワークショップでは、Zava Sales Agent を作成します：Zava の小売 DIY ビジネスの売上データに関する質問に答え、チャートを生成し、製品推薦を提供し、画像ベースの製品検索をサポートする会話型エージェントです。

## エージェントアプリのコンポーネント

1. **Microsoft Azure サービス**

    このエージェントは Microsoft Azure サービス上に構築されています。

      - **生成 AI モデル**: このアプリを支える基盤 LLM は [Azure OpenAI gpt-4o-mini](https://learn.microsoft.com/azure/ai-foundry/openai/concepts/models?tabs=global-standard%2Cstandard-chat-completions#how-do-i-access-the-gpt-4o-and-gpt-4o-mini-models){:target="_blank"} LLM です。

      - **コントロールプレーン**: アプリとそのアーキテクチャコンポーネントは、ブラウザからアクセス可能な [Azure AI Foundry](https://ai.azure.com){:target="_blank"} ポータルを使用して管理・監視されます。

2. **Azure AI Foundry (SDK)**

    ワークショップは Azure AI Foundry SDK を使用して [Python](https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme?view=azure-python-preview&context=%2Fazure%2Fai-services%2Fagents%2Fcontext%2Fcontext){:target="_blank"} で提供されます。SDK は [Code Interpreter](https://learn.microsoft.com/azure/ai-services/agents/how-to/tools/code-interpreter?view=azure-python-preview&tabs=python&pivots=overview){:target="_blank"} と [Model Context Protocol (MCP)](https://modelcontextprotocol.io/){:target="_blank"} 統合を含む Azure AI Agents サービスの主要機能をサポートします。

3. **データベース**

    アプリは Zava Sales Database によって駆動されます。これは Zava の小売 DIY 運営の包括的な売上データを含む pgvector 拡張機能付きの [Azure Database for PostgreSQL flexible server](https://www.postgresql.org/){:target="_blank"} です。

    データベースは売上、在庫、顧客データの複雑なクエリをサポートします。行レベルセキュリティ（RLS）により、エージェントは割り当てられた店舗のみにアクセスできます。

4. **MCP Server**

    Model Context Protocol (MCP) サーバーは、エージェントと PostgreSQL データベース間のブリッジとして機能するカスタム Python サービスです。以下を処理します：

     - **データベーススキーマ発見**: エージェントが利用可能なデータを理解するためにデータベーススキーマを自動的に取得します。
     - **クエリ生成**: 自然言語リクエストを SQL クエリに変換します。
     - **ツール実行**: SQL クエリを実行し、エージェントが使用できる形式で結果を返します。
     - **時刻サービス**: 時間に敏感なレポート生成のための時刻関連データを提供します。

## ワークショップソリューションの拡張

ワークショップは、データベースを更新し Foundry Agent Service の指示をカスタマイズすることで、カスタマーサポートなどの用途に簡単に適応できます。

## アプリで実証されたベストプラクティス

このアプリは効率性とユーザーエクスペリエンスのためのベストプラクティスも実証しています。

- **非同期 API**:
  ワークショップサンプルでは、Foundry Agent Service と PostgreSQL の両方が非同期 API を使用し、リソース効率とスケーラビリティを最適化しています。この設計選択は、FastAPI、ASP.NET、Streamlit などの非同期 Web フレームワークでアプリケーションをデプロイする際に特に有利になります。

- **トークンストリーミング**:
  LLM を活用したエージェントアプリの認識応答時間を短縮することでユーザーエクスペリエンスを向上させるために、トークンストリーミングが実装されています。

- **可観測性**:
  アプリには、エージェントのパフォーマンス、使用パターン、レイテンシを監視するための組み込み[トレーシング](https://learn.microsoft.com/azure/ai-foundry/agents/concepts/tracing){:target="_blank"}と[メトリクス](https://learn.microsoft.com/azure/ai-foundry/agents/how-to/metrics){:target="_blank"}が含まれています。これにより、問題を特定し、時間をかけてエージェントを最適化できます。

*Translated using GitHub Copilot and GPT-4o.*
