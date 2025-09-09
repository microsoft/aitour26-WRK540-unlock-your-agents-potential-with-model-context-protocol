# 实验 6：理解追踪

## 简介

追踪通过显示执行期间的步骤序列、输入和输出来帮助您理解和调试代理的行为。在 Azure AI Foundry 中，追踪让您观察代理如何处理请求、调用工具和生成响应。您可以使用 Azure AI Foundry 门户或与 OpenTelemetry 和 Application Insights 集成来收集和分析追踪数据，使排除故障和优化代理变得更容易。

<!-- ## 实验练习

=== "Python"

      1. 打开 `app.py` 文件。
      2. 将 `AZURE_TELEMETRY_ENABLED` 变量更改为 `True` 以启用追踪：

         ```python
         AZURE_TELEMETRY_ENABLED = True
         ```

        !!! info "注意"
            此设置为您的代理启用遥测。在 `app.py` 中的 `initialize` 函数中，配置遥测客户端向 Azure Monitor 发送数据。

            ```python
             if AZURE_TELEMETRY_ENABLED:
                 configure_azure_monitor(connection_string=await self.project_client.telemetry.get_connection_string())
            ```         

=== "C#"

      待定 -->

<!-- ## 运行代理应用

1. 按 <kbd>F5</kbd> 运行应用。
2. 选择**在编辑器中预览**在新编辑器选项卡中打开代理应用。

### 开始与代理对话

将以下提示复制并粘贴到代理应用中以开始对话：

```plaintext
Write an executive report that analysis the top 5 product categories and compares performance of the online store verses the average for the physical stores.
``` -->

## 查看追踪

您可以在 Azure AI Foundry 门户中或使用 OpenTelemetry 查看代理执行的追踪。追踪将显示代理执行期间的步骤序列、工具调用和数据交换。此信息对于调试和优化代理性能至关重要。

### 使用 Azure AI Foundry 门户

要在 Azure AI Foundry 门户中查看追踪，请按照以下步骤操作：

1. 导航到 [Azure AI Foundry](https://ai.azure.com/) 门户。
2. 选择您的项目。
3. 在左侧菜单中选择**追踪**选项卡。
4. 在这里，您可以看到代理生成的追踪。

   ![](media/ai-foundry-tracing.png)

### 深入追踪详情

1. 您可能需要单击**刷新**按钮以查看最新的追踪，因为追踪可能需要几分钟才能显示。
2. 选择名为 `Zava Agent Initialization` 的追踪以查看详细信息。
   ![](media/ai-foundry-trace-agent-init.png)
3. 选择 `create_agent Zava DIY Sales Agent` 追踪以查看代理创建过程的详细信息。在 `Input & outputs` 部分，您将看到代理指令。
4. 接下来，选择 `Zava Agent Chat Request: Write an executive...` 追踪以查看聊天请求的详细信息。在 `Input & outputs` 部分，您将看到用户输入和代理的响应。

<!-- https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/continuous-evaluation-agents -->

*使用 GitHub Copilot 翻译。*
