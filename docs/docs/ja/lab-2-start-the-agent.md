## 学習内容

このラボでは、Code Interpreterを有効にして自然言語で売上データを分析し、グラフを作成します。

## はじめに

このラボでは、Azure AI Agentを2つのツールで拡張します：

- **Code Interpreter:** エージェントがデータ分析と可視化のためにPythonコードを生成・実行できるようにします。
- **MCPサーバーツール:** エージェントがMCPツールを使用して外部データソース（この場合はPostgreSQLデータベースのデータ）にアクセスできるようにします。

## ラボ演習

### Code InterpreterとMCPサーバーを有効化する

このラボでは、連携する2つの強力なツールを有効化します：Code Interpreter（データ分析と可視化のためにAI生成Pythonコードを実行）とMCPサーバー（PostgreSQLに格納されたZavaの売上データへのセキュアなアクセスを提供）。

=== "Python"

    1. `app.py`を**開きます**。
    2. **50行目あたりまでスクロール**し、Code InterpreterとMCPツールをエージェントのツールセットに追加する行を見つけます。これらの行は現在、行の先頭に`#`でコメントアウトされています。
    3. 以下の行を**アンコメント**します：

        ```python
        
        # code_interpreter = CodeInterpreterTool()
        # self.toolset.add(code_interpreter)
        
        # mcp_tools = McpTool(
        #     server_label="ZavaSalesAnalysisMcpServer",
        #     server_url=Config.DEV_TUNNEL_URL,
        #     allowed_tools=[
        #         "get_multiple_table_schemas",
        #         "execute_sales_query",
        #         "get_current_utc_date",
        #         "semantic_search_products",
        #     ],
        # )

        # mcp_tools.set_approval_mode("never")  # No human in the loop
        # self.toolset.add(mcp_tools)
        ```

        !!! info "このコードは何をしますか？"
            - **Code Interpreter**: エージェントがデータ分析と可視化のためにPythonコードを実行できるようにします。
            - **MCPサーバーツール**: 特定の許可されたツールで外部データソースへのアクセスを提供し、人間の承認は不要です。本番アプリケーションでは、機密操作に対してhuman-in-the-loop認証の有効化を検討してください。

    4. アンコメントしたコードを**確認**します。コードは以下のようになっている必要があります：

        アンコメント後、コードは以下のようになります：

        ```python
        class AgentManager:
            """Manages Azure AI Agent lifecycle and dependencies."""

            async def _setup_agent_tools(self) -> None:
                """Setup MCP tools and code interpreter."""
                logger.info("Setting up Agent tools...")
                self.toolset = AsyncToolSet()

                code_interpreter = CodeInterpreterTool()
                self.toolset.add(code_interpreter)

                mcp_tools = McpTool(
                    server_label="ZavaSalesAnalysisMcpServer",
                    server_url=Config.DEV_TUNNEL_URL,
                    allowed_tools=[
                        "get_multiple_table_schemas",
                        "execute_sales_query",
                        "get_current_utc_date",
                        "semantic_search_products",
                    ],
                )

                mcp_tools.set_approval_mode("never")  # No human in the loop
                self.toolset.add(mcp_tools)
        ```

    ## エージェントアプリを起動する

    1. 以下のテキストをクリップボードにコピーします：

    ```text
    Debug: Select and Start Debugging
    ```

    1. <kbd>F1</kbd>を押してVS Code Command Paletteを開きます。
    1. Command Paletteにテキストを貼り付け、**Debug: Select and Start Debugging**を選択します。
    1. リストから**🌎🤖Debug Compound: Agent and MCP (http)**を選択します。これによりエージェントアプリとWebチャットクライアントが開始されます。

    これにより以下のプロセスが開始されます：

    1.  DevTunnel (workshop) Task
    2.  Web Chat (workshop)
    3.  Agent Manager (workshop)
    4.  MCP Server (workshop)

    VS CodeのTERMINALパネルでこれらが実行されているのを確認できます。

    ![The image shows the running processes in the VS Code TERMINAL panel](../media/vs-code-processes.png)

    ## Agent Web Chatクライアントを開く

    === "@Event Attendees"

        以下のリンクを選択してブラウザでWeb Chatアプリを開きます。

        [Web Chatを開く](http://localhost:8005){:target="_blank"}

    === "Self-Guided Learners"

        ## ポート8005をパブリックにする

        ブラウザでWebチャットクライアントにアクセスするために、ポート8005をパブリックにする必要があります。

        1. VS Code下部パネルの**Ports**タブを選択します。
        2. **Web Chat App (8005)**ポートを右クリックし、**Port Visibility**を選択します。
        3. **Public**を選択します。

        ![](../media/make-port-public.png)


        ## ブラウザでWebチャットクライアントを開く

        1.  以下のテキストをクリップボードにコピーします：

        ```text
        Open Port in Browser
        ```

        2.  <kbd>F1</kbd>を押してVS Code Command Paletteを開きます。
        3.  Command Paletteにテキストを貼り付け、**Open Port in Browser**を選択します。
        4.  リストから**8005**を選択します。これにより、ブラウザでエージェントWebチャットクライアントが開きます。

    ![](../media/agent_web_chat.png)

=== "C#"

    1. `McpAgentWorkshop.WorkshopApi`プロジェクトの`Services`フォルダから`AgentService.cs`を**開きます**。
    2. `InitialiseAgentAsync`メソッドに移動します。
    3. 以下の行を**アンコメント**します：

        ```csharp
        // var mcpTool = new MCPToolDefinition(
        //     ZavaMcpToolLabel,
        //     devtunnelUrl + "mcp");

        // var codeInterpreterTool = new CodeInterpreterToolDefinition();

        // IEnumerable<ToolDefinition> tools = [mcpTool, codeInterpreterTool];

        // persistentAgent = await persistentAgentsClient.Administration.CreateAgentAsync(
        //         name: AgentName,
        //         model: configuration.GetValue<string>("MODEL_DEPLOYMENT_NAME"),
        //         instructions: instructionsContent,
        //         temperature: modelTemperature,
        //         tools: tools);

        // logger.LogInformation("Agent created with ID: {AgentId}", persistentAgent.Id);
        ```

    ## エージェントアプリを起動する

    4. <kbd>F1</kbd>を押してVS Code Command Paletteを開きます。
    5. 起動設定として**Debug Aspire**を選択します。

    デバッガーが起動すると、Aspireダッシュボードがブラウザウィンドウで開きます。すべてのリソースが開始されたら、**Workshop Frontend**リンクをクリックしてワークショップWebアプリケーションを起動できます。

    ![Aspire dashboard](../media//lab-2-start-agent-aspire-dashboard.png)

    !!! tip "トラブルシューティング"
        ブラウザが読み込まれない場合は、ページをハードリフレッシュ（Ctrl + F5またはCmd + Shift + R）してください。それでも読み込まれない場合は、[トラブルシューティングガイド](./dotnet-troubleshooting.md)を参照してください。

## エージェントとの会話を開始する

Webチャットクライアントから、エージェントとの会話を開始できます。エージェントはZavaの売上データに関する質問に答え、Code Interpreterを使用して可視化を生成するよう設計されています。

1.  製品売上分析。以下の質問をチャットにコピー＆ペーストします：

    ```text
    Show the top 10 products by revenue by store for the last quarter
    ```

    しばらくすると、エージェントは各店舗の売上上位10製品を示すテーブルで応答します。

    !!! info
        エージェントはLLMが3つのMCPサーバーツールを呼び出してデータを取得し、テーブルで表示します：

        1. **get_current_utc_date()**: 現在の日時を取得し、エージェントが現在の日付に対して前四半期を決定できるようにします。
        2. **get_multiple_table_schemas()**: 有効なSQLを生成するためにLLMが必要とするデータベースのテーブルスキーマを取得します。
        3. **execute_sales_query**: PostgreSQLデータベースから前四半期の売上上位10製品を取得するSQLクエリを実行します。

    !!! tip
        === "Python"

            VS Codeに戻り、TERMINALパネルから**MCP Server (workspace)**を選択すると、Azure AI Foundry Agent ServiceによるMCPサーバーへの呼び出しを確認できます。

            ![](../media/mcp-server-in-action.png)

        === "C#"

            Aspireダッシュボードで、`dotnet-mcp-server`リソースのログを選択して、Azure AI Foundry Agent ServiceによるMCPサーバーへの呼び出しを確認できます。

            また、トレースビューを開いて、Webチャットでのユーザー入力からエージェント呼び出しとMCPツール呼び出しまでのアプリケーションのエンドツーエンドトレースを見つけることもできます。

            ![Trace overview](../media/lab-7-trace-overview.png)

2.  円グラフを生成する。以下の質問をチャットにコピー＆ペーストします：

    ```text
    Show sales by store as a pie chart for this financial year
    ```

    エージェントは今会計年度の店舗別売上分布を示す円グラフで応答します。

    !!! info
        これは魔法のように感じるかもしれませんが、すべてを動作させるために舞台裏で何が起こっているのでしょうか？

        Foundry Agent Serviceは以下のステップを調整します：

        1. 前の質問と同様に、エージェントはクエリに必要なテーブルスキーマを持っているかどうかを判断します。持っていない場合は、**get_multiple_table_schemas()**ツールを使用して現在の日付とデータベーススキーマを取得します。
        2. エージェントは次に**execute_sales_query**ツールを使用して売上データを取得します
        3. 返されたデータを使用して、LLMが円グラフを作成するPythonコードを記述します。
        4. 最後に、Code InterpreterがPythonコードを実行してグラフを生成します。

3.  Code Interpreterの動作を確認するために、Zava売上データに関する質問を続けてください。以下にいくつかのフォローアップ質問例を示します：

    - `売上を牽引する製品やカテゴリを判断してください。棒グラフで表示。`
    - `ショック現象（例：ある地域での20%の売上下落）が世界の売上分布にどのような影響を与えるか？グループ化棒グラフで表示。`
      - フォローアップ：`ショック現象が50%だったらどうなる？`
    - `平均を上回る、または下回る売上の地域はどこか？平均からの偏差を含む棒グラフで表示。`
    - `平均を上回る、または下回る割引の地域はどこか？平均からの偏差を含む棒グラフで表示。`
    - `モンテカルロシミュレーションを使用して地域別の将来売上をシミュレートし、信頼区間を推定。鮮やかな色を使った信頼帯付き線グラフで表示。`

<!-- ## エージェントアプリを停止する

1. VS Codeエディターに戻る。
1. <kbd>Shift + F5</kbd>を押してエージェントアプリを停止する。 -->

## エージェントアプリを実行したままにする

次のラボでエージェントをさらなるツールと機能で拡張するために、エージェントアプリを実行したままにしてください。
