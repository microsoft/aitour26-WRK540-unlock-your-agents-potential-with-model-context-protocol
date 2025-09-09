# 实验 5：服务监控

## 简介

监控使您的 Azure AI Foundry 代理服务保持可用、高性能和可靠。Azure Monitor 收集指标和日志，提供实时洞察并发送警报。使用仪表板和自定义警报来跟踪关键指标、分析趋势并主动响应。通过 Azure 门户、CLI、REST API 或客户端库访问监控。

## 实验练习

1. 从 VS Code 文件资源管理器中，在 `workshop` 文件夹中打开 `resources.txt` 文件。
1. **复制** `AI Project Name` 键的值到剪贴板。
1. 导航到 [Azure AI Foundry 门户](https://ai.azure.com){:target="_blank"} 页面。
1. 从 Foundry 项目列表中选择您的项目。

## 打开监控仪表板

1. 从 `resources.txt` 中，复制 `Application Insights Name` 的值到剪贴板。
1. 切换回 AI Foundry 门户，在左侧菜单中选择**监控**部分。
1. 将复制的 `Application Insights Name` 粘贴到 `Application Insights resource name` 下拉列表中。
1. 从下拉列表中选择**Application Insights** 资源。
1. 选择**连接**。

### 探索监控仪表板

熟悉 `Application analytics` 仪表板上可用的信息。

!!!tip "您可以选择日期范围来过滤监控工具中显示的数据。"

![图像显示了应用程序监控仪表板](../media/monitor_usage.png)

### 监控资源使用情况

您可以深入挖掘，选择 `Resource Usage` 查看有关 AI 项目资源消耗的详细指标。同样，您可以按时间范围过滤数据。

![图像显示了资源使用情况监控仪表板](../media/monitor_resource_usage.png)

*使用 GitHub Copilot 翻译。*
