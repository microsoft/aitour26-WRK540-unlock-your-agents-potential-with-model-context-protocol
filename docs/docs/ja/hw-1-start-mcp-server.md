## 学習内容

このラボでは以下を学習します：

- DevTunnelを使用してローカルMCPサーバーをクラウドベースエージェントサービスにアクセス可能にする
- Model Context Protocolを使った実践的な実験のための環境設定

## はじめに

Model Context Protocol（MCP）サーバーは、大規模言語モデル（LLM）と外部ツールおよびデータソース間の通信を処理する重要なコンポーネントです。MCPサーバーをローカルマシンで実行しますが、Azure AI Foundry Agent Serviceはインターネットアクセスが必要です。ローカルMCPサーバーをインターネットからアクセス可能にするために、DevTunnelを使用します。これにより、Agent ServiceはMCPサーバーがAzureのサービスとして実行されているかのように通信できます。

## MCPのインターフェイスオプション

MCPは、LLMをツールに接続するための2つの主要インターフェイスをサポートしています：

- **Streamable HTTP Transport**: WebベースのAPIとサービス用。
- **Stdio Transport**: ローカルスクリプトとコマンドラインツール用。

このラボでは、Azure AI Foundry Agent Serviceと統合するためにStreamable HTTP transportインターフェイスを使用します。

!!! note
    通常は本番環境でMCPサーバーをデプロイしますが、このワークショップではローカルの開発環境で実行します。これにより、完全なデプロイを必要とすることなく、MCPツールをテストし、やり取りできます。

### MCPサーバー用のDevTunnelを起動する

1. 新しいターミナルで、DevTunnelを認証します。Azureアカウントでのログインを促されます。Azure AI Foundry Agent ServiceまたはAzure Portalへのログインに使用したものと同じアカウントを使用してください。以下のコマンドを実行します：

    ```bash
    devtunnel login
    ```

1. 次に、MCPサーバーが実行されているターミナルで、以下を実行してDevTunnelを開始します：

    ```bash
    devtunnel host -p 8000 --allow-anonymous
    ```

    これはエージェントがMCPサーバーに接続するために必要なURLを出力します。出力は以下のようになります：

    ```text
    Hosting port: 8000
    Connect via browser: https://<tunnel-id>-8000.aue.devtunnels.ms
    Inspect network activity: https://<tunnel-id>-8000-inspect.aue.devtunnels.ms
    ```

## DevTunnel環境変数を更新する

1. **Connect via browser** URLをクリップボードにコピーします - エージェントを設定する次のラボで必要になります。
2. workshopフォルダの`.env`ファイルを開きます。
3. `DEV_TUNNEL_URL`変数をコピーしたURLで更新します。

    ```text
    DEV_TUNNEL_URL=https://<tunnel-id>-8000.aue.devtunnels.ms
    ```

## エージェントアプリを起動する

1. 以下のテキストをクリップボードにコピーします：

    ```text
    Debug: Select and Start Debugging
    ```

2. <kbd>F1</kbd>を押してVS Code Command Paletteを開きます。
3. Command Paletteにテキストを貼り付け、**Debug: Select and Start Debugging**を選択します。
4. リストから**🌎🤖Debug Compound: Agent and MCP (http)**を選択します。これによりエージェントアプリとWebチャットクライアントが開始されます。

## エージェントとの会話を開始する

ブラウザの**Web Chat**タブに切り替えます。エージェントアプリが実行され、質問を受け付ける準備ができていることを確認してください。

### DevTunnelでのデバッグ

DevTunnelを使用してMCPサーバーとエージェントアプリをデバッグできます。これにより、ネットワークアクティビティを検査し、問題をリアルタイムでトラブルシューティングできます。

1. DevTunnel出力から**Inspect network activity** URLを選択します。
2. これにより、MCPサーバーとエージェントアプリのネットワークアクティビティを確認できる新しいタブがブラウザで開きます。
3. これを使用して、ワークショップ中に発生する問題をデバッグできます。

また、特定の問題をデバッグするために、MCPサーバーコードとエージェントアプリコードにブレークポイントを設定することもできます。これを行うには：

1. `mcp_server`フォルダの`sales_analysis.py`ファイルを開きます。
2. 実行を一時停止したい行番号の横のガターをクリックしてブレークポイントを設定します。
3. 実行がブレークポイントに到達すると、変数を検査し、コードをステップ実行し、Debug Consoleで式を評価できます。
