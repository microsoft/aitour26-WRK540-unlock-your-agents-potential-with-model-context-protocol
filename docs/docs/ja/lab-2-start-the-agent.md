## 学習内容

このラボでは、コードインタープリターを有効にして、自然言語で売上データを分析し、グラフを作成します。

## はじめに

このラボでは、Azure AI エージェントを2つのツールで拡張します：

- **コードインタープリター:** エージェントがデータ分析と可視化のためにPythonコードを生成・実行できるようにします。
- **MCPサーバーツール:** エージェントがMCPツールを使用して外部データソース（この場合はPostgreSQLデータベースのデータ）にアクセスできるようにします。

## ラボ演習

### コードインタープリターとMCPサーバーの有効化

このラボでは、連携して動作する2つの強力なツールを有効にします：コードインタープリター（データ分析と可視化のためにAI生成Pythonコードを実行）とMCPサーバー（PostgreSQLに保存されたZavaの売上データへの安全なアクセスを提供）。

=== "Python"

    1. **開く** `app.py` ファイルを。
    2. **67行目まで** スクロールし、エージェントのツールセットにコードインタープリターツールとMCPサーバーツールを追加する行を見つけます。これらの行は現在、先頭に **# プラス スペース** 文字でコメントアウトされています。
    3. **コメントアウトを解除** 次の行の：

        !!! warning "Pythonではインデントが重要です！"
            コメントアウトを解除する際は、`#` シンボルとそれに続くスペースの両方を削除してください。これにより、コードが適切なPythonインデントを維持し、周囲のコードと正しく整列されます。

        ```python
        # self.toolset.add(code_interpreter_tool)
        # self.toolset.add(mcp_server_tools)
        ```

        !!! info "このコードは何をしますか？"
            - **コードインタープリターツール**: エージェントがデータ分析と可視化のためにPythonコードを実行できるようにします。
            - **MCPサーバーツール**: 特定の許可されたツールで外部データソースへのアクセスを提供し、人間の承認は不要です。本番アプリケーションでは、機密操作に対してヒューマンインザループ認証を有効にすることを検討してください。

    4. **確認** コメントアウトを解除したコードを。コードは次のようになるはずです：

        コメントアウトを解除後、あなたのコードは次のようになるはずです：

        ```python
        async def _setup_agent_tools(self) -> None:
            """Setup MCP tools and code interpreter."""
            logger.info("Setting up Agent tools...")
            self.toolset = AsyncToolSet()

            code_interpreter_tool = CodeInterpreterTool()

            mcp_server_tools = McpTool(
                server_label="ZavaSalesAnalysisMcpServer",
                server_url=Config.DEV_TUNNEL_URL,
                allowed_tools=[
                    "get_multiple_table_schemas",
                    "execute_sales_query",
                    "get_current_utc_date",
                    "semantic_search_products",
                ],
            )
            mcp_server_tools.set_approval_mode("never")  # No human in the loop

            self.toolset.add(code_interpreter_tool)
            self.toolset.add(mcp_server_tools)
        ```

    ## エージェントアプリの開始

    1. 以下のテキストをクリップボードにコピー：

    ```text
    Debug: Select and Start Debugging
    ```

    1. <kbd>F1</kbd>を押してVS Codeコマンドパレットを開きます。
    1. テキストをコマンドパレットに貼り付け、**Debug: Select and Start Debugging**を選択します。
    1. リストから**🌎🤖Debug Compound: Agent and MCP (http)**を選択します。これにより、エージェントアプリとWebチャットクライアントが開始されます。

    これにより次のプロセスが開始されます：

    1.  DevTunnel (workshop) Task
    2.  Web Chat (workshop)
    3.  Agent Manager (workshop)
    4.  MCP Server (workshop)

    VS CodeのTERMINALパネルでこれらが実行されているのが見えます。

    ![画像はVS Code TERMINALパネルで実行中のプロセスを示しています](../media/vs-code-processes.png)

    ## エージェントWebチャットクライアントを開く

    === "@イベント参加者"

        次のリンクを選択してブラウザでWebチャットアプリを開きます。

        [Webチャットを開く](http://localhost:8005){:target="_blank"}

    === "自己学習者"

        ## ポート8005を公開する

        ブラウザでWebチャットクライアントにアクセスするため、ポート8005を公開する必要があります。

        1. VS Codeの下部パネルで**Ports**タブを選択します。
        2. **Web Chat App (8005)**ポートを右クリックして**Port Visibility**を選択します。
        3. **Public**を選択します。

        ![](../media/make-port-public.png)


        ## ブラウザでWebチャットクライアントを開く

        1.  以下のテキストをクリップボードにコピー：

        ```text
        Open Port in Browser
        ```

        2.  <kbd>F1</kbd>を押してVS Codeコマンドパレットを開きます。
        3.  テキストをコマンドパレットに貼り付け、**Open Port in Browser**を選択します。
        4.  リストから**8005**を選択します。これによりブラウザでエージェントWebチャットクライアントが開きます。

    ![](../media/agent_web_chat.png)

=== "C#"

    1. **開く** `McpAgentWorkshop.WorkshopApi` プロジェクトの`Services`フォルダーから`AgentService.cs`を。
    2. `InitialiseAgentAsync`メソッドに移動します。
    3. **コメントアウトを解除** 次の行の：

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

    ## エージェントアプリの開始

    4. <kbd>F1</kbd>を押してVS Codeコマンドパレットを開きます。
    5. 起動設定として**Debug Aspire**を選択します。

    デバッガが起動されると、Aspireダッシュボードでブラウザウィンドウが開きます。すべてのリソースが開始されると、**Workshop Frontend**リンクをクリックしてワークショップWebアプリケーションを起動できます。

    ![Aspireダッシュボード](../media//lab-2-start-agent-aspire-dashboard.png)

    !!! tip "トラブルシューティング"
        ブラウザが読み込まれない場合は、ページを強制リフレッシュしてみてください（Ctrl + F5 または Cmd + Shift + R）。それでも読み込まれない場合は、[トラブルシューティングガイド](./dotnet-troubleshooting.md)を参照してください。

## エージェントとの会話を開始

Webチャットクライアントから、エージェントとの会話を開始できます。エージェントは、Zavaの売上データに関する質問に答え、コードインタープリターを使用して可視化を生成するように設計されています。

1.  製品売上分析。次の質問をチャットにコピー＆ペーストしてください：

    ```text
    Show the top 10 products by revenue by store for the last quarter
    ```

    しばらくすると、エージェントは各店舗の売上トップ10製品を示すテーブルで応答します。

    !!! info
        エージェントは、データを取得してテーブルに表示するために3つのMCPサーバーツールを呼び出すLLMを使用します：

        1. **get_current_utc_date()**: 現在の日付と時刻を取得し、エージェントが現在の日付に対して最後の四半期を決定できるようにします。
        2. **get_multiple_table_schemas()**: 有効なSQLを生成するためにLLMが必要とするデータベース内のテーブルのスキーマを取得します。
        3. **execute_sales_query**: PostgreSQLデータベースから最後の四半期の売上トップ10製品を取得するSQLクエリを実行します。

    !!! tip
        === "Python"

            VS Codeに戻り、TERMINALパネルから**MCP Server (workspace)**を選択すると、Azure AI Foundry Agent ServiceによってMCPサーバーに対して行われた呼び出しが表示されます。

            ![](../media/mcp-server-in-action.png)

        === "C#"

            Aspireダッシュボードで、`dotnet-mcp-server`リソースのログを選択して、Azure AI Foundry Agent ServiceによってMCPサーバーに対して行われた呼び出しを確認できます。

            また、トレースビューを開いて、Webチャットでのユーザー入力から、エージェント呼び出しとMCPツール呼び出しまでの、アプリケーションのエンドツーエンドトレースを見つけることもできます。

            ![トレース概要](../media/lab-7-trace-overview.png)

2.  円グラフを生成。次の質問をチャットにコピー＆ペーストしてください：

    ```text
    Show sales by store as a pie chart for this financial year
    ```

    エージェントは、今会計年度の店舗別売上分布を示す円グラフで応答します。

    !!! info
        これは魔法のように感じるかもしれませんが、すべてを機能させるために舞台裏で何が起こっているのでしょうか？

        Foundry Agent Serviceは次のステップを調整します：

        1. 前の質問と同様に、エージェントはクエリに必要なテーブルスキーマを持っているかどうかを判断します。持っていない場合、**get_multiple_table_schemas()** ツールを使用して現在の日付とデータベーススキーマを取得します。
        2. 次に、エージェントは**execute_sales_query**ツールを使用して売上を取得します
        3. 返されたデータを使用して、LLMは円グラフを作成するPythonコードを記述します。
        4. 最後に、コードインタープリターがPythonコードを実行してグラフを生成します。

3.  Zavaの売上データに関する質問を続けて、コードインタープリターの動作を確認してください。試してみたいフォローアップ質問をいくつか紹介します：

    - `Determine which products or categories drive sales. Show as a Bar Chart.`
    - `What would be the impact of a shock event (e.g., 20% sales drop in one region) on global sales distribution? Show as a Grouped Bar Chart.`
      - 続けて `What if the shock event was 50%?`
    - `Which regions have sales above or below the average? Show as a Bar Chart with Deviation from Average.`
    - `Which regions have discounts above or below the average? Show as a Bar Chart with Deviation from Average.`
    - `Simulate future sales by region using a Monte Carlo simulation to estimate confidence intervals. Show as a Line with Confidence Bands using vivid colors.`

<!-- ## Stop the Agent App

1. Switch back to the VS Code editor.
1. Press <kbd>Shift + F5</kbd> to stop the agent app. -->

## エージェントアプリを実行したままにする

次のラボでエージェントをより多くのツールと機能で拡張するために使用するため、エージェントアプリを実行したままにしてください。

*GitHub Copilotを使用して翻訳されました。*
