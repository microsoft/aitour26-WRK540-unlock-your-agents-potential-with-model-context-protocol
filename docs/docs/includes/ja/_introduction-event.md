## Microsoft イベント参加者

このページの指示は、[Microsoft Event 2025](https://build.microsoft.com/){:target="_blank"} に参加し、事前設定されたラボ環境にアクセスできることを前提としています。この環境は、ワークショップを完了するために必要なすべてのツールとリソースを含む Azure サブスクリプションを提供します。

## はじめに

このワークショップは、Azure AI Agents Service と関連する [SDK](https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme?context=%2Fazure%2Fai-services%2Fagents%2Fcontext%2Fcontext){:target="_blank"} について学習するよう設計されています。Azure AI Agents Service の特定の機能をハイライトする複数のラボで構成されています。各ラボは前のラボの知識と作業に基づいて構築されるため、順番に完了することを意図しています。

## ワークショッププログラミング言語の選択

ワークショップは Python と C# の両方で利用できます。言語セレクタータブを使用して、参加しているラボルームに適した言語を選択してください。ワークショップ途中で言語を切り替えないでください。

**ラボルームに対応する言語タブを選択してください：**

=== "Python"
    ワークショップのデフォルト言語は **Python** に設定されています。
=== "C#"
    ワークショップのデフォルト言語は **C#** に設定されています。

## Azure での認証

エージェントアプリが Azure AI Agents Service とモデルにアクセスできるよう、Azure で認証する必要があります。以下の手順に従ってください：

1. ターミナルウィンドウを開きます。ターミナルアプリは Windows 11 タスクバーに**ピン留め**されています。

    ![端末ウィンドウを開く](../media/windows-taskbar.png){ width="300" }

2. 次のコマンドを実行して Azure で認証します：

    ```powershell
    az login
    ```

    !!! note
        ブラウザリンクを開いて Azure アカウントにログインするよう求められます。

        1. ブラウザウィンドウが自動的に開くので、**職場または学校アカウント**を選択し、**次へ**をクリックします。

        1. ラボ環境の**リソース**タブの**上部セクション**にある**ユーザー名**と**パスワード**を使用します。

        2. **OK**を選択し、次に**完了**を選択します。

3. コマンドラインから**Enter**をクリックして**デフォルト**サブスクリプションを選択します。

4. ログインしたら、次のコマンドを実行してリソースグループに**ユーザー**ロールを割り当てます：

    ```powershell
    $subId = $(az account show --query id --output tsv) `
    ;$objectId = $(az ad signed-in-user show --query id -o tsv) `
    ; az role assignment create --role "f6c7c914-8db3-469d-8ca1-694a8f32e121" --assignee-object-id $objectId --scope /subscriptions/$subId/resourceGroups/"rg-agent-workshop" --assignee-principal-type 'User'
    ```

5. 次のステップのためにターミナルウィンドウを開いたままにしておきます。

## ワークショップを開く

Visual Studio Code でワークショップを開くには、以下の手順に従ってください：

=== "Python"

      1. ターミナルウィンドウから、次のコマンドを実行してワークショップリポジトリをクローンし、関連フォルダに移動し、仮想環境をセットアップし、アクティベートし、必要なパッケージをインストールします：

          ```powershell
          git clone https://github.com/microsoft/build-your-first-agent-with-azure-ai-agent-service-workshop.git `
          ; cd build-your-first-agent-with-azure-ai-agent-service-workshop `
          ; python -m venv src/python/workshop/.venv `
          ; src\python\workshop\.venv\Scripts\activate `
          ; pip install -r src/python/workshop/requirements.txt `
          ; code --install-extension tomoki1207.pdf
          ```

      2. VS Code で開きます。ターミナルウィンドウから、次のコマンドを実行します：

          ```powershell
          code .vscode\python-workspace.code-workspace
          ```

        !!! warning "VS Code でプロジェクトが開くと、右下角に2つの通知が表示されます。両方の通知を閉じるために ✖ をクリックしてください。"

=== "C#"

    1. ターミナルウィンドウから、次のコマンドを実行してワークショップリポジトリをクローンします：

        ```powershell
        git clone https://github.com/microsoft/build-your-first-agent-with-azure-ai-agent-service-workshop.git
        ```

    === "VS Code"

        1. Visual Studio Code でワークショップを開きます。ターミナルウィンドウから、次のコマンドを実行します：

            ```powershell
            code build-your-first-agent-with-azure-ai-agent-service-workshop\.vscode\csharp-workspace.code-workspace
            ```

        !!! note "VS Code でプロジェクトが開くと、右下角に C# 拡張機能をインストールする通知が表示されます。C# 開発に必要な機能を提供するため、**インストール**をクリックして C# 拡張機能をインストールしてください。"

    === "Visual Studio 2022"

        1. Visual Studio 2022 でワークショップを開きます。ターミナルウィンドウから、次のコマンドを実行します：

            ```powershell
            start build-your-first-agent-with-azure-ai-agent-service-workshop\src\csharp\workshop\AgentWorkshop.sln
            ```

            !!! note "ソリューションを開くプログラムを尋ねられる場合があります。**Visual Studio 2022** を選択してください。"

## Azure AI Foundry プロジェクトエンドポイント

次に、エージェントアプリが Azure AI Agents Service に接続するために使用するプロジェクトエンドポイントを取得するため、Azure AI Foundry にログインします。

1. [Azure AI Foundry](https://ai.azure.com){:target="_blank"} ウェブサイトに移動します。
2. **サインイン**を選択し、ラボ環境の**リソース**タブの**上部セクション**にある**ユーザー名**と**パスワード**を使用します。**ユーザー名**と**パスワード**フィールドをクリックして、ログイン詳細を自動的に入力します。
    ![Azure 認証情報](../media/azure-credentials.png){:width="500"}
3. Azure AI Foundry の紹介を読み、**了解**をクリックします。
4. [すべてのリソース](https://ai.azure.com/AllResources){:target="_blank"} に移動して、事前プロビジョニングされた AI リソースのリストを表示します。
5. **Project** タイプの **aip-** で始まるリソース名を選択します。

    ![プロジェクトを選択](../media/ai-foundry-project.png){:width="500"}

6. 紹介ガイドを確認し、**閉じる**をクリックします。
7. **概要**サイドバーメニューから、**エンドポイントとキー** -> **ライブラリ** -> **Azure AI Foundry** セクションを見つけ、**コピー**アイコンをクリックして **Azure AI Foundry プロジェクトエンドポイント**をコピーします。

    ![接続文字列をコピー](../media/project-connection-string.png){:width="500"}

=== "Python"

    ## ワークショップを設定する

    1. VS Code で開いたワークショップに戻ります。
    2. `.env.sample` ファイルを `.env` に**名前変更**します。

        - VS Code **エクスプローラー**パネルで **.env.sample** ファイルを選択します。
        - ファイルを右クリックして**名前の変更**を選択するか、<kbd>F2</kbd> を押します。
        - ファイル名を `.env` に変更し、<kbd>Enter</kbd> を押します。

    3. Azure AI Foundry からコピーした**プロジェクトエンドポイント**を `.env` ファイルに貼り付けます。

        ```python
        PROJECT_ENDPOINT="<your_project_endpoint>"
        ```

        `.env` ファイルは次のようになりますが、あなたのプロジェクトエンドポイントが含まれます。

        ```python
        PROJECT_ENDPOINT="<your_project_endpoint>"
        MODEL_DEPLOYMENT_NAME="<your_model_deployment_name>"
        DEV_TUNNEL_URL="<your_dev_tunnel_url>"
        ```

    4. `.env` ファイルを保存します。

    ## プロジェクト構造

    ワークショップ全体を通して作業する主要な**サブフォルダ**と**ファイル**について必ず理解しておいてください。

    5. **app.py** ファイル: アプリのエントリーポイントで、主要なロジックが含まれています。
    6. **sales_data.py** ファイル: SQLite データベースに対する動的 SQL クエリを実行する関数ロジックです。
    7. **stream_event_handler.py** ファイル: トークンストリーミングのイベントハンドラーロジックが含まれています。
    8. **shared/files** フォルダ: エージェントアプリによって作成されたファイルが含まれています。
    9. **shared/instructions** フォルダ: LLM に渡される指示が含まれています。

    ![ラボフォルダ構造](../media/project-structure-self-guided-python.png)

=== "C#"

    ## ワークショップを設定する

    1. ターミナルを開き、**src/csharp/workshop/AgentWorkshop.Client** フォルダに移動します。

        ```powershell
        cd build-your-first-agent-with-azure-ai-agent-service-workshop\src\csharp\workshop\AgentWorkshop.Client
        ```

    2. Azure AI Foundry からコピーした**プロジェクトエンドポイント**をユーザーシークレットに追加します。

        ```powershell
        dotnet user-secrets set "ConnectionStrings:AiAgentService" "<your_project_endpoint>"
        ```

    3. **モデルデプロイメント名**をユーザーシークレットに追加します。

        ```powershell
        dotnet user-secrets set "Azure:ModelName" "gpt-4o"
        ```

    4. Bing 検索でのグラウンディングのために **Bing 接続 ID** をユーザーシークレットに追加します。

        ```powershell
        $subId = $(az account show --query id --output tsv)
        $rgName = "rg-agent-workshop"
        $aiAccount = "<ai_account_name>" # 実際の AI アカウント名に置き換えてください
        $aiProject = "<ai_project_name>" # 実際の AI プロジェクト名に置き換えてください
        $bingConnectionId = "/subscriptions/$subId/resourceGroups/$rgName/providers/Microsoft.CognitiveServices/accounts/$aiAccount/projects/$aiProject/connections/groundingwithbingsearch"
        dotnet user-secrets set "Azure:BingConnectionId" "$bingConnectionId"
        ```

    ## プロジェクト構造

    ワークショップ全体を通して作業する主要な**サブフォルダ**と**ファイル**について必ず理解しておいてください。

    ### workshop フォルダ

    - **Lab1.cs、Lab2.cs、Lab3.cs** ファイル: 各ラボのエントリーポイントで、エージェントロジックが含まれています。
    - **Program.cs** ファイル: アプリのエントリーポイントで、主要なロジックが含まれています。
    - **SalesData.cs** ファイル: SQLite データベースに対する動的 SQL クエリを実行する関数ロジックです。

    ### shared フォルダ

    - **files** フォルダ: エージェントアプリによって作成されたファイルが含まれています。
    - **fonts** フォルダ: Code Interpreter で使用される多言語フォントが含まれています。
    - **instructions** フォルダ: LLM に渡される指示が含まれています。

    ![ラボフォルダ構造](../media/project-structure-self-guided-csharp.png)

## プロのヒント

!!! tips
    1. ラボ環境の右側パネルの**ハンバーガーメニュー**には、**分割ウィンドウビュー**やラボを終了するオプションなど、追加機能が提供されています。**分割ウィンドウビュー**により、ラボ環境を全画面に最大化し、スクリーン空間を最適化できます。ラボの**指示**と**リソース**パネルは別ウィンドウで開きます。
    2. ラボ環境で指示のスクロールが遅い場合は、指示の URL をコピーして**お使いのコンピュータのローカルブラウザ**で開くと、よりスムーズな体験ができます。
    3. 画像の表示に問題がある場合は、**画像をクリックして拡大**してください。

*Translated using GitHub Copilot and GPT-4o.*
