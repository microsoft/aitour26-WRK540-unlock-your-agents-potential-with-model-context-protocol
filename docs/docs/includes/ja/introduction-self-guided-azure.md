## Codespace ビルドの完了を待つ

続行する前に、Codespace または Dev Container が完全にビルドされ、準備が整っていることを確認してください。インターネット接続とダウンロードされるリソースによっては、数分かかる場合があります。

## Azure での認証

エージェントアプリが Azure AI Agents Service とモデルにアクセスできるよう、Azure で認証します。以下の手順に従ってください：

1. ワークショップ環境が準備されており、VS Code で開いていることを確認します。
2. VS Code から、**Terminal** > **New Terminal** でターミナルを開き、次のコマンドを実行します：

    ```shell
    az login --use-device-code
    ```

    !!! note
        ブラウザを開いて Azure にログインするよう求められます。認証コードをコピーして：

        1. アカウントタイプを選択し、**次へ**をクリックします。
        2. Azure 認証情報でサインインします。
        3. コードを貼り付けます。
        4. **OK**をクリックし、**完了**をクリックします。

    !!! warning
        複数の Azure テナントがある場合は、次のコマンドで正しいテナントを指定してください：

        ```shell
        az login --use-device-code --tenant <tenant_id>
        ```

3. 次に、コマンドラインから適切なサブスクリプションを選択します。
4. 次のステップのためにターミナルウィンドウを開いたままにしておきます。

## Azure リソースをデプロイする

このデプロイメントは、**rg-zava-agent-wks-nnnn** リソースグループの下で Azure サブスクリプションに以下のリソースを作成します：

- **fdy-zava-agent-wks-nnnn** という名前の **Azure AI Foundry hub**
- **prj-zava-agent-wks-nnnn** という名前の **Azure AI Foundry project**
- 2つのモデルがデプロイされます：**gpt-4o-mini** と **text-embedding-3-small**。[価格を確認してください。](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/){:target="_blank"}

!!! warning "エージェントは頻繁にモデル呼び出しを行うため、gpt-4o-mini Global Standard SKU に対して少なくとも 120K TPM クォータがあることを確認してください。[AI Foundry Management Center](https://ai.azure.com/managementCenter/quota){:target="_blank"} でクォータを確認してください。"

ワークショップに必要なリソースのデプロイメントを自動化するバッシュスクリプトを提供しています。

### 自動デプロイメント

`deploy.sh` スクリプトは、デフォルトで `westus` リージョンにリソースをデプロイします。スクリプトを実行するには：

```bash
cd infra && ./deploy.sh
```

<!-- !!! note "Windows では、`deploy.sh` の代わりに `deploy.ps1` を実行してください" -->

### ワークショップ設定

=== "Python"

    #### Azure リソース設定

    deploy スクリプトは、プロジェクトとモデルエンドポイント、モデルデプロイメント名、Application Insights 接続文字列を含む **.env** ファイルを生成します。.env ファイルは `src/python/workshop` フォルダに自動的に保存されます。
    
    **.env** ファイルは以下のようになり、あなたの値で更新されます：

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

    `workshop` フォルダに `resources.txt` という名前のファイルもあります。このファイルには、デプロイメント中に作成された Azure リソースの名前が含まれています。

    以下のようになります：

    ```plaintext
    Azure AI Foundry Resources:
    - Resource Group Name: rg-zava-agent-wks-nnnn
    - AI Project Name: prj-zava-agent-wks-nnnn
    - Foundry Resource Name: fdy-zava-agent-wks-nnnn
    - Application Insights Name: appi-zava-agent-wks-nnnn
    ```

=== "C#"

    スクリプトは、[ASP.NET Core 開発シークレット](https://learn.microsoft.com/aspnet/core/security/app-secrets){:target="_blank"} の Secret Manager を使用してプロジェクト変数を安全に保存します。

    VS Code で C# ワークスペースを開いた後、次のコマンドを実行してシークレットを表示できます：

    ```bash
    dotnet user-secrets list
    ```

*Translated using GitHub Copilot and GPT-4o.*
