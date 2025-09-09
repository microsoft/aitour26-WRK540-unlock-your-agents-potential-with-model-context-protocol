# 入门工作区

工作坊中有两个 VS Code 工作区，一个用于 Python，一个用于 C#。工作区包含源代码和完成每种语言实验所需的所有文件。选择与您要使用的语言匹配的工作区。

=== "Python"

    1. **复制**以下路径到剪贴板：

        ```text
        /workspace/.vscode/python-workspace.code-workspace
        ```
    2. 从 VS Code 菜单中，选择**文件**然后**从文件打开工作区**。
    3. 替换并**粘贴**复制的路径名称，然后选择**确定**。


    ## 项目结构

    熟悉您在整个工作坊中要使用的工作区中的关键**文件夹**和**文件**。

    ### "workshop"文件夹

    - **app.py** 文件：应用程序的入口点，包含其主要逻辑。

    注意 **INSTRUCTIONS_FILE** 变量——它设置代理使用的指令文件。您将在后续实验中更新此变量。

    - **resources.txt** 文件：包含代理应用程序使用的资源。
    - **.env** 文件：包含代理应用程序使用的环境变量。

    ### "mcp_server"文件夹

    - **sales_analysis.py** 文件：具有销售分析工具的 MCP 服务器。

    ### "shared/instructions"文件夹

    - **instructions** 文件夹：包含传递给 LLM 的指令。

    ![实验文件夹结构](media/project-structure-self-guided-python.png)

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

    ![实验文件夹结构](media/project-structure-self-guided-csharp.png)

*使用 GitHub Copilot 翻译。*
