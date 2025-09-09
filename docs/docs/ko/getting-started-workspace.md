워크샵에는 Python용과 C#용 두 개의 VS Code 워크스페이스가 있습니다. 워크스페이스에는 각 언어의 랩을 완료하는 데 필요한 소스 코드와 모든 파일이 포함되어 있습니다. 작업하려는 언어와 일치하는 워크스페이스를 선택하세요.

=== "Python"

    1. 다음 경로를 클립보드에 **복사**하세요:

        ```text
        /workspace/.vscode/python-workspace.code-workspace
        ```
    1. VS Code 메뉴에서 **File**을 선택한 다음 **Open Workspace from File**을 선택하세요.
    3. 복사한 경로명을 **바꿔서 붙여넣고** **OK**를 선택하세요.


    ## 프로젝트 구조

    워크샵 전반에 걸쳐 작업할 워크스페이스의 주요 **폴더**와 **파일**에 익숙해지세요.

    ### "workshop" 폴더

    - **app.py** 파일: 주요 로직을 포함하는 앱의 진입점입니다.

    **INSTRUCTIONS_FILE** 변수를 주목하세요—이것은 에이전트가 사용하는 지침 파일을 설정합니다. 나중 랩에서 이 변수를 업데이트할 것입니다.

    - **resources.txt** 파일: 에이전트 앱에서 사용하는 리소스를 포함합니다.
    - **.env** 파일: 에이전트 앱에서 사용하는 환경 변수를 포함합니다.

    ### "mcp_server" 폴더

    - **sales_analysis.py** 파일: 판매 분석용 도구가 있는 MCP 서버입니다.

    ### "shared/instructions" 폴더

    - **instructions** 폴더: LLM에 전달되는 지침을 포함합니다.

    ![랩 폴더 구조](media/project-structure-self-guided-python.png)

=== "C#"

    1. Visual Studio Code에서 **File** > **Open Workspace from File**로 이동하세요.
    2. 기본 경로를 다음으로 바꾸세요:

        ```text
        /workspace/.vscode/csharp-workspace.code-workspace
        ```

    3. **OK**를 선택하여 워크스페이스를 여세요.

    ## 프로젝트 구조

    프로젝트는 [Aspire](http://aka.ms/dotnet-aspire)를 사용하여 에이전트 애플리케이션 구축, MCP 서버 관리, 모든 외부 의존성 조정을 단순화합니다. 솔루션은 `McpAgentWorkshop` 접두사가 붙은 네 개의 프로젝트로 구성됩니다:

    * `AppHost`: Aspire 오케스트레이터이자 워크샵의 시작 프로젝트입니다.
    * `McpServer`: MCP 서버 프로젝트입니다.
    * `ServiceDefaults`: 로깅 및 원격 측정과 같은 서비스의 기본 구성입니다.
    * `WorkshopApi`: 워크샵용 에이전트 API입니다. 핵심 애플리케이션 로직은 `AgentService` 클래스에 있습니다.

    솔루션의 .NET 프로젝트 외에도 `shared` 폴더(솔루션 폴더로 표시되고 파일 탐색기를 통해 볼 수 있음)가 있으며, 여기에는 다음이 포함됩니다:

    * `instructions`: LLM에 전달되는 지침입니다.
    * `scripts`: 다양한 작업을 위한 헬퍼 셸 스크립트로, 필요할 때 참조됩니다.
    * `webapp`: 프론트엔드 클라이언트 애플리케이션입니다. 참고: 이것은 Aspire가 생명주기를 관리할 Python 애플리케이션입니다.

    ![랩 폴더 구조](media/project-structure-self-guided-csharp.png)

*GitHub Copilot을 사용하여 번역됨.*
