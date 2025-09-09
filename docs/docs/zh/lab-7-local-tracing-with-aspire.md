# 使用 Aspire 进行本地追踪

## 简介

!!! note "使用 Aspire 仪表板进行追踪仅在工作坊的 C# 版本中受支持。"

到目前为止，对于我们的追踪，我们专注于如何通过 Azure AI Foundry 仪表板可视化，这在本地开发时可能会中断工作流程。除此之外，我们可以利用 Aspire 仪表板实时可视化应用程序生成的追踪，以及操作如何跨越系统内的多个资源。

## 运行代理应用

按 <kbd>F5</kbd> 启动应用程序并等待 Aspire 仪表板在浏览器中出现。这将显示工作坊中资源的完整列表。

![Aspire 仪表板](../media/lab-7-dashboard.png)

与之前的实验步骤一样，打开**Workshop Frontend**并在聊天中输入提示，例如：

```plaintext
Write an executive report that analysis the top 5 product categories and compares performance of the online store verses the average for the physical stores.
```

## 查看追踪

要查看应用程序生成的追踪，请导航到 Aspire 仪表板中的**追踪**选项卡。在这里，您可以看到已捕获的所有追踪列表，从其发起者开始。

![追踪概述](../media/lab-7-trace-overview.png)

上述屏幕截图中的最后一个条目显示了来自**dotnet-front-end**执行 `GET` 到 `/chat/stream` 的事件。**Span** 列然后显示此追踪跨越的资源，`dotnet-front-end`、`dotnet-agent-app`、`ai-foundry`、`dotnet-mcp-server` 和 `pg`。

每个资源都有一个关联的数字，这是该资源发生的_跨度_数。我们还可以在 `dotnet-mcp-server` 和 `pg` 资源上注意到错误指示器，这表示这些资源上发生了错误。

点击追踪将显示追踪时间线的详细视图：

![追踪时间线](../media/lab-7-trace-timeline.png)

从这里，我们可以查看各个跨度、它们发生的顺序、持续时间，以及事件如何在应用程序内的资源之间发生。

点击单个跨度将显示该特定跨度的更多详细信息：

![跨度详细信息](../media/lab-7-span-details.png)

尝试使用不同的提示进行实验并模拟错误，以观察追踪在 Aspire 仪表板中的变化。

## 其他阅读

- [Aspire 文档](https://aka.ms/aspire-docs)
- [Aspire 遥测文档](https://learn.microsoft.com/dotnet/aspire/fundamentals/telemetry)

*使用 GitHub Copilot 翻译。*
