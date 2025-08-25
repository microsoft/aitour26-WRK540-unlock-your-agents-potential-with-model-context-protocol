!!! danger 
    続行する前に、Codespace または Dev Container が完全に構築され、準備ができていることを確認してください。

## Azure での認証

エージェントアプリがAzure AI エージェントサービスとモデルにアクセスできるよう、Azureで認証します。以下の手順に従ってください：

1. VS Code から、<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>`</kbd> を**押して**新しいターミナルウィンドウを開きます。次に以下のコマンドを実行します：

    ```shell
    az login --use-device-code
    ```

    !!! warning
        複数のAzureテナントがある場合は、正しいものを指定してください：

        ```shell
        az login --use-device-code --tenant <tenant_id>
        ```

2. 以下の手順で認証します：

    1. **認証コード**をクリップボードに**コピー**します。
    2. <kbd>ctrl</kbd>または<kbd>cmd</kbd>キーを**押し続けます**。
    3. 認証URLを**選択**してブラウザーで開きます。
    4. コードを**貼り付け**、**次へ**をクリックします。
    5. **アカウントを選択**してサインインします。
    6. **続行**を選択します。
    7. VS Code のターミナルウィンドウに**戻ります**。
    8. プロンプトが表示されたら、サブスクリプションを**選択**します。

3. 次のステップのためにターミナルウィンドウを開いたままにします。

## Azure リソースのデプロイ

このデプロイメントは、Azure サブスクリプションに以下のリソースを作成します。

- **rg-zava-agent-wks-nnnn** という名前のリソースグループ
- **fdy-zava-agent-wks-nnnn** という名前の **Azure AI Foundry ハブ**
- **prj-zava-agent-wks-nnnn** という名前の **Azure AI Foundry プロジェクト**
- 2つのモデルがデプロイされます：**gpt-4o-mini** と **text-embedding-3-small**。[価格を参照。](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/){:target="_blank"}

!!! warning "少なくとも以下のモデルクォータがあることを確認してください"
    - エージェントが頻繁にモデル呼び出しを行うため、gpt-4o-mini Global Standard SKU に対して 120K TPM クォータ。
    - text-embedding-3-small モデル Global Standard SKU に対して 50K TPM。
    - [AI Foundry 管理センター](https://ai.azure.com/managementCenter/quota){:target="_blank"}でクォータを確認してください。

### 自動デプロイメント

ワークショップに必要なリソースのデプロイメントを自動化するために、以下の bash スクリプトを実行します。`deploy.sh` スクリプトは、デフォルトで `westus` リージョンにリソースをデプロイします。スクリプトを実行するには：

=== "Linux/Mac OS"

    ```bash
    cd infra && ./deploy.sh
    ```

=== "Windows"

    ```powershell
    cd infra && .\deploy.ps1
    ```

<!-- !!! note "Windows では、`deploy.sh` の代わりに `deploy.ps1` を実行してください" -->

### ワークショップ設定

=== "Python"

    #### Azure リソース設定

    デプロイスクリプトは **.env** ファイルを生成します。これにはプロジェクトとモデルのエンドポイント、モデルデプロイ名、Application Insights 接続文字列が含まれます。.env ファイルは `src/python/workshop` フォルダーに自動的に保存されます。
    
    **.env** ファイルは次のようになり、あなたの値で更新されます：

    ```python
    PROJECT_ENDPOINT="<your_project_endpoint>"
    GPT_MODEL_DEPLOYMENT_NAME="<your_model_deployment_name>"
    EMBEDDING_MODEL_DEPLOYMENT_NAME="<your_embedding_model_deployment_name>"
    APPLICATIONINSIGHTS_CONNECTION_STRING="<your_application_insights_connection_string>"
    DEV_TUNNEL_URL="<your_dev_tunnel_url>"
    AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED="true"
    AZURE_OPENAI_ENDPOINT="<your_azure_openai_endpoint>"
    ```

    #### Azure リソース名

    `workshop` フォルダーには `resources.txt` という名前のファイルもあります。このファイルには、デプロイメント中に作成された Azure リソースの名前が含まれています。

    次のようになります：

    ```plaintext
    Azure AI Foundry Resources:
    - Resource Group Name: rg-zava-agent-wks-nnnn
    - AI Project Name: prj-zava-agent-wks-nnnn
    - Foundry Resource Name: fdy-zava-agent-wks-nnnn
    - Application Insights Name: appi-zava-agent-wks-nnnn
    ```

=== "C#"

    スクリプトは [ASP.NET Core 開発シークレット](https://learn.microsoft.com/aspnet/core/security/app-secrets){:target="_blank"}の Secret Manager を使用して、プロジェクト変数を安全に保存します。

    VS Code で C# ワークスペースを開いた後、以下のコマンドを実行してシークレットを表示できます：

    ```bash
    dotnet user-secrets list
    ```

*GitHub Copilot を使用して翻訳されました。*
