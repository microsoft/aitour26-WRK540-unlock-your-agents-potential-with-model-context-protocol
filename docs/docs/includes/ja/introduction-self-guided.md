## セルフガイド学習者向け

これらの手順は、事前設定されたラボ環境にアクセスできないセルフガイド学習者向けのものです。以下の手順に従って環境を設定し、ワークショップを開始してください。

## はじめに

このワークショップは、Azure AI エージェントサービスと関連するSDKについて学習するために設計されています。複数のラボで構成されており、各ラボはAzure AI エージェントサービスの特定の機能をハイライトしています。各ラボは前のラボの知識と作業に基づいているため、順番に完了することを意図しています。

## 前提条件

1. Azureサブスクリプションへのアクセス。Azureサブスクリプションをお持ちでない場合は、開始する前に[無料アカウント](https://azure.microsoft.com/free/){:target="_blank"}を作成してください。
1. GitHubアカウントが必要です。お持ちでない場合は、[GitHub](https://github.com/join){:target="_blank"}で作成してください。

## ワークショップのプログラミング言語を選択

ワークショップはPythonとC#の両方で利用可能です。言語セレクタータブを使用して、お好みの言語を選択してください。なお、ワークショップの途中で言語を変更しないでください。

**お好みの言語のタブを選択してください：**

=== "Python"
    ワークショップのデフォルト言語は**Python**に設定されています。
=== "C#"
    ワークショップのデフォルト言語は**C#**に設定されています。

    !!! warning "このワークショップのC#/.NETバージョンはベータ版であり、既知の安定性の問題があります。"

    ワークショップを開始する**前に**、[トラブルシューティングガイド](../../ja/dotnet-troubleshooting.md)セクションを必ずお読みください。それ以外の場合は、ワークショップの**Python**バージョンを選択してください。

## ワークショップを開く

推奨：必要なツールが全て事前設定された**GitHub Codespaces**。または、Visual Studio Code **Dev Container**と**Docker**を使用してローカルで実行することもできます。下記のタブを使用して選択してください。

!!! Tip
    CodespacesやDev Containerのビルドには約5分かかります。ビルドを開始した後、完了するまでの間に**読み続けて**ください。

=== "GitHub Codespaces"

    **Open in GitHub Codespaces**を選択して、GitHub CodespacesでプロジェクトToしてください。

    [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/microsoft/aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol){:target="_blank"}

=== "VS Code Dev Container"

    1. ローカルマシンに以下がインストールされていることを確認してください：

        - [Docker](https://docs.docker.com/get-docker/){:target="\_blank"}
        - [Visual Studio Code](https://code.visualstudio.com/download){:target="\_blank"}
        - [Remote - Containers拡張機能](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers){:target="\_blank"}
    1. ローカルマシンにリポジトリをクローンします：

        ```bash
        git clone https://github.com/microsoft/aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol.git
        ```

    1. Visual Studio Codeでクローンしたリポジトリを開きます。
    1. プロンプトが表示されたら、**Reopen in Container**を選択してプロジェクトをDev Containerで開きます。

---

## Azureサービスの認証

!!! danger
続行する前に、CodespaceまたはDev Containerが完全にビルドされて準備ができていることを確認してください。

### DevTunnelでの認証

DevTunnelは、ワークショップで使用されるポート転送サービスで、Azure AI エージェントサービスがローカル開発環境で実行しているMCPサーバーにアクセスできるようにします。認証するには以下の手順に従ってください：

1. VS Codeで、<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>`</kbd>を**押して**新しいターミナルウィンドウを開きます。次に以下のコマンドを実行します：
1. **以下のコマンドを実行して**DevTunnelで認証します：

   ```shell
   devtunnel login
   ```

1. 認証するには以下の手順に従ってください：

   1. **認証コード**をクリップボードにコピーします。
   2. <kbd>ctrl</kbd>または<kbd>cmd</kbd>キーを**押し続けます**。
   3. 認証URLを**選択して**ブラウザで開きます。
   4. コードを**貼り付けて**、**次へ**をクリックします。
   5. **アカウントを選択**してサインインします。
   6. **続行**を選択します
   7. VS Codeのターミナルウィンドウに**戻ります**。

1. 次の手順のためにターミナルウィンドウを**開いたまま**にしておきます。

### Azureでの認証

エージェントアプリがAzure AI エージェントサービスとモデルにアクセスできるようにするため、Azureで認証します。以下の手順に従ってください：

1. 次に以下のコマンドを実行します：

    ```shell
    az login --use-device-code
    ```

    !!! warning
    複数のAzureテナントがある場合は、以下を使用して正しいテナントを指定してください：

    ```shell
    az login --use-device-code --tenant <tenant_id>
    ```

2. 認証するには以下の手順に従ってください：

    1. **認証コード**をクリップボードに**コピー**します。
    2. <kbd>ctrl</kbd>または<kbd>cmd</kbd>キーを**押し続けます**。
    3. 認証URLを**選択して**ブラウザで開きます。
    4. コードを**貼り付けて**、**次へ**をクリックします。
    5. **アカウントを選択**してサインインします。
    6. **続行**を選択します
    7. VS Codeのターミナルウィンドウに**戻ります**。
    8. プロンプトが表示されたら、**サブスクリプションを選択**します。

3. 次の手順のためにターミナルウィンドウを開いたままにしておきます。

---

## Azureリソースのデプロイ

このデプロイメントは、Azureサブスクリプションに以下のリソースを作成します。

- **rg-zava-agent-wks-nnnnnnnn**という名前のリソースグループ
- **fdy-zava-agent-wks-nnnnnnnn**という名前の**Azure AI Foundryハブ**
- **prj-zava-agent-wks-nnnnnnnn**という名前の**Azure AI Foundryプロジェクト**
- 2つのモデルがデプロイされます：**gpt-4o-mini**と**text-embedding-3-small**。[価格を参照。](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/){:target="\_blank"}
- **appi-zava-agent-wks-nnnnnnnn**という名前のApplication Insightsリソース。[価格を参照](https://azure.microsoft.com/pricing/calculator/?service=monitor){:target="\_blank"}
- ワークショップのコストを低く抑えるため、PostgreSQLはクラウドサービスではなく、CodespaceまたはDev Container内のローカルコンテナで実行されます。マネージドPostgreSQLサービスのオプションについては、[Azure Database for PostgreSQL Flexible Server](https://azure.microsoft.com/en-us/products/postgresql){:target="\_blank"}をご覧ください。

!!! warning "以下の最低限のモデルクォータがあることを確認してください" - gpt-4o-mini Global Standard SKUの120K TPMクォータ（エージェントが頻繁にモデル呼び出しを行うため）。 - text-embedding-3-small モデル Global Standard SKUの50K TPM。 - [AI Foundry管理センター](https://ai.azure.com/managementCenter/quota){:target="\_blank"}でクォータを確認してください。"

### 自動デプロイ

以下のbashスクリプトを実行して、ワークショップに必要なリソースのデプロイを自動化します。`deploy.sh`スクリプトはデフォルトで`westus`リージョンにリソースをデプロイします。スクリプトを実行するには：

```bash
cd infra && ./deploy.sh
```

### ワークショップの構成

=== "Python"

    #### Azureリソース構成

    デプロイスクリプトは**.env**ファイルを生成します。これには、プロジェクトとモデルエンドポイント、モデルデプロイメント名、およびApplication Insights接続文字列が含まれます。.envファイルは`src/python/workshop`フォルダーに自動的に保存されます。

    **.env**ファイルは以下のようになり、あなたの値で更新されます：

    ```python
    PROJECT_ENDPOINT="<your_project_endpoint>"
    GPT_MODEL_DEPLOYMENT_NAME="<your_model_deployment_name>"
    EMBEDDING_MODEL_DEPLOYMENT_NAME="<your_embedding_model_deployment_name>"
    APPLICATIONINSIGHTS_CONNECTION_STRING="<your_application_insights_connection_string>"
    AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED="true"
    AZURE_OPENAI_ENDPOINT="<your_azure_openai_endpoint>"
    ```

    #### Azureリソース名

    また、`workshop`フォルダーに`resources.txt`という名前のファイルもあります。このファイルには、デプロイ中に作成されたAzureリソースの名前が含まれています。

    以下のような内容になります：

    ```plaintext
    Azure AI Foundry Resources:
    - Resource Group Name: rg-zava-agent-wks-nnnnnnnn
    - AI Project Name: prj-zava-agent-wks-nnnnnnnn
    - Foundry Resource Name: fdy-zava-agent-wks-nnnnnnnn
    - Application Insights Name: appi-zava-agent-wks-nnnnnnnn
    ```

=== "C#"

    スクリプトは[ASP.NET Core開発シークレット](https://learn.microsoft.com/aspnet/core/security/app-secrets){:target="_blank"}のSecret Managerを使用してプロジェクト変数を安全に保存します。

    VS CodeでC#ワークスペースを開いた後、以下のコマンドを実行してシークレットを表示できます：

    ```bash
    dotnet user-secrets list
    ```

---

## VS Codeワークスペースを開く

ワークショップには、PythonとC#用の2つのVS Codeワークスペースがあります。ワークスペースには、各言語のラボを完了するために必要なソースコードとすべてのファイルが含まれています。作業したい言語に合ったワークスペースを選択してください。

=== "Python"

    1. 以下のパスをクリップボードに**コピー**します：

        ```text
        /workspace/.vscode/python-workspace.code-workspace
        ```
    1. VS Codeメニューから、**File**を選択し、次に**Open Workspace from File**を選択します。
    3. コピーしたパス名を**置き換えて貼り付け**、**OK**を選択します。


    ## プロジェクト構造

    ワークショップ全体を通して作業する主要な**フォルダー**と**ファイル**に慣れ親しんでください。

    ### "workshop"フォルダー

    - **app.py**ファイル：アプリのエントリーポイントで、メインロジックが含まれています。

    **INSTRUCTIONS_FILE**変数に注目してください。これは、エージェントが使用する指示ファイルを設定します。後のラボでこの変数を更新します。

    - **resources.txt**ファイル：エージェントアプリが使用するリソースが含まれています。
    - **.env**ファイル：エージェントアプリが使用する環境変数が含まれています。

    ### "mcp_server"フォルダー

    - **sales_analysis.py**ファイル：売上分析のためのツールを含むMCPサーバー。

    ### "shared/instructions"フォルダー

    - **instructions**フォルダー：LLMに渡される指示が含まれています。

    ![ラボフォルダー構造](../../media/project-structure-self-guided-python.png)

=== "C#"

    1. Visual Studio Codeで、**File** > **Open Workspace from File**に移動します。
    2. デフォルトパスを以下に置き換えます：

        ```text
        /workspace/.vscode/csharp-workspace.code-workspace
        ```

    3. **OK**を選択してワークスペースを開きます。

    ## プロジェクト構造

    プロジェクトは[Aspire](http://aka.ms/dotnet-aspire)を使用して、エージェントアプリケーションの構築、MCPサーバーの管理、およびすべての外部依存関係のオーケストレーションを簡素化しています。ソリューションは4つのプロジェクトで構成されており、すべて`McpAgentWorkshop`のプレフィックスが付いています：

    * `AppHost`：Aspireオーケストレーターで、ワークショップの起動プロジェクトです。
    * `McpServer`：MCPサーバープロジェクト。
    * `ServiceDefaults`：ログ記録とテレメトリーなど、サービスのデフォルト構成。
    * `WorkshopApi`：ワークショップ用のエージェントAPI。コアアプリケーションロジックは`AgentService`クラスにあります。

    ソリューション内の.NETプロジェクトに加えて、`shared`フォルダー（ソリューションフォルダーとして表示され、ファイルエクスプローラー経由でアクセス可能）があります：

    * `instructions`：LLMに渡される指示。
    * `scripts`：さまざまなタスクのためのヘルパーシェルスクリプト。これらは必要に応じて参照されます。
    * `webapp`：フロントエンドクライアントアプリケーション。注意：これはPythonアプリケーションで、AspireがライフサイクルPOISTRを管理します。

    ![ラボフォルダー構造](../../media/project-structure-self-guided-csharp.png)
