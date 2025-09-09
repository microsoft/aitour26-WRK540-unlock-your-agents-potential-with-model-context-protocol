## 자습식 학습자

이 지침은 미리 구성된 랩 환경에 액세스할 수 없는 자습식 학습자를 위한 것입니다. 다음 단계에 따라 환경을 설정하고 워크숍을 시작하세요.

## 소개

이 워크숍은 Azure AI Agents Service와 관련 SDK에 대해 배우도록 설계되었습니다. 여러 랩으로 구성되어 있으며, 각 랩은 Azure AI Agents Service의 특정 기능을 강조합니다. 랩은 순서대로 완료하도록 되어 있으며, 각 랩은 이전 랩의 지식과 작업을 기반으로 합니다.

## 전제 조건

1. Azure 구독에 대한 액세스. Azure 구독이 없으면 시작하기 전에 [무료 계정](https://azure.microsoft.com/free/){:target="_blank"}을 만드세요.
1. GitHub 계정이 필요합니다. 없으면 [GitHub](https://github.com/join){:target="_blank"}에서 만드세요.

## 워크숍 프로그래밍 언어 선택

워크숍은 Python과 C# 모두에서 사용할 수 있습니다. 언어 선택기 탭을 사용하여 선호하는 언어를 선택하세요. 참고: 워크숍 중간에 언어를 변경하지 마세요.

**선호하는 언어의 탭을 선택하세요:**

=== "Python"
    워크숍의 기본 언어는 **Python**으로 설정되어 있습니다.
=== "C#"
    워크숍의 기본 언어는 **C#**으로 설정되어 있습니다.

    !!! warning "이 워크숍의 C#/.NET 버전은 베타 버전이며 알려진 안정성 문제가 있습니다."

    워크숍을 시작하기 **전에** [문제 해결 가이드](../../en/dotnet-troubleshooting.md) 섹션을 반드시 읽어보세요. 아니면 워크숍의 **Python** 버전을 선택하세요.

## 워크숍 열기

선호: 필요한 모든 도구가 미리 구성된 환경을 제공하는 **GitHub Codespaces**. 또는 Visual Studio Code **Dev Container**와 **Docker**를 사용하여 로컬에서 실행하세요. 아래 탭을 사용하여 선택하세요.

!!! Tip
    Codespaces 또는 Dev Container 빌드에는 약 5분이 걸립니다. 빌드를 시작한 다음 완료되는 동안 **계속 읽어보세요**.

=== "GitHub Codespaces"

    **Open in GitHub Codespaces**를 선택하여 GitHub Codespaces에서 프로젝트를 엽니다.

    [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/microsoft/aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol){:target="_blank"}

=== "VS Code Dev Container"

    1. 로컬 머신에 다음이 설치되어 있는지 확인하세요:

        - [Docker](https://docs.docker.com/get-docker/){:target="\_blank"}
        - [Visual Studio Code](https://code.visualstudio.com/download){:target="\_blank"}
        - [Remote - Containers 확장](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers){:target="\_blank"}
    1. 저장소를 로컬 머신에 복제하세요:

        ```bash
        git clone https://github.com/microsoft/aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol.git
        ```

    1. Visual Studio Code에서 복제된 저장소를 엽니다.
    1. 메시지가 표시되면 **Reopen in Container**를 선택하여 Dev Container에서 프로젝트를 엽니다.

---

## Azure 서비스 인증

!!! danger
계속하기 전에 Codespace 또는 Dev Container가 완전히 빌드되어 준비되었는지 확인하세요.

### DevTunnel 인증

DevTunnel은 워크숍에서 Azure AI Agents Service가 로컬 개발 환경에서 실행할 MCP Server에 액세스할 수 있도록 하는 포트 포워딩 서비스를 제공합니다. 인증하려면 다음 단계를 따르세요:

1. VS Code에서 <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>`</kbd>를 **눌러** 새 터미널 창을 엽니다. 그런 다음 다음 명령을 실행합니다:
1. **다음 명령을 실행**하여 DevTunnel로 인증합니다:

   ```shell
   devtunnel login
   ```

1. 인증하려면 다음 단계를 따르세요:

   1. **Authentication Code**를 클립보드에 복사하세요.
   2. <kbd>ctrl</kbd> 또는 <kbd>cmd</kbd> 키를 **누르고 있으세요**.
   3. 브라우저에서 열 수 있도록 인증 URL을 **선택**하세요.
   4. 코드를 **붙여넣고** **Next**를 클릭하세요.
   5. **계정을 선택**하고 로그인하세요.
   6. **Continue**를 선택하세요
   7. VS Code의 터미널 창으로 **돌아가세요**.

1. 다음 단계를 위해 터미널 창을 **열어** 둡니다.

### Azure 인증

에이전트 앱이 Azure AI Agents Service와 모델에 액세스할 수 있도록 Azure로 인증합니다. 다음 단계를 따르세요:

1. 그런 다음 다음 명령을 실행합니다:

    ```shell
    az login --use-device-code
    ```

    !!! warning
    여러 Azure 테넌트가 있는 경우 올바른 테넌트를 지정하세요:

    ```shell
    az login --use-device-code --tenant <tenant_id>
    ```

2. 인증하려면 다음 단계를 따르세요:

    1. **Authentication Code**를 클립보드에 **복사**하세요.
    2. <kbd>ctrl</kbd> 또는 <kbd>cmd</kbd> 키를 **누르고 있으세요**.
    3. 브라우저에서 열 수 있도록 인증 URL을 **선택**하세요.
    4. 코드를 **붙여넣고** **Next**를 클릭하세요.
    5. **계정을 선택**하고 로그인하세요.
    6. **Continue**를 선택하세요
    7. VS Code의 터미널 창으로 **돌아가세요**.
    8. 메시지가 표시되면 구독을 **선택**하세요.

3. 다음 단계를 위해 터미널 창을 열어 둡니다.

---

## Azure 리소스 배포

이 배포는 Azure 구독에 다음 리소스를 생성합니다.

- **rg-zava-agent-wks-nnnnnnnn**이라는 리소스 그룹
- **fdy-zava-agent-wks-nnnnnnnn**이라는 **Azure AI Foundry hub**
- **prj-zava-agent-wks-nnnnnnnn**이라는 **Azure AI Foundry project**
- 두 개의 모델이 배포되어 있습니다: **gpt-4o-mini**와 **text-embedding-3-small**. [가격 보기.](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/){:target="\_blank"}
- **appi-zava-agent-wks-nnnnnnnn**이라는 Application Insights 리소스. [가격 보기](https://azure.microsoft.com/pricing/calculator/?service=monitor){:target="\_blank"}
- 워크숍 비용을 낮게 유지하기 위해 PostgreSQL은 클라우드 서비스가 아닌 Codespace 또는 Dev Container 내의 로컬 컨테이너에서 실행됩니다. 관리형 PostgreSQL 서비스의 옵션에 대해 알아보려면 [Azure Database for PostgreSQL Flexible Server](https://azure.microsoft.com/en-us/products/postgresql){:target="\_blank"}를 참조하세요.

!!! warning "다음 모델 할당량이 최소한 있는지 확인하세요" - 에이전트가 빈번한 모델 호출을 하므로 gpt-4o-mini Global Standard SKU에 대한 120K TPM 할당량. - text-embedding-3-small 모델 Global Standard SKU에 대한 50K TPM. - [AI Foundry Management Center](https://ai.azure.com/managementCenter/quota){:target="\_blank"}에서 할당량을 확인하세요."

### 자동화된 배포

다음 bash 스크립트를 실행하여 워크숍에 필요한 리소스 배포를 자동화합니다. `deploy.sh` 스크립트는 기본적으로 `westus` 지역에 리소스를 배포합니다. 스크립트를 실행하려면:

```bash
cd infra && ./deploy.sh
```

### 워크숍 구성

=== "Python"

    #### Azure 리소스 구성

    배포 스크립트는 프로젝트 및 모델 엔드포인트, 모델 배포 이름, Application Insights 연결 문자열이 포함된 **.env** 파일을 생성합니다. .env 파일은 자동으로 `src/python/workshop` 폴더에 저장됩니다.

    **.env** 파일은 사용자의 값으로 업데이트되어 다음과 같이 표시됩니다:

    ```python
    PROJECT_ENDPOINT="<your_project_endpoint>"
    GPT_MODEL_DEPLOYMENT_NAME="<your_model_deployment_name>"
    EMBEDDING_MODEL_DEPLOYMENT_NAME="<your_embedding_model_deployment_name>"
    APPLICATIONINSIGHTS_CONNECTION_STRING="<your_application_insights_connection_string>"
    AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED="true"
    AZURE_OPENAI_ENDPOINT="<your_azure_openai_endpoint>"
    ```

    #### Azure 리소스 이름

    `workshop` 폴더에 `resources.txt`라는 파일도 있습니다. 이 파일에는 배포 중에 생성된 Azure 리소스의 이름이 포함되어 있습니다.

    다음과 같이 표시됩니다:

    ```plaintext
    Azure AI Foundry Resources:
    - Resource Group Name: rg-zava-agent-wks-nnnnnnnn
    - AI Project Name: prj-zava-agent-wks-nnnnnnnn
    - Foundry Resource Name: fdy-zava-agent-wks-nnnnnnnn
    - Application Insights Name: appi-zava-agent-wks-nnnnnnnn
    ```

=== "C#"

    스크립트는 [ASP.NET Core 개발 비밀](https://learn.microsoft.com/aspnet/core/security/app-secrets){:target="_blank"}용 Secret Manager를 사용하여 프로젝트 변수를 안전하게 저장합니다.

    VS Code에서 C# 워크스페이스를 연 후 다음 명령을 실행하여 비밀을 볼 수 있습니다:

    ```bash
    dotnet user-secrets list
    ```

---

## VS Code 워크스페이스 열기

워크숍에는 Python용과 C#용으로 두 개의 VS Code 워크스페이스가 있습니다. 워크스페이스에는 각 언어에 대한 랩을 완료하는 데 필요한 소스 코드와 모든 파일이 포함되어 있습니다. 작업하려는 언어와 일치하는 워크스페이스를 선택하세요.

=== "Python"

    1. 다음 경로를 클립보드에 **복사**하세요:

        ```text
        /workspace/.vscode/python-workspace.code-workspace
        ```
    1. VS Code 메뉴에서 **File**을 선택한 다음 **Open Workspace from File**을 선택하세요.
    3. 복사한 경로 이름을 바꾸고 **붙여넣은** 다음 **OK**를 선택하세요.


    ## 프로젝트 구조

    워크숍 전반에 걸쳐 작업할 워크스페이스의 주요 **폴더**와 **파일**을 숙지하세요.

    ### "workshop" 폴더

    - **app.py** 파일: 메인 로직을 포함하는 앱의 진입점입니다.

    **INSTRUCTIONS_FILE** 변수를 확인하세요. 이 변수는 에이전트가 사용하는 지시사항 파일을 설정합니다. 이후 랩에서 이 변수를 업데이트할 예정입니다.

    - **resources.txt** 파일: 에이전트 앱이 사용하는 리소스를 포함합니다.
    - **.env** 파일: 에이전트 앱이 사용하는 환경 변수를 포함합니다.

    ### "mcp_server" 폴더

    - **sales_analysis.py** 파일: 영업 분석용 도구가 포함된 MCP Server입니다.

    ### "shared/instructions" 폴더

    - **instructions** 폴더: LLM에 전달되는 지시사항을 포함합니다.

    ![랩 폴더 구조](../../media/project-structure-self-guided-python.png)

=== "C#"

    1. Visual Studio Code에서 **File** > **Open Workspace from File**로 이동하세요.
    2. 기본 경로를 다음으로 바꾸세요:

        ```text
        /workspace/.vscode/csharp-workspace.code-workspace
        ```

    3. **OK**를 선택하여 워크스페이스를 엽니다.

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

*GitHub Copilot을 사용하여 번역됨.*
