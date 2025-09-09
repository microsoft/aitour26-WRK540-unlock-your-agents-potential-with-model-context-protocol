# 硬件实操 1：启动 MCP 服务器

## 您将学到什么

在本实验中，您将：

- 使用 DevTunnel 使您的本地 MCP 服务器能够被基于云的代理服务访问
- 设置环境以便进行模型上下文协议的实际实验

## 简介

模型上下文协议 (MCP) 服务器是处理大型语言模型 (LLM) 与外部工具和数据源之间通信的关键组件。您将在本地计算机上运行 MCP 服务器，但 Azure AI Foundry 代理服务需要互联网访问才能连接到它。要使您的本地 MCP 服务器可从互联网访问，您将使用 DevTunnel。这允许代理服务与您的 MCP 服务器通信，就像它在 Azure 中作为服务运行一样。

## MCP 的接口选项

MCP 支持两种连接 LLM 与工具的主要接口：

- **可流式传输的 HTTP 传输**：用于基于 Web 的 API 和服务。
- **标准输入输出传输**：用于本地脚本和命令行工具。

本实验使用可流式传输的 HTTP 传输接口与 Azure AI Foundry 代理服务集成。

!!! note
    通常，您会在生产环境中部署 MCP 服务器，但在本工作坊中，您将在开发环境中本地运行它。这允许您测试和与 MCP 工具交互，而无需完整部署。

### 为 MCP 服务器启动 DevTunnel

1. 在新终端中，验证 DevTunnel。您将被提示使用 Azure 账户登录，使用与登录 Azure AI Foundry 代理服务或 Azure 门户相同的账户。运行以下命令：

    ```bash
    devtunnel login
    ```

2. 接下来，在运行 MCP 服务器的终端中，通过运行以下命令启动 DevTunnel：

    ```bash
    devtunnel host -p 8000 --allow-anonymous
    ```

    这将输出一个 URL，您需要它来让代理连接到 MCP 服务器。输出将类似于：

    ```text
    Hosting port: 8000
    Connect via browser: https://<tunnel-id>-8000.aue.devtunnels.ms
    Inspect network activity: https://<tunnel-id>-8000-inspect.aue.devtunnels.ms
    ```

## 更新 DevTunnel 环境变量

1. 将**通过浏览器连接**的 URL 复制到剪贴板 - 您将在下一个实验中需要它来配置代理。
2. 在 workshop 文件夹中打开 `.env` 文件。
3. 使用复制的 URL 更新 `DEV_TUNNEL_URL` 变量。

    ```text
    DEV_TUNNEL_URL=https://<tunnel-id>-8000.aue.devtunnels.ms
    ```

## 启动代理应用

1. 将以下文本复制到剪贴板：

    ```text
    Debug: Select and Start Debugging
    ```

2. 按 <kbd>F1</kbd> 打开 VS Code 命令面板。
3. 将文本粘贴到命令面板中并选择**Debug: Select and Start Debugging**。
4. 从列表中选择**🌎🤖Debug Compound: Agent and MCP (http)**。这将启动代理应用和 Web 聊天客户端。

## 开始与代理对话

切换到浏览器中的**Web Chat**选项卡。您应该看到代理应用正在运行并准备接受问题。

### 使用 DevTunnel 调试

您可以使用 DevTunnel 调试 MCP 服务器和代理应用。这允许您检查网络活动并实时排除问题。

1. 从 DevTunnel 输出中选择**检查网络活动** URL。
2. 这将在浏览器中打开一个新选项卡，您可以在其中查看 MCP 服务器和代理应用的网络活动。
3. 您可以使用它来调试工作坊期间出现的任何问题。

您还可以在 MCP 服务器代码和代理应用代码中设置断点来调试特定问题。要这样做：

1. 在 `mcp_server` 文件夹中打开 `sales_analysis.py` 文件。
2. 通过单击要暂停执行的行号旁边的装订线来设置断点。
3. 当执行到达断点时，您可以检查变量、逐步执行代码，并在调试控制台中评估表达式。

*使用 GitHub Copilot 翻译。*
