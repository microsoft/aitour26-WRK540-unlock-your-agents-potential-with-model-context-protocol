## Microsoft 活动参与者

本页面的说明假设您正在参加活动并且可以访问预配置的实验环境。此环境提供了一个 Azure 订阅，其中包含完成工作坊所需的所有工具和资源。

## 简介

本工作坊旨在教您 Azure AI 代理服务和相关的 [SDK](https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme?context=%2Fazure%2Fai-services%2Fagents%2Fcontext%2Fcontext){:target="_blank"}。它由多个实验组成，每个实验都突出了 Azure AI 代理服务的特定功能。实验应按顺序完成，因为每个实验都建立在前一个实验的知识和工作基础上。

## 选择工作坊编程语言

工作坊提供 Python 和 C# 两种版本。请确保使用语言选择器选项卡选择适合实验室或偏好的语言。注意，不要在工作坊中途切换语言。

**选择与您的实验室匹配的语言选项卡：**

=== "Python"
    工作坊的默认语言设置为 **Python**。

## 使用 Azure 进行身份验证

您需要使用 Azure 进行身份验证，以便代理应用可以访问 Azure AI 代理服务和模型。按照以下步骤操作：

1. 打开终端窗口。终端应用已**固定**到 Windows 11 任务栏。

    ![打开终端窗口](../../media/windows-taskbar.png){ width="300" }

2. 运行以下命令以使用 Azure 进行身份验证：

    ```powershell
    az login
    ```

    !!! note
        系统将提示您打开浏览器链接并登录到您的 Azure 账户。

        1. 浏览器窗口将自动打开，选择**工作或学校账户**，然后选择**继续**。
        1. 使用在实验环境**资源**选项卡**顶部**找到的**用户名**和 **TAP（临时访问密码）**。
        1. 选择**是，所有应用**
        1. 选择**完成**

3. 然后通过选择**Enter**从命令行选择**默认**订阅。

4. 保持终端窗口打开以进行后续步骤。

## 使用 DevTunnel 服务进行身份验证

DevTunnel 使 Azure AI 代理服务能够在工作坊期间访问您的本地 MCP 服务器。

```powershell
devtunnel login
```

!!! note
    系统将提示您使用您用于 `az login` 的账户。选择该账户并继续。

保持终端窗口打开以进行后续步骤。

## 打开工作坊

按照以下步骤在 Visual Studio Code 中打开工作坊：

=== "Python"

    以下命令块更新工作坊仓库，激活 Python 虚拟环境，并在 VS Code 中打开项目。

    将以下命令块复制并粘贴到终端，然后按**Enter**。

    ```powershell
    ; cd $HOME\aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol `
    ; git pull `
    ; .\src\python\workshop\.venv\Scripts\activate `
    ; code .vscode\python-workspace.code-workspace
    ```

    !!! warning "当项目在 VS Code 中打开时，右下角会出现两个通知。单击 ✖ 关闭两个通知。"

## 项目结构

=== "Python"

    确保熟悉您在整个工作坊中将要使用的关键**子文件夹**和**文件**。

    5. **main.py** 文件：应用程序的入口点，包含其主要逻辑。
    6. **sales_data.py** 文件：针对 SQLite 数据库执行动态 SQL 查询的函数逻辑。
    7. **stream_event_handler.py** 文件：包含令牌流传输的事件处理程序逻辑。
    8. **shared/files** 文件夹：包含代理应用创建的文件。
    9. **shared/instructions** 文件夹：包含传递给 LLM 的指令。

    ![实验文件夹结构](../../media/project-structure-self-guided-python.png)

## 专业提示

!!! tips
    1. 实验环境右侧面板中的**汉堡菜单**提供了其他功能，包括**拆分窗口视图**和结束实验的选项。**拆分窗口视图**允许您将实验环境最大化到全屏，优化屏幕空间。实验的**说明**和**资源**面板将在单独的窗口中打开。

*使用 GitHub Copilot 翻译。*
