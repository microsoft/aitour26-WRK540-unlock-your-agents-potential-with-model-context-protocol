## はじめに

!!! note "Aspire Dashboardでのトレースは、ワークショップのC#版でのみサポートされています。"

これまでのトレースでは、Azure AI Foundryダッシュボードを通じて可視化する方法に焦点を当ててきましたが、これはローカル開発時のワークフローの中断となる場合があります。それに加えて、Aspire Dashboardを活用して、アプリケーションによって生成されたトレースをリアルタイムで可視化し、アクションがシステム内の複数のリソースにわたってどのように展開されるかを確認できます。

## エージェントアプリを実行する

<kbd>F5</kbd>を押してアプリケーションを起動し、ブラウザにAspire Dashboardが表示されるまで待ちます。これにより、ワークショップ内のリソースの完全なリストが表示されます。

![Aspire Dashboard](../media/lab-7-dashboard.png)

前のラボステップと同様に、**Workshop Frontend**を開き、チャットに以下のようなプロンプトを入力します：

```plaintext
Write an executive report that analysis the top 5 product categories and compares performance of the online store verses the average for the physical stores.
```

## トレースを表示する

アプリケーションによって生成されたトレースを表示するには、Aspire Dashboardの**Traces**タブに移動します。ここで、発信者から始まるキャプチャされたすべてのトレースのリストを確認できます。

![Trace overview](../media/lab-7-trace-overview.png)

上記のスクリーンショットの最終エントリは、**dotnet-front-end**が`/chat/stream`に`GET`を実行するイベントを示しています。**Span**列には、このトレースが展開されるリソース、`dotnet-front-end`、`dotnet-agent-app`、`ai-foundry`、`dotnet-mcp-server`、`pg`が表示されます。

各リソースには番号が関連付けられており、これはそのリソースに対して発生した_スパン_の数です。また、`dotnet-mcp-server`と`pg`リソースにエラーインジケータがあることも確認でき、これらのリソースでエラーが発生したことを示しています。

トレースをクリックすると、トレースタイムラインの詳細ビューが表示されます：

![Trace timeline](../media/lab-7-trace-timeline.png)

ここから、個々のスパン、発生順序、継続時間、アプリケーション内のリソース間でのイベント発生を確認できます。

個々のスパンをクリックすると、その特定のスパンについての詳細が表示されます：

![Span details](../media/lab-7-span-details.png)

異なるプロンプトを試したり、エラーをシミュレートしたりして、Aspire Dashboardでトレースがどのように変化するかを観察してみてください。

## 追加資料

- [Aspire Documentation](https://aka.ms/aspire-docs)
- [Aspire Telemetry Documentation](https://learn.microsoft.com/dotnet/aspire/fundamentals/telemetry)
