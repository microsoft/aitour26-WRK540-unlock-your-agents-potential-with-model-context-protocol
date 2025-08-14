ワークショップには2つの VS Code ワークスペースがあります。1つは Python 用、もう1つは C# 用です。ワークスペースには、各言語のラボを完了するために必要なソースコードとすべてのファイルが含まれています。作業したい言語に合ったワークスペースを選択してください。

=== "Python"

    1. 次のパスをクリップボードに**コピー**します：

        ```text
        /workspace/.vscode/python-workspace.code-workspace
        ```
    1. VS Code メニューから、**File** を選択し、次に **Open Workspace from File** を選択します。
    3. コピーしたパス名を**置換**して**貼り付け**、**OK** を選択します。


    ## プロジェクト構造

    ワークショップ全体で作業する主要な**フォルダー**と**ファイル**に慣れ親しんでください。

    ### "workshop" フォルダー

    - **app.py** ファイル: アプリのエントリーポイントで、メインロジックを含みます。
  
    **INSTRUCTIONS_FILE** 変数に注目してください—これは、エージェントが使用する指示ファイルを設定します。後のラボでこの変数を更新します。

    - **resources.txt** ファイル: エージェントアプリが使用するリソースを含みます。
    - **.env** ファイル: エージェントアプリが使用する環境変数を含みます。

    ### "mcp_server" フォルダー

    - **sales_analysis.py** ファイル: 売上分析用ツールを持つ MCP サーバー。

    ### "shared/instructions" フォルダー

    - **instructions** フォルダー: LLM に渡される指示を含みます。

    ![ラボフォルダー構造](media/project-structure-self-guided-python.png)

=== "C#"

    1. Visual Studio Code で、**File** > **Open Workspace from File** に移動します。
    2. デフォルトパスを次のように置換します：

        ```text
        /workspace/.vscode/csharp-workspace.code-workspace
        ```

    3. **OK** を選択してワークスペースを開きます。

    ## プロジェクト構造

    ワークショップ全体で作業する主要な**フォルダー**と**ファイル**を必ず理解してください。

    ### workshop フォルダー

    - **Lab1.cs、Lab2.cs、Lab3.cs** ファイル: 各ラボのエントリーポイントで、エージェントロジックを含みます。
    - **Program.cs** ファイル: アプリのエントリーポイントで、メインロジックを含みます。
    - **SalesData.cs** ファイル: SQLite データベースに対して動的 SQL クエリを実行する関数ロジック。

    ### shared フォルダー

    - **files** フォルダー: エージェントアプリによって作成されたファイルを含みます。
    - **fonts** フォルダー: コードインタープリターが使用する多言語フォントを含みます。
    - **instructions** フォルダー: LLM に渡される指示を含みます。

    ![ラボフォルダー構造](media/project-structure-self-guided-csharp.png)

*GitHub Copilot を使用して翻訳されました。*
