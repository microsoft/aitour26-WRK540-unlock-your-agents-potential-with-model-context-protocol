## はじめに

トレースは、実行中のステップのシーケンス、入力、出力を表示することで、エージェントの動作を理解し、デバッグするのに役立ちます。Azure AI Foundryでは、トレースによりエージェントがリクエストを処理し、ツールを呼び出し、応答を生成する方法を観察できます。Azure AI Foundryポータルを使用するか、OpenTelemetryとApplication Insightsと統合してトレースデータを収集・分析し、エージェントのトラブルシューティングと最適化を容易にできます。

<!-- ## ラボ演習

=== "Python"

      1. `app.py`ファイルを開きます。
      2. トレースを有効にするために`AZURE_TELEMETRY_ENABLED`変数を`True`に変更します：

         ```python
         AZURE_TELEMETRY_ENABLED = True
         ```

        !!! info "注意"
            この設定はエージェントのテレメトリを有効にします。`app.py`の`initialize`関数で、テレメトリクライアントはAzure Monitorにデータを送信するよう設定されます。

            ```python
             if AZURE_TELEMETRY_ENABLED:
                 configure_azure_monitor(connection_string=await self.project_client.telemetry.get_connection_string())
            ```         

=== "C#"

      tbd -->

<!-- ## エージェントアプリを実行する

1. <kbd>F5</kbd>を押してアプリを実行します。
2. **Preview in Editor**を選択して、新しいエディタタブでエージェントアプリを開きます。

### エージェントとの会話を開始する

以下のプロンプトをエージェントアプリにコピー＆ペーストして会話を開始します：

```plaintext
Write an executive report that analysis the top 5 product categories and compares performance of the online store verses the average for the physical stores.
``` -->

## トレースを表示する

Azure AI Foundryポータルまたは OpenTelemetryを使用して、エージェント実行のトレースを表示できます。トレースは、エージェント実行中のステップのシーケンス、ツール呼び出し、交換されたデータを示します。この情報は、エージェントのパフォーマンスのデバッグと最適化に不可欠です。

### Azure AI Foundryポータルを使用

Azure AI Foundryポータルでトレースを表示するには、以下の手順に従ってください：

1. [Azure AI Foundry](https://ai.azure.com/)ポータルに移動します。
2. プロジェクトを選択します。
3. 左側メニューの**Tracing**タブを選択します。
4. ここで、エージェントによって生成されたトレースを確認できます。

   ![](media/ai-foundry-tracing.png)

### トレースを詳しく調べる

1. トレースは表示されるまで数分かかる場合があるため、最新のトレースを表示するために**Refresh**ボタンをクリックする必要がある場合があります。
2. `Zava Agent Initialization`という名前のトレースを選択して詳細を表示します。
   ![](media/ai-foundry-trace-agent-init.png)
3. `create_agent Zava DIY Sales Agent`トレースを選択して、エージェント作成プロセスの詳細を表示します。`Input & outputs`セクションで、エージェントの指示を確認できます。
4. 次に、`Zava Agent Chat Request: Write an executive...`トレースを選択して、チャットリクエストの詳細を表示します。`Input & outputs`セクションで、ユーザー入力とエージェントの応答を確認できます。

<!-- https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/continuous-evaluation-agents -->
