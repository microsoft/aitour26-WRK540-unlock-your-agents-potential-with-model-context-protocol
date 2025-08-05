## 学習内容

このラボでは、以下を行います：

- DevTunnel を使用してローカル MCP サーバーをクラウドベースのエージェントサービスからアクセス可能にする
- Model Context Protocol の実践的な実験のための環境をセットアップする

## はじめに

Model Context Protocol (MCP) サーバーは、大規模言語モデル（LLM）と外部ツールやデータソース間の通信を処理する重要なコンポーネントです。MCP サーバーをローカルマシンで実行しますが、Azure AI Foundry Agent Service がそれに接続するにはインターネットアクセスが必要です。ローカル MCP サーバーをインターネットからアクセス可能にするために、DevTunnel を使用します。これにより、Agent Service は MCP サーバーが Azure のサービスとして実行されているかのように通信できます。

## MCP のインターフェースオプション

MCP は、LLM とツールを接続するための2つの主要なインターフェースをサポートします：

- **Streamable HTTP Transport**: Web ベースの API とサービス用。
- **Stdio Transport**: ローカルスクリプトとコマンドラインツール用。

このラボでは、Azure AI Foundry Agent Service との統合に Streamable HTTP トランスポートインターフェースを使用します。

!!! note
    通常は、本番環境で MCP サーバーをデプロイしますが、このワークショップでは開発環境でローカルに実行します。これにより、完全なデプロイメントを必要とせずに MCP ツールをテストし、対話できます。

### MCP Server 用の DevTunnel を起動する

1. 新しいターミナルで、DevTunnel を認証します。Azure アカウントでのログインを求められますので、Azure AI Foundry Agent Service または Azure Portal へのログインに使用したものと同じアカウントを使用してください。次のコマンドを実行します：

    ```bash
    devtunnel login
    ```

1. 次に、MCP サーバーが実行されているターミナルで、以下を実行して DevTunnel を開始します：

    ```bash
    devtunnel host -p 8000 --allow-anonymous
    ```

    これにより、エージェントが MCP サーバーに接続するために必要な URL が出力されます。出力は以下のようになります：

    ```text
    Hosting port: 8000
    Connect via browser: https://<tunnel-id>-8000.aue.devtunnels.ms
    Inspect network activity: https://<tunnel-id>-8000-inspect.aue.devtunnels.ms
    ```

## DevTunnel 環境変数を更新する

1. **Connect via browser** URL をクリップボードにコピーします - エージェントを設定するための次のラボで必要になります。
2. workshop フォルダの `.env` ファイルを開きます。
3. コピーした URL で `DEV_TUNNEL_URL` 変数を更新します。

    ```text
    DEV_TUNNEL_URL=https://<tunnel-id>-8000.aue.devtunnels.ms
    ```

## エージェントアプリを開始する

1. 以下のテキストをクリップボードにコピーします：

    ```text
    Debug: Select and Start Debugging
    ```

2. <kbd>F1</kbd> を押して VS Code コマンドパレットを開きます。
3. テキストをコマンドパレットに貼り付けて、**Debug: Select and Start Debugging** を選択します。
4. リストから **🌎🤖Debug Compound: Agent and MCP (http)** を選択します。これにより、エージェントアプリと Web チャットクライアントが開始されます。

## エージェントとの会話を開始する

ブラウザの **Web Chat** タブに切り替えます。エージェントアプリが実行され、質問を受け付ける準備ができているはずです。

### DevTunnel を使ったデバッグ

DevTunnel を使用して MCP サーバーとエージェントアプリをデバッグできます。これにより、ネットワークアクティビティを検査し、リアルタイムで問題をトラブルシューティングできます。

1. DevTunnel 出力から **Inspect network activity** URL を選択します。
2. これにより、MCP サーバーとエージェントアプリのネットワークアクティビティを確認できる新しいタブがブラウザで開きます。
3. これを使用して、ワークショップ中に発生する問題をデバッグできます。

MCP サーバーコードとエージェントアプリコードにブレークポイントを設定して、特定の問題をデバッグすることもできます。これを行うには：

1. `mcp_server` フォルダの `sales_analysis.py` ファイルを開きます。
2. 実行を一時停止したい行番号の横の余白をクリックして、ブレークポイントを設定します。
3. 実行がブレークポイントに到達すると、変数を検査し、コードをステップ実行し、デバッグコンソールで式を評価できます。

*Translated using GitHub Copilot and GPT-4o.*
