## 言語ワークスペースを開く

ワークショップには2つのワークスペースがあります：Python用とC#用です。ワークスペースには、各言語でラボを完了するために必要なソースコードとすべてのファイルが含まれています。作業したい言語に対応するワークスペースを選択してください。

=== "Python"

    1. 次のコマンドをクリップボードにコピーします：

        ```text
        File: Open Workspace from File...
        ```
    2. Visual Studio Code に切り替え、<kbd>F1</kbd> を押してコマンドパレットを開きます。
    3. コマンドをコマンドパレットに貼り付け、**Open Workspace from File...** を選択します。
    4. 次のパスをファイルピッカーにコピー・貼り付けし、<kbd>Enter</kbd> を押します：

        ```text
        /workspace/.vscode/python-workspace.code-workspace
        ```

    ## プロジェクト構造

    ワークショップを通じて作業する主要な**フォルダ**と**ファイル**について必ず理解しておいてください。

    ### workshop フォルダ

    - **app.py** ファイル: アプリのエントリーポイントで、主要なロジックが含まれています。
  
    **INSTRUCTIONS_FILE** 変数に注意してください—これはエージェントが使用する指示ファイルを設定します。後のラボでこの変数を更新します。

    - **resources.txt** ファイル: エージェントアプリで使用されるリソースが含まれています。
    - **.env** ファイル: エージェントアプリで使用される環境変数が含まれています。

    ### mcp_server フォルダ

    - **sales_analysis.py** ファイル: 売上分析用ツールを含む MCP Server です。

    ### shared フォルダ

    - **instructions** フォルダ: LLM に渡される指示が含まれています。

    ![ラボフォルダ構造](media/project-structure-self-guided-python.png)

=== "C#"

    1. Visual Studio Code で、**File** > **Open Workspace from File** に移動します。
    2. デフォルトパスを以下に置き換えます：

        ```text
        /workspace/.vscode/csharp-workspace.code-workspace
        ```

    3. **OK** を選択してワークスペースを開きます。

    ## プロジェクト構造

    ワークショップを通じて作業する主要な**フォルダ**と**ファイル**について必ず理解しておいてください。

    ### workshop フォルダ

    - **Lab1.cs、Lab2.cs、Lab3.cs** ファイル: 各ラボのエントリーポイントで、エージェントロジックが含まれています。
    - **Program.cs** ファイル: アプリのエントリーポイントで、主要なロジックが含まれています。
    - **SalesData.cs** ファイル: SQLite データベースに対する動的 SQL クエリを実行する関数ロジックです。

    ### shared フォルダ

    - **files** フォルダ: エージェントアプリによって作成されたファイルが含まれています。
    - **fonts** フォルダ: Code Interpreter で使用される多言語フォントが含まれています。
    - **instructions** フォルダ: LLM に渡される指示が含まれています。

    ![ラボフォルダ構造](media/project-structure-self-guided-csharp.png)

*Translated using GitHub Copilot and GPT-4o.*
