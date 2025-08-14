**TBC: このラベルは、エージェントが応答で使用する迷惑な絵文字を削除するためにエージェント指示ファイルを更新するようユーザーに求めます。**

## はじめに

トレーシングは、実行中のステップのシーケンス、入力、出力を表示することで、エージェントの動作を理解およびデバッグするのに役立ちます。Azure AI Foundry では、トレーシングにより、エージェントがリクエストを処理し、ツールを呼び出し、応答を生成する方法を観察できます。Azure AI Foundry ポータルを使用するか、OpenTelemetry と Application Insights と統合してトレースデータを収集および分析し、エージェントのトラブルシューティングと最適化を簡単にできます。

<!-- ## ラボ演習

=== "Python"

      1. `app.py` ファイルを開きます。
      2. トレーシングを有効にするために `AZURE_TELEMETRY_ENABLED` 変数を `True` に変更します：

         ```python
         AZURE_TELEMETRY_ENABLED = True
         ```

        !!! info "注記"
            この設定により、エージェントのテレメトリが有効になります。`app.py` の `initialize` 関数で、テレメトリクライアントが Azure Monitor にデータを送信するよう設定されます。

            ```python
             if AZURE_TELEMETRY_ENABLED:
                 configure_azure_monitor(connection_string=await self.project_client.telemetry.get_connection_string())
            ```         

=== "C#"

      tbd -->

## エージェントアプリの実行

1. <kbd>F5</kbd> を押してアプリを実行します。
2. **Preview in Editor** を選択して、新しいエディタータブでエージェントアプリを開きます。

### エージェントとの会話開始

エージェントアプリに以下のプロンプトをコピーして貼り付け、会話を開始します：

```plaintext
上位5つの製品カテゴリを分析し、オンラインストアのパフォーマンスと実店舗の平均を比較したエグゼクティブレポートを作成してください。
```

## トレースの表示

Azure AI Foundry ポータルまたは OpenTelemetry を使用して、エージェントの実行のトレースを表示できます。トレースは、エージェントの実行中のステップのシーケンス、ツール呼び出し、データ交換を表示します。この情報は、エージェントのパフォーマンスをデバッグおよび最適化するために重要です。

### Azure AI Foundry ポータルの使用

Azure AI Foundry ポータルでトレースを表示するには、以下の手順に従います：

1. **[Azure AI Foundry](https://ai.azure.com/)** ポータルに移動します。
2. プロジェクトを選択します。
3. 左側のメニューの **Tracing** タブを選択します。
4. ここで、エージェントによって生成されたトレースを確認できます。

   ![](media/ai-foundry-tracing.png)

### トレースの詳細表示

1. トレースが表示されるまで数分かかる場合があるため、最新のトレースを確認するために **Refresh** ボタンをクリックする必要がある場合があります。
2. `Zava Agent Initialization` という名前のトレースを選択して詳細を表示します。
   ![](media/ai-foundry-trace-agent-init.png)
3. `creare_agent Zava DIY Sales Agent` トレースを選択して、エージェント作成プロセスの詳細を表示します。`Input & outputs` セクションで、エージェント指示を確認できます。
4. 次に、`Zava Agent Chat Request: Write an executive...` トレースを選択して、チャットリクエストの詳細を表示します。`Input & outputs` セクションで、ユーザー入力とエージェントの応答を確認できます。

<!-- https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/continuous-evaluation-agents -->

*GitHub Copilot を使用して翻訳されました。*
