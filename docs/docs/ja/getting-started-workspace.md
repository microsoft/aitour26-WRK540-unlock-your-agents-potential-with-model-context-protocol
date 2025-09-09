ワークショップにはPython用とC#用の2つのVS Codeワークスペースがあります。ワークスペースには、各言語のラボを完了するのに必要なソースコードとすべてのファイルが含まれています。作業したい言語に合ったワークスペースを選択してください。

=== "Python"

    1. 以下のパスをクリップボードに**コピー**してください：

        ```text
        /workspace/.vscode/python-workspace.code-workspace
        ```
    1. VS Codeメニューから、**File**、**Open Workspace from File**を選択します。
    3. コピーしたパス名を**置換して貼り付け**、**OK**を選択します。


    ## プロジェクト構造

    ワークショップを通して作業する重要な**フォルダ**と**ファイル**について理解してください。

    ### "workshop"フォルダ

    - **app.py**ファイル：アプリのエントリーポイントで、メインロジックが含まれています。

    **INSTRUCTIONS_FILE**変数に注目してください—これはエージェントが使用する指示ファイルを設定します。後のラボでこの変数を更新します。

    - **resources.txt**ファイル：エージェントアプリが使用するリソースが含まれています。
    - **.env**ファイル：エージェントアプリが使用する環境変数が含まれています。

    ### "mcp_server"フォルダ

    - **sales_analysis.py**ファイル：売上分析用のツールを含むMCPサーバー。

    ### "shared/instructions"フォルダ

    - **instructions**フォルダ：LLMに渡される指示が含まれています。

    ![ラボフォルダ構造](media/project-structure-self-guided-python.png)

=== "C#"

    1. Visual Studio Codeで、**File** > **Open Workspace from File**に移動します。
    2. デフォルトパスを以下に置換してください：

        ```text
        /workspace/.vscode/csharp-workspace.code-workspace
        ```

    3. **OK**を選択してワークスペースを開きます。

    ## プロジェクト構造

    プロジェクトは[Aspire](http://aka.ms/dotnet-aspire)を使用してエージェントアプリケーションの構築、MCPサーバーの管理、すべての外部依存関係の調整を簡素化しています。ソリューションは4つのプロジェクトから構成され、すべて`McpAgentWorkshop`プレフィックスが付いています：

    * `AppHost`: Aspireオーケストレーター、ワークショップのランチプロジェクト。
    * `McpServer`: MCPサーバープロジェクト。
    * `ServiceDefaults`: ロギングやテレメトリなどのサービスのデフォルト設定。
    * `WorkshopApi`: ワークショップ用のエージェントAPI。コアアプリケーションロジックは`AgentService`クラスにあります。

    ソリューションの.NETプロジェクトに加えて、`shared`フォルダ（Solution Folderおよびファイルエクスプローラーから表示）があり、以下が含まれています：

    * `instructions`: LLMに渡される指示。
    * `scripts`: さまざまなタスク用のヘルパーシェルスクリプト。必要に応じて参照されます。
    * `webapp`: フロントエンドクライアントアプリケーション。注：これはPythonアプリケーションで、Aspireがライフサイクルを管理します。

    ![ラボフォルダ構造](media/project-structure-self-guided-csharp.png)
