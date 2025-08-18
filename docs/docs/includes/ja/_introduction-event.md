## Microsoft イベント参加者

このページの指示は、[Microsoft Event 2025](https://build.microsoft.com/){:target="_blank"}に参加しており、事前設定されたラボ環境にアクセスできることを前提としています。この環境は、ワークショップを完了するために必要なすべてのツールとリソースを備えたAzureサブスクリプションを提供します。

## はじめに

このワークショップは、Azure AI エージェントサービスと関連する[SDK](https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme?context=%2Fazure%2Fai-services%2Fagents%2Fcontext%2Fcontext){:target="_blank"}について学習することを目的として設計されています。複数のラボで構成され、それぞれがAzure AI エージェントサービスの特定の機能にフォーカスしています。各ラボは前のラボの知識と作業に基づいて構築されるため、順番に完了することを意図しています。

## ワークショッププログラミング言語の選択

ワークショップはPythonとC#の両方で利用可能です。言語セレクタータブを使用して、参加しているラボルームに適した言語を必ず選択してください。なお、ワークショップの途中で言語を切り替えないでください。

**ラボルームに合った言語タブを選択してください：**

=== "Python"
    ワークショップのデフォルト言語は **Python** に設定されています。
=== "C#"
    ワークショップのデフォルト言語は **C#** に設定されています。

## Azure での認証

エージェントアプリがAzure AI エージェントサービスとモデルにアクセスできるよう、Azureで認証する必要があります。以下の手順に従ってください：

1. ターミナルウィンドウを開きます。ターミナルアプリはWindows 11のタスクバーに**ピン留め**されています。

    ![ターミナルウィンドウを開く](../media/windows-taskbar.png){ width="300" }

2. 以下のコマンドを実行してAzureで認証します：

    ```powershell
    az login
    ```

    !!! note
        ブラウザリンクを開いてAzureアカウントにログインするよう求められます。

        1. ブラウザウィンドウが自動的に開きます。**職場または学校アカウント**を選択し、**次へ**をクリックします。

        1. ラボ環境の**Resources**タブの**上部セクション**にある**ユーザー名**と**パスワード**を使用します。

        2. **OK**を選択し、次に**完了**を選択します。

3. 次に、コマンドラインから**Enter**をクリックして**デフォルト**サブスクリプションを選択します。

4. ログインしたら、以下のコマンドを実行してリソースグループに**ユーザー**ロールを割り当てます：

    ```powershell
    $subId = $(az account show --query id --output tsv) `
    ;$objectId = $(az ad signed-in-user show --query id -o tsv) `
    ; az role assignment create --role "f6c7c914-8db3-469d-8ca1-694a8f32e121" --assignee-object-id $objectId --scope /subscriptions/$subId/resourceGroups/"rg-agent-workshop" --assignee-principal-type 'User'
    ```

5. 次のステップのためにターミナルウィンドウを開いたままにしておきます。

## ワークショップを開く

Visual Studio Codeでワークショップを開くには、以下の手順に従ってください：

=== "Python"

      1. ターミナルウィンドウから、以下のコマンドを実行してワークショップリポジトリをクローンし、関連フォルダーに移動し、仮想環境を設定し、アクティベートし、必要なパッケージをインストールします：

          ```powershell
          git clone https://github.com/microsoft/build-your-first-agent-with-azure-ai-agent-service-workshop.git `
          ; cd build-your-first-agent-with-azure-ai-agent-service-workshop `
          ; python -m venv src/python/workshop/.venv `
          ; src\python\workshop\.venv\Scripts\activate `
          ; pip install -r src/python/workshop/requirements.txt `
          ; code --install-extension tomoki1207.pdf
          ```

      2. VS Codeで開きます。ターミナルウィンドウから、以下のコマンドを実行します：

          ```powershell
          code .vscode\python-workspace.code-workspace
          ```

        !!! warning "プロジェクトがVS Codeで開くと、右下角に2つの通知が表示されます。✖をクリックして両方の通知を閉じてください。"

=== "C#"

    1. ターミナルウィンドウから、以下のコマンドを実行してワークショップリポジトリをクローンします：

        ```powershell
        git clone https://github.com/microsoft/build-your-first-agent-with-azure-ai-agent-service-workshop.git
        ```

    === "VS Code"

        1. Visual Studio Codeでワークショップを開きます。ターミナルウィンドウから、以下のコマンドを実行します：

            ```powershell
            code build-your-first-agent-with-azure-ai-agent-service-workshop\.vscode\csharp-workspace.code-workspace
            ```

        !!! note "プロジェクトがVS Codeで開くと、右下角にC#拡張機能をインストールする通知が表示されます。**インストール**をクリックしてC#拡張機能をインストールしてください。これによりC#開発に必要な機能が提供されます。"

    === "Visual Studio 2022"

        1. Visual Studio 2022でワークショップを開きます。ターミナルウィンドウから、以下のコマンドを実行します：

            ```powershell
            start build-your-first-agent-with-azure-ai-agent-service-workshop\src\csharp\workshop\AgentWorkshop.sln
            ```

            !!! note "ソリューションを開くプログラムを尋ねられる場合があります。**Visual Studio 2022**を選択してください。"

## Azure AI Foundry プロジェクトエンドポイント

次に、Azure AI Foundryにログインしてプロジェクトエンドポイントを取得します。エージェントアプリはこれを使用してAzure AI エージェントサービスに接続します。

1. [Azure AI Foundry](https://ai.azure.com){:target="_blank"}ウェブサイトに移動します。
2. **サインイン**を選択し、ラボ環境の**Resources**タブの**上部セクション**にある**ユーザー名**と**パスワード**を使用します。**ユーザー名**と**パスワード**フィールドをクリックすると、ログイン詳細が自動的に入力されます。
    ![Azure認証情報](../media/azure-credentials.png){:width="500"}
3. Azure AI Foundryの紹介を読み、**了解**をクリックします。
4. [すべてのリソース](https://ai.azure.com/AllResources){:target="_blank"}に移動して、事前にプロビジョニングされたAIリソースのリストを表示します。
5. **aip-**で始まるタイプ**Project**のリソース名を選択します。

    ![プロジェクトを選択](../media/ai-foundry-project.png){:width="500"}

6. 紹介ガイドを確認し、**閉じる**をクリックします。
7. **概要**サイドバーメニューから、**エンドポイントとキー** -> **ライブラリ** -> **Azure AI Foundry**セクションで、**コピー**アイコンをクリックして**Azure AI Foundryプロジェクトエンドポイント**をコピーします。

    ![接続文字列をコピー](../media/project-connection-string.png){:width="500"}

=== "Python"

    ## ワークショップの設定

    1. VS Codeで開いたワークショップに戻ります。
    2. `.env.sample`ファイルを`.env`に**名前変更**します。

        - VS Code **エクスプローラー**パネルで**.env.sample**ファイルを選択します。
        - ファイルを右クリックして**名前変更**を選択するか、<kbd>F2</kbd>を押します。
        - ファイル名を`.env`に変更し、<kbd>Enter</kbd>を押します。

    3. Azure AI FoundryからコピーしたプロジェクトエンドポイントをファイルにAzure AI Foundryプロジェクトエンドポイントの値のを`.env`ファイルに貼り付けます。

        ```python
        PROJECT_ENDPOINT="<your_project_endpoint>"
        ```

        `.env`ファイルは次のようになりますが、あなたのプロジェクトエンドポイントが入ります。

        ```python
        PROJECT_ENDPOINT="<your_project_endpoint>"
        MODEL_DEPLOYMENT_NAME="<your_model_deployment_name>"
        DEV_TUNNEL_URL="<your_dev_tunnel_url>"
        ```

    4. `.env`ファイルを保存します。

    ## プロジェクト構造

    ワークショップ全体で作業する主要な**サブフォルダー**と**ファイル**を必ず理解してください。

    5. **app.py**ファイル：アプリのエントリーポイントで、メインロジックを含みます。
    6. **sales_data.py**ファイル：SQLiteデータベースに対して動的SQLクエリを実行する関数ロジック。
    7. **stream_event_handler.py**ファイル：トークンストリーミングのイベントハンドラーロジックを含みます。
    8. **shared/files**フォルダー：エージェントアプリによって作成されたファイルを含みます。
    9. **shared/instructions**フォルダー：LLMに渡される指示を含みます。

    ![ラボフォルダー構造](../media/project-structure-self-guided-python.png)

=== "C#"

    ## ワークショップの設定

    1. ターミナルを開き、**src/csharp/workshop/AgentWorkshop.Client**フォルダーに移動します。

        ```powershell
        cd build-your-first-agent-with-azure-ai-agent-service-workshop\src\csharp\workshop\AgentWorkshop.Client
        ```

    2. Azure AI Foundryからコピーしたプロジェクトエンドポイントをユーザーシークレットに追加します。

        ```powershell
        dotnet user-secrets set "ConnectionStrings:AiAgentService" "<your_project_endpoint>"
        ```

    3. **モデルデプロイ名**をユーザーシークレットに追加します。

        ```powershell
        dotnet user-secrets set "Azure:ModelName" "gpt-4o"
        ```

    4. Bing検索によるグラウンディング用の**Bing接続ID**をユーザーシークレットに追加します。

        ```powershell
        $subId = $(az account show --query id --output tsv)
        $rgName = "rg-agent-workshop"
        $aiAccount = "<ai_account_name>" # 実際のAIアカウント名に置き換えてください
        $aiProject = "<ai_project_name>" # 実際のAIプロジェクト名に置き換えてください
        $bingConnectionId = "/subscriptions/$subId/resourceGroups/$rgName/providers/Microsoft.CognitiveServices/accounts/$aiAccount/projects/$aiProject/connections/groundingwithbingsearch"
        dotnet user-secrets set "Azure:BingConnectionId" "$bingConnectionId"
        ```

    ## プロジェクト構造

    ワークショップ全体で作業する主要な**サブフォルダー**と**ファイル**を必ず理解してください。

    ### workshopフォルダー

    - **Lab1.cs、Lab2.cs、Lab3.cs**ファイル：各ラボのエントリーポイントで、エージェントロジックを含みます。
    - **Program.cs**ファイル：アプリのエントリーポイントで、メインロジックを含みます。
    - **SalesData.cs**ファイル：SQLiteデータベースに対して動的SQLクエリを実行する関数ロジック。

    ### sharedフォルダー

    - **files**フォルダー：エージェントアプリによって作成されたファイルを含みます。
    - **fonts**フォルダー：コードインタープリターが使用する多言語フォントを含みます。
    - **instructions**フォルダー：LLMに渡される指示を含みます。

    ![ラボフォルダー構造](../media/project-structure-self-guided-csharp.png)

## プロティップス

!!! tips
    1. ラボ環境の右側パネルの**ハンバーガーメニュー**は、**スプリットウィンドウビュー**やラボを終了するオプションなどの追加機能を提供します。**スプリットウィンドウビュー**により、ラボ環境を全画面表示に最大化でき、画面スペースを最適化できます。ラボの**指示**と**リソース**パネルは別ウィンドウで開きます。
    2. ラボ環境で指示のスクロールが遅い場合は、指示のURLをコピーして**お使いのコンピューターのローカルブラウザー**で開くと、よりスムーズな体験ができます。
    3. 画像の表示に問題がある場合は、単に**画像をクリックして拡大**してください。

*GitHub Copilot を使用して翻訳されました。*
