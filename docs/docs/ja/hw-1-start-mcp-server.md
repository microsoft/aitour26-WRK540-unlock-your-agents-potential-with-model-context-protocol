## 学習内容

このラボでは、以下を行います：

- DevTunnel を使用してローカル MCP サーバーをクラウドベースのエージェントサービスからアクセス可能にする
- Model Context Protocol を使った実践的実験のための環境設定

## はじめに

Model Context Protocol（MCP）サーバーは、大規模言語モデル（LLM）と外部ツールおよびデータソース間の通信を処理する重要なコンポーネントです。MCP サーバーをローカルマシンで実行しますが、Azure AI Foundry エージェントサービスは接続するためにインターネットアクセスが必要です。ローカル MCP サーバーをインターネットからアクセス可能にするために、DevTunnel を使用します。これにより、エージェントサービスは MCP サーバーが Azure でサービスとして実行されているかのように通信できます。

## MCP のインターフェースオプション

MCP は LLM とツールを接続するための2つの主要インターフェースをサポートします：

- **Streamable HTTP Transport**: ウェブベースの API とサービス用。
- **Stdio Transport**: ローカルスクリプトとコマンドラインツール用。

このラボでは、Azure AI Foundry エージェントサービスと統合するために Streamable HTTP トランスポートインターフェースを使用します。

!!! note
    通常は本番環境で MCP サーバーをデプロイしますが、このワークショップでは開発環境でローカルに実行します。これにより、完全なデプロイを必要とせずに MCP ツールをテストし対話できます。

### MCP サーバー用の DevTunnel を起動

1. 新しいターミナルで、DevTunnel を認証します。Azure アカウントでのログインが求められますので、Azure AI Foundry エージェントサービスまたは Azure ポータルへのログインに使用したのと同じアカウントを使用してください。次のコマンドを実行します：

    ```bash
    devtunnel login
    ```

1. 次に、MCP サーバーが実行されているターミナルで、以下を実行して DevTunnel を開始します：

    ```bash
    devtunnel host -p 8000 --allow-anonymous
    ```

    これにより、エージェントが MCP サーバーに接続するために必要な URL が出力されます。出力は次のようになります：

    ```text
    Hosting port: 8000
    Connect via browser: https://<tunnel-id>-8000.aue.devtunnels.ms
    Inspect network activity: https://<tunnel-id>-8000-inspect.aue.devtunnels.ms
    ```

## DevTunnel 環境変数の更新

1. **Connect via browser** URL をクリップボードにコピーします - 次のラボでエージェントを設定するために必要です。
2. workshop フォルダーの `.env` ファイルを開きます。
3. `DEV_TUNNEL_URL` 変数をコピーした URL で更新します。

    ```text
    DEV_TUNNEL_URL=https://<tunnel-id>-8000.aue.devtunnels.ms
    ```

## エージェントアプリの開始

1. 以下のテキストをクリップボードにコピーします：

    ```text
    Debug: Select and Start Debugging
    ```

2. <kbd>F1</kbd> を押して VS Code コマンドパレットを開きます。
3. テキストをコマンドパレットに貼り付け、**Debug: Select and Start Debugging** を選択します。
4. リストから **🌎🤖Debug Compound: Agent and MCP (http)** を選択します。これによりエージェントアプリとウェブチャットクライアントが開始されます。

## エージェントとの会話開始

ブラウザーの **Web Chat** タブに切り替えます。エージェントアプリが実行され、質問を受け付ける準備ができていることが確認できるはずです。

### DevTunnel でのデバッグ

DevTunnel を使用して MCP サーバーとエージェントアプリをデバッグできます。これにより、ネットワークアクティビティを検査し、リアルタイムで問題をトラブルシューティングできます。

1. DevTunnel 出力から **Inspect network activity** URL を選択します。
2. これにより、MCP サーバーとエージェントアプリのネットワークアクティビティを確認できる新しいタブがブラウザーで開きます。
3. これを使用してワークショップ中に発生する問題をデバッグできます。

また、特定の問題をデバッグするために MCP サーバーコードとエージェントアプリコードにブレークポイントを設定することもできます。これを行うには：

1. `mcp_server` フォルダーの `sales_analysis.py` ファイルを開きます。
2. 実行を一時停止したい行番号の横の余白をクリックしてブレークポイントを設定します。
3. 実行がブレークポイントに到達すると、変数の検査、コードのステップ実行、デバッグコンソールでの式の評価を行うことができます。

*GitHub Copilot を使用して翻訳されました。*
