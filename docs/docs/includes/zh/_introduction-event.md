## Microsoft 活动参与者

本页面的说明假设您正在参加 [Microsoft Event 2025](https://build.microsoft.com/){:target="_blank"} 并且可以访问预配置的实验环境。此环境提供了一个 Azure 订阅，其中包含完成工作坊所需的所有工具和资源。

## 简介

本工作坊旨在教您 Azure AI 代理服务和相关的 [SDK](https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme?context=%2Fazure%2Fai-services%2Fagents%2Fcontext%2Fcontext){:target="_blank"}。它由多个实验组成，每个实验都突出了 Azure AI 代理服务的特定功能。实验应按顺序完成，因为每个实验都建立在前一个实验的知识和工作基础上。

## 选择工作坊编程语言

工作坊提供 Python 和 C# 两种版本。请确保使用语言选择器选项卡选择适合您所在实验室的语言。注意，不要在工作坊中途切换语言。

**选择与您的实验室匹配的语言选项卡：**

=== "Python"
    工作坊的默认语言设置为 **Python**。
=== "C#"
    工作坊的默认语言设置为 **C#**。

## 使用 Azure 进行身份验证

您需要使用 Azure 进行身份验证，以便代理应用可以访问 Azure AI 代理服务和模型。按照以下步骤操作：

1. 打开终端窗口。终端应用已**固定**到 Windows 11 任务栏。

    ![打开终端窗口](../media/windows-taskbar.png){ width="300" }

2. 运行以下命令以使用 Azure 进行身份验证：

    ```powershell
    az login
    ```

    !!! note
        系统将提示您打开浏览器链接并登录到您的 Azure 账户。

        1. 浏览器窗口将自动打开，选择**工作或学校账户**，然后选择**继续**。

        1. 使用在实验环境的**资源**选项卡**顶部**找到的**用户名**和**密码**。

        2. 选择**是，所有应用**

3. 然后通过选择**Enter**从命令行选择**默认**订阅。

4. 登录后，运行以下命令将**用户**角色分配给资源组：

    ```powershell
    $subId = $(az account show --query id --output tsv) `
    ;$objectId = $(az ad signed-in-user show --query id -o tsv) `
    ; az role assignment create --role "f6c7c914-8db3-469d-8ca1-694a8f32e121" --assignee-object-id $objectId --scope /subscriptions/$subId/resourceGroups/"rg-agent-workshop" --assignee-principal-type 'User'
    ```

5. 保持终端窗口打开以进行后续步骤。

## 打开工作坊

按照以下步骤在 Visual Studio Code 中打开工作坊：

=== "Python"

      1. 从终端窗口执行以下命令来克隆工作坊仓库，导航到相关文件夹，设置虚拟环境，激活它，并安装必需的包：

          ```powershell
          git clone https://github.com/microsoft/build-your-first-agent-with-azure-ai-agent-service-workshop.git `
          ; cd build-your-first-agent-with-azure-ai-agent-service-workshop `
          ; python -m venv src/python/workshop/.venv `
          ; src\python\workshop\.venv\Scripts\activate `
          ; pip install -r src/python/workshop/requirements.txt `
          ; code --install-extension tomoki1207.pdf
          ```

      2. 在 VS Code 中打开。从终端窗口运行以下命令：

          ```powershell
          code .vscode\python-workspace.code-workspace
          ```

        !!! warning "当项目在 VS Code 中打开时，右下角会出现两个通知。单击 ✖ 关闭两个通知。"

=== "C#"

    1. 从终端窗口执行以下命令来克隆工作坊仓库：

        ```powershell
        git clone https://github.com/microsoft/build-your-first-agent-with-azure-ai-agent-service-workshop.git
        ```

    === "VS Code"

        1. 在 Visual Studio Code 中打开工作坊。从终端窗口运行以下命令：

            ```powershell
            code build-your-first-agent-with-azure-ai-agent-service-workshop\.vscode\csharp-workspace.code-workspace
            ```

        !!! note "当项目在 VS Code 中打开时，右下角会出现安装 C# 扩展的通知。单击**安装**来安装 C# 扩展，因为这将为 C# 开发提供必要的功能。"

    === "Visual Studio 2022"

        1. 在 Visual Studio 2022 中打开工作坊。从终端窗口运行以下命令：

            ```powershell
            start build-your-first-agent-with-azure-ai-agent-service-workshop\src\csharp\workshop\AgentWorkshop.sln
            ```

            !!! note "可能会询问您使用什么程序打开解决方案。选择 **Visual Studio 2022**。"

## Azure AI Foundry 项目端点

接下来，我们登录 Azure AI Foundry 来检索项目端点，代理应用使用它连接到 Azure AI 代理服务。

1. 导航到 [Azure AI Foundry](https://ai.azure.com){:target="_blank"} 网站。
2. 选择**登录**并使用在实验环境**资源**选项卡**顶部**找到的**用户名**和**密码**。单击**用户名**和**密码**字段以自动填写登录详细信息。
    ![Azure 凭据](../media/azure-credentials.png){:width="500"}
3. 阅读 Azure AI Foundry 简介并点击**知道了**。
4. 导航到[所有资源](https://ai.azure.com/AllResources){:target="_blank"}查看为您预配置的 AI 资源列表。
5. 选择以**aip-**开头的**Project**类型资源名称。

    ![选择项目](../media/ai-foundry-project.png){:width="500"}

6. 查看介绍指南并点击**关闭**。
7. 从**概述**侧边栏菜单中，找到**端点和密钥** -> **库** -> **Azure AI Foundry**部分，点击**复制**图标复制**Azure AI Foundry 项目端点**。

    ![复制连接字符串](../media/project-connection-string.png){:width="500"}

=== "Python"

    ## 配置工作坊

    1. 切换回您在 VS Code 中打开的工作坊。
    2. 将 `.env.sample` 文件**重命名**为 `.env`。

        - 在 VS Code **资源管理器**面板中选择 **.env.sample** 文件。
        - 右键单击文件并选择**重命名**，或按 <kbd>F2</kbd>。
        - 将文件名更改为 `.env` 并按 <kbd>Enter</kbd>。

    3. 将您从 Azure AI Foundry 复制的**项目端点**粘贴到 `.env` 文件中。

        ```python
        PROJECT_ENDPOINT="<your_project_endpoint>"
        ```

        您的 `.env` 文件应该看起来类似这样，但使用您的项目端点。

        ```python
        PROJECT_ENDPOINT="<your_project_endpoint>"
        MODEL_DEPLOYMENT_NAME="<your_model_deployment_name>"
        DEV_TUNNEL_URL="<your_dev_tunnel_url>"
        ```

    4. 保存 `.env` 文件。

    ## 项目结构

    确保熟悉您在整个工作坊中将要使用的关键**子文件夹**和**文件**。

    5. **app.py** 文件：应用程序的入口点，包含其主要逻辑。
    6. **sales_data.py** 文件：针对 SQLite 数据库执行动态 SQL 查询的函数逻辑。
    7. **stream_event_handler.py** 文件：包含令牌流传输的事件处理程序逻辑。
    8. **shared/files** 文件夹：包含代理应用创建的文件。
    9. **shared/instructions** 文件夹：包含传递给 LLM 的指令。

    ![实验文件夹结构](../media/project-structure-self-guided-python.png)

=== "C#"

    ## 配置工作坊

    1. 打开终端并导航到 **src/csharp/workshop/AgentWorkshop.Client** 文件夹。

        ```powershell
        cd build-your-first-agent-with-azure-ai-agent-service-workshop\src\csharp\workshop\AgentWorkshop.Client
        ```

    2. 将您从 Azure AI Foundry 复制的**项目端点**添加到用户机密。

        ```powershell
        dotnet user-secrets set "ConnectionStrings:AiAgentService" "<your_project_endpoint>"
        ```

    3. 将**模型部署名称**添加到用户机密。

        ```powershell
        dotnet user-secrets set "Azure:ModelName" "gpt-4o"
        ```

    4. 为使用必应搜索进行基础设定添加**必应连接 ID**到用户机密。

        ```powershell
        $subId = $(az account show --query id --output tsv)
        $rgName = "rg-agent-workshop"
        $aiAccount = "<ai_account_name>" # 替换为实际的 AI 账户名称
        $aiProject = "<ai_project_name>" # 替换为实际的 AI 项目名称
        $bingConnectionId = "/subscriptions/$subId/resourceGroups/$rgName/providers/Microsoft.CognitiveServices/accounts/$aiAccount/projects/$aiProject/connections/groundingwithbingsearch"
        dotnet user-secrets set "Azure:BingConnectionId" "$bingConnectionId"
        ```

    ## 项目结构

    确保熟悉您在整个工作坊中将要使用的关键**子文件夹**和**文件**。

    ### workshop 文件夹

    - **Lab1.cs、Lab2.cs、Lab3.cs** 文件：每个实验的入口点，包含其代理逻辑。
    - **Program.cs** 文件：应用程序的入口点，包含其主要逻辑。
    - **SalesData.cs** 文件：针对 SQLite 数据库执行动态 SQL 查询的函数逻辑。

    ### shared 文件夹

    - **files** 文件夹：包含代理应用创建的文件。
    - **fonts** 文件夹：包含代码解释器使用的多语言字体。
    - **instructions** 文件夹：包含传递给 LLM 的指令。

    ![实验文件夹结构](../media/project-structure-self-guided-csharp.png)

## 专业提示

!!! tips
    1. 实验环境右侧面板中的**汉堡菜单**提供了其他功能，包括**拆分窗口视图**和结束实验的选项。**拆分窗口视图**允许您将实验环境最大化到全屏，优化屏幕空间。实验的**说明**和**资源**面板将在单独的窗口中打开。
    2. 如果实验说明在实验环境中滚动缓慢，请尝试复制说明的 URL 并在**您计算机的本地浏览器**中打开，以获得更流畅的体验。
    3. 如果您无法查看图像，只需**单击图像将其放大**。

*使用 GitHub Copilot 翻译。*
