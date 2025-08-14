워크샵에는 Python용과 C#용 두 개의 VS Code 워크스페이스가 있습니다. 워크스페이스에는 각 언어별 랩을 완료하는 데 필요한 소스 코드와 모든 파일이 포함되어 있습니다. 작업하고자 하는 언어와 일치하는 워크스페이스를 선택하세요.

=== "Python"

    1. 다음 경로를 클립보드에 **복사**합니다:

        ```text
        /workspace/.vscode/python-workspace.code-workspace
        ```
    1. VS Code 메뉴에서 **File**을 선택한 다음 **Open Workspace from File**을 선택합니다.
    3. 복사한 경로명을 **붙여넣기**하고 **OK**를 선택합니다.


    ## 프로젝트 구조

    워크샵 전반에 걸쳐 작업할 워크스페이스의 주요 **폴더**와 **파일**에 익숙해지세요.

    ### "workshop" 폴더

    - **app.py** 파일: 앱의 진입점으로 주요 로직을 포함합니다.
  
    **INSTRUCTIONS_FILE** 변수를 주목하세요—이 변수는 에이전트가 사용할 지침 파일을 설정합니다. 이후 랩에서 이 변수를 업데이트할 것입니다.

    - **resources.txt** 파일: 에이전트 앱에서 사용하는 리소스를 포함합니다.
    - **.env** 파일: 에이전트 앱에서 사용하는 환경 변수를 포함합니다.

    ### "mcp_server" 폴더

    - **sales_analysis.py** 파일: 판매 분석을 위한 도구가 있는 MCP 서버입니다.

    ### "shared/instructions" 폴더

    - **instructions** 폴더: LLM에 전달되는 지침을 포함합니다.

    ![랩 폴더 구조](media/project-structure-self-guided-python.png)

=== "C#"

    1. Visual Studio Code에서 **File** > **Open Workspace from File**로 이동합니다.
    2. 기본 경로를 다음으로 바꿉니다:

        ```text
        /workspace/.vscode/csharp-workspace.code-workspace
        ```

    3. **OK**를 선택하여 워크스페이스를 엽니다.

    ## 프로젝트 구조

    워크샵 전반에 걸쳐 작업할 주요 **폴더**와 **파일**에 익숙해지세요.

    ### workshop 폴더

    - **Lab1.cs, Lab2.cs, Lab3.cs** 파일: 각 랩의 진입점으로 에이전트 로직을 포함합니다.
    - **Program.cs** 파일: 앱의 진입점으로 주요 로직을 포함합니다.
    - **SalesData.cs** 파일: SQLite 데이터베이스에 대한 동적 SQL 쿼리를 실행하는 함수 로직입니다.

    ### shared 폴더

    - **files** 폴더: 에이전트 앱에서 생성한 파일을 포함합니다.
    - **fonts** 폴더: 코드 인터프리터에서 사용하는 다국어 폰트를 포함합니다.
    - **instructions** 폴더: LLM에 전달되는 지침을 포함합니다.

    ![랩 폴더 구조](media/project-structure-self-guided-csharp.png)

*GitHub Copilot을 사용하여 번역되었습니다.*
