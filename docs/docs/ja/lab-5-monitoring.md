## はじめに

監視により、Azure AI Foundry Agent Serviceの可用性、パフォーマンス、信頼性が保たれます。Azure Monitorはメトリクスとログを収集し、リアルタイムの洞察を提供し、アラートを送信します。ダッシュボードとカスタムアラートを使用して主要メトリクスを追跡し、トレンドを分析し、積極的に対応できます。Azureポータル、CLI、REST API、またはクライアントライブラリを介して監視にアクセスします。

## ラボ演習

1. VS Code file explorerから、`workshop`フォルダの`resources.txt`ファイルを開きます。
1. `AI Project Name`キーの値をクリップボードに**コピー**します。
1. [Azure AI Foundry Portal](https://ai.azure.com){:target="_blank"}ページに移動します。
1. foundryプロジェクトのリストから自分のプロジェクトを選択します。

## Monitoringダッシュボードを開く

1. `resources.txt`から、`Application Insights Name`の値をクリップボードにコピーします。
1. AI Foundryポータルに戻り、左側メニューの**Monitoring**セクションを選択します。
1. コピーした`Application Insights Name`を`Application Insights resource name`ドロップダウンリストに貼り付けます。
1. ドロップダウンリストから**Application Insights**リソースを選択します。
1. **Connect**を選択します。

### Monitoringダッシュボードを探索する

`Application analytics`ダッシュボードで利用可能な情報について理解してください。

!!!tip "監視ツールに表示されるデータをフィルタリングするために日付範囲を選択できます。"

![The image shows the application monitoring dashboard](../media/monitor_usage.png)

### リソース使用量を監視する

さらに詳しく調べるには、`Resource Usage`を選択してAIプロジェクトのリソース消費に関する詳細メトリクスを表示します。こちらも時間範囲でデータをフィルタリングできます。

![The image shows the resource usage monitoring dashboard](../media/monitor_resource_usage.png)
