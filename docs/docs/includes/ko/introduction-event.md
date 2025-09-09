## Microsoft 이벤트 참석자

이 페이지의 지침은 이벤트에 참석하고 미리 구성된 랩 환경에 액세스할 수 있다고 가정합니다. 이 환경은 워크숍을 완료하는 데 필요한 모든 도구와 리소스가 포함된 Azure 구독을 제공합니다.

## 소개

이 워크숍은 Azure AI Agents Service와 관련 [SDK](https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme?context=%2Fazure%2Fai-services%2Fagents%2Fcontext%2Fcontext){:target="_blank"}에 대해 배우도록 설계되었습니다. 여러 랩으로 구성되어 있으며, 각 랩은 Azure AI Agents Service의 특정 기능을 강조합니다. 랩은 순서대로 완료하도록 되어 있으며, 각 랩은 이전 랩의 지식과 작업을 기반으로 합니다.

## 워크숍 클라우드 리소스

랩 Azure 구독에 다음 리소스가 미리 프로비저닝되어 있습니다:

- **rg-zava-agent-wks-nnnnnnnn**이라는 리소스 그룹
- **fdy-zava-agent-wks-nnnnnnnn**이라는 **Azure AI Foundry hub**
- **prj-zava-agent-wks-nnnnnnnn**이라는 **Azure AI Foundry project**
- 두 개의 모델이 배포되어 있습니다: **gpt-4o-mini**와 **text-embedding-3-small**. [가격 보기.](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/){:target="\_blank"}
- **pg-zava-agent-wks-nnnnnnnn**이라는 Azure Database for PostgreSQL Flexible Server (B1ms Burstable 32GB) 데이터베이스. [가격 보기](https://azure.microsoft.com/pricing/details/postgresql/flexible-server){:target="\_blank"}
- **appi-zava-agent-wks-nnnnnnnn**이라는 Application Insights 리소스. [가격 보기](https://azure.microsoft.com/pricing/calculator/?service=monitor){:target="\_blank"}

## 워크숍 프로그래밍 언어 선택

워크숍은 Python과 C# 모두에서 사용할 수 있습니다. 언어 선택기 탭을 사용하여 랩실이나 선호도에 맞는 언어를 선택하세요. 참고: 워크숍 중간에 언어를 변경하지 마세요.

**랩실과 일치하는 언어 탭을 선택하세요:**

=== "Python"
    워크숍의 기본 언어는 **Python**으로 설정되어 있습니다.
=== "C#"
    워크숍의 기본 언어는 **C#**으로 설정되어 있습니다.

    !!! warning "이 워크숍의 C#/.NET 버전은 베타 버전이며 알려진 안정성 문제가 있습니다."

    워크숍을 시작하기 **전에** [문제 해결 가이드](../../en/dotnet-troubleshooting.md) 섹션을 반드시 읽어보세요. 아니면 워크숍의 **Python** 버전을 선택하세요.

## Azure 인증

에이전트 앱이 Azure AI Agents Service와 모델에 액세스할 수 있도록 Azure로 인증해야 합니다. 다음 단계를 따르세요:

1. 터미널 창을 엽니다. 터미널 앱은 Windows 11 작업 표시줄에 **고정**되어 있습니다.

    ![터미널 창 열기](../../media/windows-taskbar.png){ width="300" }

2. 다음 명령을 실행하여 Azure로 인증합니다:

    ```powershell
    az login
    ```

    !!! note
        브라우저 링크를 열고 Azure 계정에 로그인하라는 메시지가 표시됩니다.

        1. 브라우저 창이 자동으로 열리면 **회사 또는 학교 계정**을 선택한 다음 **계속**을 선택합니다.
        1. 랩 환경의 **Resources** 탭 **상단 섹션**에 있는 **Username**과 **TAP (Temporary Access Pass)**를 사용합니다.
        1. **네, 모든 앱**을 선택합니다
        1. **완료**를 선택합니다

3. 그런 다음 **Enter**를 선택하여 명령줄에서 **Default** 구독을 선택합니다.

4. 다음 단계를 위해 터미널 창을 열어 둡니다.

## DevTunnel Service 인증

DevTunnel은 워크숍 중에 Azure AI Agents Service가 로컬 MCP Server에 액세스할 수 있도록 합니다.

```powershell
devtunnel login
```

!!! note
    `az login`에 사용한 계정을 사용하라는 메시지가 표시됩니다. 계정을 선택하고 계속 진행하세요.

다음 단계를 위해 터미널 창을 열어 둡니다.

## 워크숍 열기

Visual Studio Code에서 워크숍을 열려면 다음 단계를 따르세요:

=== "Python"

    다음 명령 블록은 워크숍 저장소를 업데이트하고, Python 가상 환경을 활성화하며, VS Code에서 프로젝트를 엽니다.

    다음 명령 블록을 터미널에 복사하여 붙여넣고 **Enter**를 누릅니다.

    ```powershell
    ; cd $HOME\aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol `
    ; git pull `
    ; .\src\python\workshop\.venv\Scripts\activate `
    ; code .vscode\python-workspace.code-workspace
    ```

    !!! warning "프로젝트가 VS Code에서 열릴 때 오른쪽 하단 모서리에 두 개의 알림이 나타납니다. ✖를 클릭하여 두 알림을 모두 닫습니다."

=== "C#"

    === "VS Code"

        1. Visual Studio Code에서 워크숍을 엽니다. 터미널 창에서 다음 명령을 실행합니다:

            ```powershell
            ; cd $HOME\aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol `
            ; git pull `
            ;code .vscode\csharp-workspace.code-workspace
            ```

        !!! note "프로젝트가 VS Code에서 열릴 때 C# 확장을 설치하라는 알림이 오른쪽 하단 모서리에 나타납니다. C# 개발에 필요한 기능을 제공하므로 **Install**을 클릭하여 C# 확장을 설치합니다."

    === "Visual Studio 2022"

        2. Visual Studio 2022에서 워크숍을 엽니다. 터미널 창에서 다음 명령을 실행합니다:

            ```powershell
            ; git pull `
            ;cd $HOME; start .\aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol\src\csharp\McpAgentWorkshop.slnx
            ```

            !!! note "솔루션을 열 때 사용할 프로그램을 묻는 메시지가 나타날 수 있습니다. **Visual Studio 2022**를 선택합니다."

## 프로젝트 구조

=== "Python"

    워크숍 전반에 걸쳐 작업할 주요 **하위 폴더**와 **파일**을 숙지하세요.

    5. **main.py** 파일: 메인 로직을 포함하는 앱의 진입점입니다.
    6. **sales_data.py** 파일: SQLite 데이터베이스에 대한 동적 SQL 쿼리를 실행하는 함수 로직입니다.
    7. **stream_event_handler.py** 파일: 토큰 스트리밍을 위한 이벤트 핸들러 로직을 포함합니다.
    8. **shared/files** 폴더: 에이전트 앱이 생성한 파일을 포함합니다.
    9. **shared/instructions** 폴더: LLM에 전달되는 지시사항을 포함합니다.

    ![랩 폴더 구조](../../media/project-structure-self-guided-python.png)

=== "C#"

    ## 프로젝트 구조

    이 프로젝트는 [Aspire](http://aka.ms/dotnet-aspire)를 사용하여 에이전트 애플리케이션 구축, MCP 서버 관리, 모든 외부 종속성 오케스트레이션을 단순화합니다. 솔루션은 모두 `McpAgentWorkshop` 접두사가 붙은 네 개의 프로젝트로 구성됩니다:

    * `AppHost`: Aspire 오케스트레이터이며 워크숍의 실행 프로젝트입니다.
    * `McpServer`: MCP 서버 프로젝트입니다.
    * `ServiceDefaults`: 로깅 및 원격 측정과 같은 서비스의 기본 구성입니다.
    * `WorkshopApi`: 워크숍용 Agent API입니다. 핵심 애플리케이션 로직은 `AgentService` 클래스에 있습니다.

    솔루션의 .NET 프로젝트 외에도 `shared` 폴더(솔루션 폴더로 표시되고 파일 탐색기를 통해 보임)가 있으며, 여기에는 다음이 포함됩니다:

    * `instructions`: LLM에 전달되는 지시사항.
    * `scripts`: 다양한 작업을 위한 도우미 셸 스크립트로, 필요할 때 참조됩니다.
    * `webapp`: 프런트엔드 클라이언트 애플리케이션. 참고: 이것은 Aspire가 라이프사이클을 관리하는 Python 애플리케이션입니다.

    ![랩 폴더 구조](../../media/project-structure-self-guided-csharp.png)

## 프로 팁

!!! tips
    1. 랩 환경의 오른쪽 패널에 있는 **Burger Menu**는 **Split Window View**와 랩을 종료하는 옵션을 포함한 추가 기능을 제공합니다. **Split Window View**를 사용하면 랩 환경을 전체 화면으로 최대화하여 화면 공간을 최적화할 수 있습니다. 랩의 **Instructions**와 **Resources** 패널이 별도의 창에서 열립니다.

*GitHub Copilot을 사용하여 번역됨.*
