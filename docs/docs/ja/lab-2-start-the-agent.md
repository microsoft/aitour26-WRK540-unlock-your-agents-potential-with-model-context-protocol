## 学習内容

このラボでは、自然言語を使用して売上データを分析し、チャートを作成するための Code Interpreter を有効にします。

## はじめに

このラボでは、Azure AI Agent を2つのツールで拡張します：

- **Code Interpreter:** エージェントがデータ分析と視覚化のための Python コードを生成・実行できるようにします。
- **MCP Server ツール:** エージェントが MCP ツールを使用して外部データソース（今回は PostgreSQL データベースのデータ）にアクセスできるようにします。

## ラボ演習

### Code Interpreter を有効にする

このラボでは、Zava の小売売上データを分析するために LLM が生成した Python コードを実行する Code Interpreter を有効にします。

=== "Python"

    1. `app.py` を**開きます**。
    2. `AgentManager` クラスの `_setup_agent_tools` メソッドで、エージェントのツールセットに Code Interpreter ツールを追加する行の**コメントアウトを解除**します。この行は現在、行の先頭に `#` でコメントアウトされています：

        ```python
        # code_interpreter = CodeInterpreterTool()
        # self.toolset.add(code_interpreter)
        ```

    3. `app.py` ファイルのコードを**確認**します。`AgentManager` クラスの `_setup_agent_tools` メソッドで、Code Interpreter と MCP Server ツールがエージェントのツールセットに追加されていることがわかります。

        ```python

        コメントアウトを解除した後、コードは次のようになります：

        ```python
        class AgentManager:
            """Manages Azure AI Agent lifecycle and dependencies."""

            async def _setup_agent_tools(self) -> None:
                """Setup MCP tools and code interpreter."""

                # Enable the code interpreter tool
                code_interpreter = CodeInterpreterTool()
                self.toolset.add(code_interpreter)

                print("Setting up Agent tools...")
                ...
        ```

=== "C#"

    TBD

## エージェントアプリを開始する

1. 以下のテキストをクリップボードにコピーします：

    ```text
    Debug: Select and Start Debugging
    ```

2. <kbd>F1</kbd> を押して VS Code コマンドパレットを開きます。
3. テキストをコマンドパレットに貼り付けて、**Debug: Select and Start Debugging** を選択します。
4. リストから **🔁🤖Debug Compound: Agent and MCP (stdio)** を選択します。これにより、エージェントアプリと Web チャットクライアントが開始されます。

## エージェント Web チャットクライアントを開く

1. 以下のテキストをクリップボードにコピーします：

    ```text
    Open Port in Browser
    ```

2. <kbd>F1</kbd> を押して VS Code コマンドパレットを開きます。
3. テキストをコマンドパレットに貼り付けて、**Open Port in Browser** を選択します。
4. リストから **8005** を選択します。これにより、エージェント Web チャットクライアントがブラウザで開きます。

### エージェントとの会話を開始する

Web チャットクライアントから、エージェントとの会話を開始できます。エージェントは Zava の売上データに関する質問に答え、Code Interpreter を使用して視覚化を生成するように設計されています。

1. 製品売上分析。以下の質問をチャットにコピー・貼り付けしてください：

    ```text
    先四半期の店舗別売上トップ10製品を表示して
    ```

    しばらくすると、エージェントは各店舗の売上トップ10製品を示すテーブルで応答します。

    !!! info
        エージェントは LLM を使用して3つの MCP Server ツールを呼び出し、データを取得してテーブルに表示します：

           1. **get_current_utc_date()**: 現在の日時を取得し、エージェントが現在の日付に対する先四半期を決定できるようにします。
           2. **get_multiple_table_schemas()**: LLM が有効な SQL を生成するために必要なデータベース内のテーブルのスキーマを取得します。
           3. **execute_sales_query**: PostgreSQL データベースから先四半期の売上トップ10製品を取得する SQL クエリを実行します。

2. 円グラフを生成します。以下の質問をチャットにコピー・貼り付けしてください：

    ```text
    今会計年度の店舗別売上を円グラフで表示して
    ```

    エージェントは、現在の会計年度の店舗別売上分布を示す円グラフで応答します。

    !!! info
        これは魔法のように感じるかもしれませんが、すべてを機能させるために舞台裏で何が起こっているのでしょうか？

        Foundry Agent Service は以下のステップを調整します：

        1. 前の質問と同様に、エージェントはクエリに必要なテーブルスキーマがあるかどうかを判断します。ない場合は、**get_multiple_table_schemas()** ツールを使用して現在の日付とデータベーススキーマを取得します。
        2. エージェントは **execute_sales_query** ツールを使用して売上データを取得します。
        3. 返されたデータを使用して、LLM は円グラフを作成する Python コードを書きます。
        4. 最後に、Code Interpreter が Python コードを実行してチャートを生成します。

3. Code Interpreter の動作を確認するために、Zava の売上データについてさらに質問を続けてください。試してみたいフォローアップ質問をいくつか紹介します：

    - ```売上を牽引する製品やカテゴリを特定してください。棒グラフで表示してください。```
    - ```ショックイベント（例：ある地域での売上20%減）がグローバル売上分布に与える影響は？グループ化棒グラフで表示してください。```
        - フォローアップで ```ショックイベントが50%だったらどうなりますか？```
    - ```平均以上または以下の売上を持つ地域はどこですか？平均からの偏差付き棒グラフで表示してください。```
    - ```平均以上または以下の割引を持つ地域はどこですか？平均からの偏差付き棒グラフで表示してください。```
    - ```モンテカルロシミュレーションを使用して地域別の将来売上をシミュレートし、信頼区間を推定してください。鮮やかな色を使った信頼帯付きラインで表示してください。```

<!-- ## エージェントアプリを停止する

1. VS Code エディターに戻ります。
1. <kbd>Shift + F5</kbd> を押してエージェントアプリを停止します。 -->

## エージェントアプリを実行したままにする

次のラボでエージェントをより多くのツールと機能で拡張するために使用するので、エージェントアプリは実行したままにしておいてください。

*Translated using GitHub Copilot and GPT-4o.*
