## 自学者

这些说明适用于无法访问预配置实验环境的自学者。按照以下步骤设置您的环境并开始工作坊。

## 简介

本工作坊旨在教您 Azure AI 代理服务和相关的 SDK。它由多个实验组成，每个实验都突出了 Azure AI 代理服务的特定功能。实验应按顺序完成，因为每个实验都建立在前一个实验的知识和工作基础上。

## 先决条件

1. 访问 Azure 订阅。如果您没有 Azure 订阅，请在开始前创建一个[免费账户](https://azure.microsoft.com/free/){:target="_blank"}。
1. 您需要一个 GitHub 账户。如果您没有，请在 [GitHub](https://github.com/join){:target="_blank"} 创建一个。

## 选择工作坊编程语言

工作坊提供 Python 和 C# 两种版本。使用语言选择器选项卡选择您的首选语言。注意，不要在工作坊中途切换语言。

**选择您首选语言的选项卡：**

=== "Python"
    工作坊的默认语言设置为 **Python**。
=== "C#"
    工作坊的默认语言设置为 **C#**。

    !!! warning "此工作坊的 C#/.NET 版本为测试版，存在已知的稳定性问题。"

    确保在开始工作坊**之前**阅读[故障排除指南](../../zh/dotnet-troubleshooting.md)部分。否则，请选择工作坊的 **Python** 版本。

## 打开工作坊

首选：**GitHub Codespaces**，它提供了预配置的环境和所有必需的工具。或者，在本地使用 Visual Studio Code **Dev Container** 和 **Docker** 运行。使用下面的选项卡选择。

!!! Tip
    Codespaces 或 Dev Container 构建需要约 5 分钟。开始构建，然后在完成时**继续阅读**。

=== "GitHub Codespaces"

    选择**在 GitHub Codespaces 中打开**以在 GitHub Codespaces 中打开项目。

    [![在 GitHub Codespaces 中打开](https://github.com/codespaces/badge.svg)](https://codespaces.new/microsoft/aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol){:target="_blank"}

=== "VS Code Dev Container"

    1. 确保在您的本地机器上安装了以下内容：

        - [Docker](https://docs.docker.com/get-docker/){:target="\_blank"}
        - [Visual Studio Code](https://code.visualstudio.com/download){:target="\_blank"}
        - [Remote - Containers 扩展](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers){:target="\_blank"}
    1. 将仓库克隆到您的本地机器：

        ```bash
        git clone https://github.com/microsoft/aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol.git
        ```

    1. 在 Visual Studio Code 中打开克隆的仓库。
    1. 当提示时，选择**在容器中重新打开**以在 Dev Container 中打开项目。

---

## Azure 服务身份验证

!!! danger
    在继续之前，请确保您的 Codespace 或 Dev Container 已完全构建并准备就绪。

### 使用 DevTunnel 进行身份验证

DevTunnel 提供端口转发服务，在工作坊中用于允许 Azure AI 代理服务访问您将在本地开发环境中运行的 MCP 服务器。按照以下步骤进行身份验证：

1. 在 VS Code 中，**按** <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>`</kbd> 打开新的终端窗口。然后运行以下命令：
1. **运行以下命令**以使用 DevTunnel 进行身份验证：

   ```shell
   devtunnel login
   ```

1. 按照以下步骤进行身份验证：

   1. 将**身份验证代码**复制到剪贴板。
   2. **按住** <kbd>ctrl</kbd> 或 <kbd>cmd</kbd> 键。
   3. **选择**身份验证 URL 以在浏览器中打开它。
   4. **粘贴**代码并点击**下一步**。
   5. **选择一个账户**并登录。
   6. 选择**继续**
   7. **返回**到 VS Code 中的终端窗口。

1. 为下一步保持终端窗口**打开**。

### 使用 Azure 进行身份验证

使用 Azure 进行身份验证，以允许代理应用访问 Azure AI 代理服务和模型。按照以下步骤操作：

1. 然后运行以下命令：

    ```shell
    az login --use-device-code
    ```

    !!! warning
    如果您有多个 Azure 租户，请使用以下命令指定正确的租户：

    ```shell
    az login --use-device-code --tenant <tenant_id>
    ```

2. 按照以下步骤进行身份验证：

    1. 将**身份验证代码****复制**到剪贴板。
    2. **按住** <kbd>ctrl</kbd> 或 <kbd>cmd</kbd> 键。
    3. **选择**身份验证 URL 以在浏览器中打开它。
    4. **粘贴**代码并点击**下一步**。
    5. **选择一个账户**并登录。
    6. 选择**继续**
    7. **返回**到 VS Code 中的终端窗口。
    8. 如果提示，**选择**一个订阅。

3. 为下一步保持终端窗口打开。

---

## 部署 Azure 资源

此部署在您的 Azure 订阅中创建以下资源。

- 名为 **rg-zava-agent-wks-nnnnnnnn** 的资源组
- 名为 **fdy-zava-agent-wks-nnnnnnnn** 的 **Azure AI Foundry 中心**
- 名为 **prj-zava-agent-wks-nnnnnnnn** 的 **Azure AI Foundry 项目**
- 部署了两个模型：**gpt-4o-mini** 和 **text-embedding-3-small**。[查看定价。](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/){:target="\_blank"}
- 名为 **appi-zava-agent-wks-nnnnnnnn** 的 Application Insights 资源。[查看定价](https://azure.microsoft.com/pricing/calculator/?service=monitor){:target="\_blank"}
- 为了保持工作坊成本低廉，PostgreSQL 在您的 Codespace 或 Dev Container 内的本地容器中运行，而不是作为云服务。请参阅 [Azure Database for PostgreSQL 灵活服务器](https://azure.microsoft.com/en-us/products/postgresql){:target="\_blank"}以了解托管 PostgreSQL 服务的选项。

!!! warning "确保您至少拥有以下模型配额"
    - gpt-4o-mini Global Standard SKU 的 120K TPM 配额，因为代理频繁调用模型。
    - text-embedding-3-small 模型 Global Standard SKU 的 50K TPM。
    - 在 [AI Foundry 管理中心](https://ai.azure.com/managementCenter/quota){:target="\_blank"}检查您的配额。

### 自动化部署

运行以下 bash 脚本以自动化部署工作坊所需的资源。`deploy.sh` 脚本默认将资源部署到 `westus` 区域。要运行脚本：

```bash
cd infra && ./deploy.sh
```

### 工作坊配置

=== "Python"

    #### Azure 资源配置

    部署脚本生成 **.env** 文件，其中包含项目和模型端点、模型部署名称以及 Application Insights 连接字符串。.env 文件将自动保存在 `src/python/workshop` 文件夹中。

    您的 **.env** 文件将类似于以下内容，并更新为您的值：

    ```python
    PROJECT_ENDPOINT="<your_project_endpoint>"
    GPT_MODEL_DEPLOYMENT_NAME="<your_model_deployment_name>"
    EMBEDDING_MODEL_DEPLOYMENT_NAME="<your_embedding_model_deployment_name>"
    APPLICATIONINSIGHTS_CONNECTION_STRING="<your_application_insights_connection_string>"
    AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED="true"
    AZURE_OPENAI_ENDPOINT="<your_azure_openai_endpoint>"
    ```

    #### Azure 资源名称

    您还会在 `workshop` 文件夹中找到名为 `resources.txt` 的文件。此文件包含在部署期间创建的 Azure 资源的名称。

    它看起来类似于以下内容：

    ```plaintext
    Azure AI Foundry Resources:
    - Resource Group Name: rg-zava-agent-wks-nnnnnnnn
    - AI Project Name: prj-zava-agent-wks-nnnnnnnn
    - Foundry Resource Name: fdy-zava-agent-wks-nnnnnnnn
    - Application Insights Name: appi-zava-agent-wks-nnnnnnnn
    ```

=== "C#"

    该脚本使用 [ASP.NET Core 开发机密](https://learn.microsoft.com/aspnet/core/security/app-secrets){:target="_blank"}的 Secret Manager 安全地存储项目变量。

    您可以在 VS Code 中打开 C# 工作区后运行以下命令查看机密：

    ```bash
    dotnet user-secrets list
    ```

---

## 打开 VS Code 工作区

工作坊中有两个 VS Code 工作区，一个用于 Python，一个用于 C#。工作区包含源代码和完成每种语言实验所需的所有文件。选择与您要使用的语言匹配的工作区。

=== "Python"

    1. **复制**以下路径到剪贴板：

        ```text
        /workspace/.vscode/python-workspace.code-workspace
        ```
    1. 在 VS Code 菜单中，选择**文件**然后**从文件打开工作区**。
    3. 替换并**粘贴**复制的路径名称并选择**确定**。

    ## 项目结构

    熟悉您在整个工作坊中将使用的工作区中的关键**文件夹**和**文件**。

    ### "workshop" 文件夹

    - **app.py** 文件：应用程序的入口点，包含其主要逻辑。

    注意 **INSTRUCTIONS_FILE** 变量—它设置代理使用哪个指令文件。您将在后面的实验中更新此变量。

    - **resources.txt** 文件：包含代理应用使用的资源。
    - **.env** 文件：包含代理应用使用的环境变量。

    ### "mcp_server" 文件夹

    - **sales_analysis.py** 文件：具有销售分析工具的 MCP 服务器。

    ### "shared/instructions" 文件夹

    - **instructions** 文件夹：包含传递给 LLM 的指令。

    ![实验文件夹结构](../../media/project-structure-self-guided-python.png)

=== "C#"

    1. 在 Visual Studio Code 中，转到**文件** > **从文件打开工作区**。
    2. 将默认路径替换为以下内容：

        ```text
        /workspace/.vscode/csharp-workspace.code-workspace
        ```

    3. 选择**确定**打开工作区。

    ## 项目结构

    该项目使用 [Aspire](http://aka.ms/dotnet-aspire) 简化构建代理应用程序、管理 MCP 服务器和编排所有外部依赖项。解决方案由四个项目组成，都以 `McpAgentWorkshop` 为前缀：

    * `AppHost`：Aspire 编排器，以及工作坊的启动项目。
    * `McpServer`：MCP 服务器项目。
    * `ServiceDefaults`：服务的默认配置，如日志记录和遥测。
    * `WorkshopApi`：工作坊的代理 API。核心应用程序逻辑在 `AgentService` 类中。

    除了解决方案中的 .NET 项目之外，还有一个 `shared` 文件夹（作为解决方案文件夹可见，并通过文件资源管理器），其中包含：

    * `instructions`：传递给 LLM 的指令。
    * `scripts`：各种任务的辅助 shell 脚本，需要时会引用这些脚本。
    * `webapp`：前端客户端应用程序。注意：这是一个 Python 应用程序，Aspire 将管理其生命周期。

    ![实验文件夹结构](../../media/project-structure-self-guided-csharp.png)

*使用 GitHub Copilot 翻译。*
