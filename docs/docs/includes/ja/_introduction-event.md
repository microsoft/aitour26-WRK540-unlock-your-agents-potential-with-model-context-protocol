## Microsoftイベント参加者

このページの指示は、[Microsoft Event 2025](https://build.microsoft.com/){:target="_blank"}に参加し、事前構成されたラボ環境にアクセスできることを前提としています。この環境は、ワークショップを完了するために必要なすべてのツールとリソースを備えたAzureサブスクリプションを提供します。

## はじめに

このワークショップは、Azure AI Agents Serviceと関連する[SDK](https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme?context=%2Fazure%2Fai-services%2Fagents%2Fcontext%2Fcontext){:target="_blank"}について教えることを目的としています。Azure AI Agents Serviceの特定の機能を強調する複数のラボから構成されています。各ラボは前のラボの知識と作業の上に構築されるため、順番に完了することを意図しています。

## ワークショッププログラミング言語の選択

ワークショップはPythonとC#の両方で利用できます。言語セレクタータブを使用して、参加しているラボルームに合った言語を必ず選択してください。注意：ワークショップの途中で言語を変更しないでください。

**ラボルームに合った言語タブを選択してください：**

=== "Python"
    ワークショップのデフォルト言語は**Python**に設定されています。
=== "C#"
    ワークショップのデフォルト言語は**C#**に設定されています。

## Azureでの認証

エージェントアプリがAzure AI Agents Serviceとモデルにアクセスできるよう、Azureで認証する必要があります。以下の手順に従ってください：

1. ターミナルウィンドウを開きます。ターミナルアプリはWindows 11のタスクバーに**ピン留め**されています。

    ![ターミナルウィンドウを開く](../media/windows-taskbar.png){ width="300" }

2. 以下のコマンドを実行してAzureで認証します：

    ```powershell
    az login
    ```

    !!! note
        ブラウザリンクを開いてAzureアカウントにログインするよう促されます。

        1. ブラウザウィンドウが自動的に開きます。**職場または学校アカウント**を選択し、**続行**を選択してください。

        1. ラボ環境の**Resources**タブの**上部セクション**にある**Username**と**Password**を使用してください。

        2. **はい、すべてのアプリ**を選択してください

3. 次に、コマンドラインから**Enter**を選択して**Default**サブスクリプションを選択します。

4. ログイン後、以下のコマンドを実行してリソースグループに**user**ロールを割り当てます：

    ```powershell
    $subId = $(az account show --query id --output tsv) `
    ;$objectId = $(az ad signed-in-user show --query id -o tsv) `
    ; az role assignment create --role "f6c7c914-8db3-469d-8ca1-694a8f32e121" --assignee-object-id $objectId --scope /subscriptions/$subId/resourceGroups/"rg-agent-workshop" --assignee-principal-type 'User'
    ```

5. 次のステップのためにターミナルウィンドウを開いたままにしておきます。

## ワークショップを開く

Visual Studio Codeでワークショップを開くには以下の手順に従ってください：

=== "Python"

      1. ターミナルウィンドウから、以下のコマンドを実行してワークショップリポジトリをクローン、関連フォルダへ移動、仮想環境の設定、アクティベート、必要パッケージのインストールを行います：

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

        !!! warning "プロジェクトがVS Codeで開くと、右下に2つの通知が表示されます。両方の通知を閉じるために✖をクリックしてください。"

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

        !!! note "プロジェクトがVS Codeで開くと、右下にC#拡張機能をインストールする通知が表示されます。C#開発に必要な機能を提供するため、**Install**をクリックしてC#拡張機能をインストールしてください。"

    === "Visual Studio 2022"

        1. Visual Studio 2022でワークショップを開きます。ターミナルウィンドウから、以下のコマンドを実行します：

            ```powershell
            start build-your-first-agent-with-azure-ai-agent-service-workshop\src\csharp\workshop\AgentWorkshop.sln
            ```

            !!! note "ソリューションを開くプログラムを尋ねられることがあります。**Visual Studio 2022**を選択してください。"

## Azure AI Foundryプロジェクトエンドポイント

次に、Azure AI Foundryにログインして、エージェントアプリがAzure AI Agents Serviceに接続するために使用するプロジェクトエンドポイントを取得します。

1. [Azure AI Foundry](https://ai.azure.com){:target="_blank"}ウェブサイトに移動します。
2. **Sign in**を選択し、ラボ環境の**Resources**タブの**上部セクション**にある**Username**と**Password**を使用します。**Username**と**Password**フィールドをクリックすると、ログイン詳細が自動的に入力されます。
    ![Azure credentials](../media/azure-credentials.png){:width="500"}
3. Azure AI Foundryの紹介を読み、**Got it**をクリックします。
4. [All Resources](https://ai.azure.com/AllResources){:target="_blank"}に移動して、事前プロビジョニングされたAIリソースのリストを表示します。
5. **aip-**で始まるタイプ**Project**のリソース名を選択します。

    ![Select project](../media/ai-foundry-project.png){:width="500"}

6. 紹介ガイドを確認し、**Close**をクリックします。
7. **Overview**サイドバーメニューから、**Endpoints and keys** -> **Libraries** -> **Azure AI Foundry**セクションを見つけ、**Copy**アイコンをクリックして**Azure AI Foundryプロジェクトエンドポイント**をコピーします。

    ![Copy connection string](../media/project-connection-string.png){:width="500"}

=== "Python"

    ## ワークショップを設定する

    1. VS Codeで開いたワークショップに戻ります。
    2. `.env.sample`ファイルを`.env`に**名前変更**します。

        - VS Code **Explorer**パネルで**.env.sample**ファイルを選択します。
        - ファイルを右クリックして**Rename**を選択するか、<kbd>F2</kbd>を押します。
        - ファイル名を`.env`に変更し、<kbd>Enter</kbd>を押します。

    3. Azure AI Foundryからコピーした**Project endpoint**を`.env`ファイルに貼り付けます。

        ```python
        PROJECT_ENDPOINT="<your_project_endpoint>"
        ```

        `.env`ファイルは以下のようになりますが、あなたのプロジェクトエンドポイントが入ります。

        ```python
        PROJECT_ENDPOINT="<your_project_endpoint>"
        MODEL_DEPLOYMENT_NAME="<your_model_deployment_name>"
        DEV_TUNNEL_URL="<your_dev_tunnel_url>"
        ```

    4. `.env`ファイルを保存します。

    ## プロジェクト構造

    ワークショップを通して作業する重要な**サブフォルダ**と**ファイル**について理解してください。

    5. **app.py**ファイル：メインロジックを含むアプリのエントリーポイント。
    6. **sales_data.py**ファイル：SQLiteデータベースに対する動的SQLクエリを実行する機能ロジック。
    7. **stream_event_handler.py**ファイル：トークンストリーミング用のイベントハンドラーロジックを含みます。
    8. **shared/files**フォルダ：エージェントアプリが作成したファイルを含みます。
    9. **shared/instructions**フォルダ：LLMに渡される指示を含みます。

    ![Lab folder structure](../media/project-structure-self-guided-python.png)

=== "C#"

    ## ワークショップを設定する

    1. ターミナルを開き、**src/csharp/workshop/AgentWorkshop.Client**フォルダに移動します。

        ```powershell
        cd build-your-first-agent-with-azure-ai-agent-service-workshop\src\csharp\workshop\AgentWorkshop.Client
        ```

    2. Azure AI Foundryからコピーした**Project endpoint**をユーザーシークレットに追加します。

        ```powershell
        dotnet user-secrets set "ConnectionStrings:AiAgentService" "<your_project_endpoint>"
        ```

    3. **Model deployment name**をユーザーシークレットに追加します。

        ```powershell
        dotnet user-secrets set "Azure:ModelName" "gpt-4o"
        ```

    4. Bing検索との根拠付けのために**Bing connection ID**をユーザーシークレットに追加します。

        ```powershell
        $subId = $(az account show --query id --output tsv)
        $rgName = "rg-agent-workshop"
        $aiAccount = "<ai_account_name>" # 実際のAIアカウント名に置き換えてください
        $aiProject = "<ai_project_name>" # 実際のAIプロジェクト名に置き換えてください
        $bingConnectionId = "/subscriptions/$subId/resourceGroups/$rgName/providers/Microsoft.CognitiveServices/accounts/$aiAccount/projects/$aiProject/connections/groundingwithbingsearch"
        dotnet user-secrets set "Azure:BingConnectionId" "$bingConnectionId"
        ```

    ## プロジェクト構造

    ワークショップを通して作業する重要な**サブフォルダ**と**ファイル**について理解してください。

    ### workshopフォルダ

    - **Lab1.cs, Lab2.cs, Lab3.cs**ファイル：各ラボのエントリーポイントで、エージェントロジックを含みます。
    - **Program.cs**ファイル：メインロジックを含むアプリのエントリーポイント。
    - **SalesData.cs**ファイル：SQLiteデータベースに対する動的SQLクエリを実行する機能ロジック。

    ### sharedフォルダ

    - **files**フォルダ：エージェントアプリが作成したファイルを含みます。
    - **fonts**フォルダ：Code Interpreterが使用する多言語フォントを含みます。
    - **instructions**フォルダ：LLMに渡される指示を含みます。

    ![Lab folder structure](../media/project-structure-self-guided-csharp.png)

## プロティップ

!!! tips
    1. ラボ環境の右パネルの**ハンバーガーメニュー**では、**Split Window View**やラボ終了オプションを含む追加機能が提供されます。**Split Window View**により、ラボ環境を全画面に最大化でき、画面スペースを最適化します。ラボの**Instructions**と**Resources**パネルが別ウィンドウで開きます。
    2. ラボ環境でラボ指示のスクロールが遅い場合は、指示のURLをコピーして**自分のコンピューターのローカルブラウザ**で開くことで、よりスムーズな体験が得られます。
    3. 画像の表示に問題がある場合は、単純に**画像をクリックして拡大**してください。
