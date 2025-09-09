## Microsoftイベント参加者

このページの指示は、イベントに参加し、事前構成されたラボ環境にアクセスできることを前提としています。この環境は、ワークショップを完了するために必要なすべてのツールとリソースを備えたAzureサブスクリプションを提供します。

## はじめに

このワークショップは、Azure AI Agents Serviceと関連する[SDK](https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme?context=%2Fazure%2Fai-services%2Fagents%2Fcontext%2Fcontext){:target="_blank"}について教えることを目的としています。Azure AI Agents Serviceの特定の機能を強調する複数のラボから構成されています。各ラボは前のラボの知識と作業の上に構築されるため、順番に完了することを意図しています。

## ワークショップクラウドリソース

以下のリソースがラボAzureサブスクリプションに事前プロビジョニングされています：

- **rg-zava-agent-wks-nnnnnnnn**という名前のリソースグループ
- **fdy-zava-agent-wks-nnnnnnnn**という名前の**Azure AI Foundryハブ**
- **prj-zava-agent-wks-nnnnnnnn**という名前の**Azure AI Foundryプロジェクト**
- 2つのモデルがデプロイされています：**gpt-4o-mini**と**text-embedding-3-small**。[料金を確認。](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/){:target="\_blank"}
- **pg-zava-agent-wks-nnnnnnnn**という名前のAzure Database for PostgreSQL Flexible Server（B1ms Burstable 32GB）データベース。[料金を確認](https://azure.microsoft.com/pricing/details/postgresql/flexible-server){:target="\_blank"}
- **appi-zava-agent-wks-nnnnnnnn**という名前のApplication Insightsリソース。[料金を確認](https://azure.microsoft.com/pricing/calculator/?service=monitor){:target="\_blank"}

## ワークショッププログラミング言語の選択

ワークショップはPythonとC#の両方で利用できます。言語セレクタータブを使用して、ラボルームまたは好みに合った言語を必ず選択してください。注意：ワークショップの途中で言語を変更しないでください。

**ラボルームに合った言語タブを選択してください：**

=== "Python"
    ワークショップのデフォルト言語は**Python**に設定されています。
=== "C#"
    ワークショップのデフォルト言語は**C#**に設定されています。

    !!! warning "このワークショップのC#/.NETバージョンはベータ版で、既知の安定性問題があります。"

    ワークショップを開始する**前に**、[トラブルシューティングガイド](../../en/dotnet-troubleshooting.md)セクションを必ずお読みください。そうでなければ、ワークショップの**Python**バージョンを選択してください。

## Azureでの認証

エージェントアプリがAzure AI Agents Serviceとモデルにアクセスできるよう、Azureで認証する必要があります。以下の手順に従ってください：

1. ターミナルウィンドウを開きます。ターミナルアプリはWindows 11のタスクバーに**ピン留め**されています。

    ![ターミナルウィンドウを開く](../../media/windows-taskbar.png){ width="300" }

2. 以下のコマンドを実行してAzureで認証します：

    ```powershell
    az login
    ```

    !!! note
        ブラウザリンクを開いてAzureアカウントにログインするよう促されます。

        1. ブラウザウィンドウが自動的に開きます。**職場または学校アカウント**を選択し、**続行**を選択してください。
        1. ラボ環境の**Resources**タブの**上部セクション**にある**Username**と**TAP（Temporary Access Pass）**を使用してください。
        1. **はい、すべてのアプリ**を選択してください
        1. **完了**を選択してください

3. 次に、コマンドラインから**Enter**を選択して**Default**サブスクリプションを選択します。

4. 次のステップのためにターミナルウィンドウを開いたままにしておきます。

## DevTunnelサービスでの認証

DevTunnelにより、ワークショップ中にAzure AI Agents ServiceがローカルMCPサーバーにアクセスできるようになります。

```powershell
devtunnel login
```

!!! note
    `az login`に使用したアカウントを使用するよう促されます。アカウントを選択して続行してください。

次のステップのためにターミナルウィンドウを開いたままにしておきます。

## ワークショップを開く

Visual Studio Codeでワークショップを開くには以下の手順に従ってください：

=== "Python"

    以下のコマンドブロックは、ワークショップリポジトリを更新し、Python仮想環境をアクティベートし、VS Codeでプロジェクトを開きます。

    以下のコマンドブロックをコピーしてターミナルに貼り付け、**Enter**を押してください。

    ```powershell
    ; cd $HOME\aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol `
    ; git pull `
    ; .\src\python\workshop\.venv\Scripts\activate `
    ; code .vscode\python-workspace.code-workspace
    ```

    !!! warning "プロジェクトがVS Codeで開くと、右下に2つの通知が表示されます。両方の通知を閉じるために✖をクリックしてください。"

=== "C#"

    === "VS Code"

        1. Visual Studio Codeでワークショップを開きます。ターミナルウィンドウから、以下のコマンドを実行します：

            ```powershell
            ; cd $HOME\aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol `
            ; git pull `
            ;code .vscode\csharp-workspace.code-workspace
            ```

        !!! note "プロジェクトがVS Codeで開くと、右下にC#拡張機能をインストールする通知が表示されます。C#開発に必要な機能を提供するため、**Install**をクリックしてC#拡張機能をインストールしてください。"

    === "Visual Studio 2022"

        2. Visual Studio 2022でワークショップを開きます。ターミナルウィンドウから、以下のコマンドを実行します：

            ```powershell
            ; git pull `
            ;cd $HOME; start .\aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol\src\csharp\McpAgentWorkshop.slnx
            ```

            !!! note "ソリューションを開くプログラムを尋ねられることがあります。**Visual Studio 2022**を選択してください。"

## プロジェクト構造

=== "Python"

    ワークショップを通して作業する重要な**サブフォルダ**と**ファイル**について理解してください。

    5. **main.py**ファイル：メインロジックを含むアプリのエントリーポイント。
    6. **sales_data.py**ファイル：SQLiteデータベースに対する動的SQLクエリを実行する機能ロジック。
    7. **stream_event_handler.py**ファイル：トークンストリーミング用のイベントハンドラーロジックを含みます。
    8. **shared/files**フォルダ：エージェントアプリが作成したファイルを含みます。
    9. **shared/instructions**フォルダ：LLMに渡される指示を含みます。

    ![Lab folder structure](../../media/project-structure-self-guided-python.png)

=== "C#"

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

    ![Lab folder structure](../../media/project-structure-self-guided-csharp.png)

## プロティップ

!!! tips
    1. ラボ環境の右パネルの**ハンバーガーメニュー**では、**Split Window View**やラボ終了オプションを含む追加機能が提供されます。**Split Window View**により、ラボ環境を全画面に最大化でき、画面スペースを最適化します。ラボの**Instructions**と**Resources**パネルが別ウィンドウで開きます。
