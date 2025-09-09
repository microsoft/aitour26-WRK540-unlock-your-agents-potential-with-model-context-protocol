## Microsoft 이벤트 참석자

이 페이지의 지침은 [Microsoft Event 2025](https://build.microsoft.com/){:target="_blank"}에 참석하고 미리 구성된 랩 환경에 액세스할 수 있다고 가정합니다. 이 환경은 워크숍을 완료하는 데 필요한 모든 도구와 리소스가 포함된 Azure 구독을 제공합니다.

## 소개

이 워크숍은 Azure AI Agents Service와 관련 [SDK](https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme?context=%2Fazure%2Fai-services%2Fagents%2Fcontext%2Fcontext){:target="_blank"}에 대해 배우도록 설계되었습니다. 여러 랩으로 구성되어 있으며, 각 랩은 Azure AI Agents Service의 특정 기능을 강조합니다. 랩은 순서대로 완료하도록 되어 있으며, 각 랩은 이전 랩의 지식과 작업을 기반으로 합니다.

## 워크숍 프로그래밍 언어 선택

워크숍은 Python과 C# 모두에서 사용할 수 있습니다. 언어 선택기 탭을 사용하여 자신이 있는 랩실에 맞는 언어를 선택하세요. 참고: 워크숍 중간에 언어를 변경하지 마세요.

**랩실과 일치하는 언어 탭을 선택하세요:**

=== "Python"
    워크숍의 기본 언어는 **Python**으로 설정되어 있습니다.
=== "C#"
    워크숍의 기본 언어는 **C#**으로 설정되어 있습니다.

## Azure 인증

에이전트 앱이 Azure AI Agents Service와 모델에 액세스할 수 있도록 Azure로 인증해야 합니다. 다음 단계를 따르세요:

1. 터미널 창을 엽니다. 터미널 앱은 Windows 11 작업 표시줄에 **고정**되어 있습니다.

    ![터미널 창 열기](../media/windows-taskbar.png){ width="300" }

2. 다음 명령을 실행하여 Azure로 인증합니다:

    ```powershell
    az login
    ```

    !!! note
        브라우저 링크를 열고 Azure 계정에 로그인하라는 메시지가 표시됩니다.

        1. 브라우저 창이 자동으로 열리면 **회사 또는 학교 계정**을 선택한 다음 **계속**을 선택합니다.

        1. 랩 환경의 **Resources** 탭 **상단 섹션**에 있는 **Username**과 **Password**를 사용합니다.

        2. **네, 모든 앱**을 선택합니다

3. 그런 다음 **Enter**를 선택하여 명령줄에서 **Default** 구독을 선택합니다.

4. 로그인한 후 다음 명령을 실행하여 리소스 그룹에 **사용자** 역할을 할당합니다:

    ```powershell
    $subId = $(az account show --query id --output tsv) `
    ;$objectId = $(az ad signed-in-user show --query id -o tsv) `
    ; az role assignment create --role "f6c7c914-8db3-469d-8ca1-694a8f32e121" --assignee-object-id $objectId --scope /subscriptions/$subId/resourceGroups/"rg-agent-workshop" --assignee-principal-type 'User'
    ```

5. 다음 단계를 위해 터미널 창을 열어 둡니다.

## 워크숍 열기

Visual Studio Code에서 워크숍을 열려면 다음 단계를 따르세요:

=== "Python"

      1. 터미널 창에서 다음 명령을 실행하여 워크숍 저장소를 복제하고, 관련 폴더로 이동하며, 가상 환경을 설정하고 활성화한 후 필요한 패키지를 설치합니다:

          ```powershell
          git clone https://github.com/microsoft/build-your-first-agent-with-azure-ai-agent-service-workshop.git `
          ; cd build-your-first-agent-with-azure-ai-agent-service-workshop `
          ; python -m venv src/python/workshop/.venv `
          ; src\python\workshop\.venv\Scripts\activate `
          ; pip install -r src/python/workshop/requirements.txt `
          ; code --install-extension tomoki1207.pdf
          ```

      2. VS Code에서 열기. 터미널 창에서 다음 명령을 실행합니다:

          ```powershell
          code .vscode\python-workspace.code-workspace
          ```

        !!! warning "프로젝트가 VS Code에서 열릴 때 오른쪽 하단 모서리에 두 개의 알림이 나타납니다. ✖를 클릭하여 두 알림을 모두 닫습니다."

=== "C#"

    1. 터미널 창에서 다음 명령을 실행하여 워크숍 저장소를 복제합니다:

        ```powershell
        git clone https://github.com/microsoft/build-your-first-agent-with-azure-ai-agent-service-workshop.git
        ```

    === "VS Code"

        1. Visual Studio Code에서 워크숍을 엽니다. 터미널 창에서 다음 명령을 실행합니다:

            ```powershell
            code build-your-first-agent-with-azure-ai-agent-service-workshop\.vscode\csharp-workspace.code-workspace
            ```

        !!! note "프로젝트가 VS Code에서 열릴 때 C# 확장을 설치하라는 알림이 오른쪽 하단 모서리에 나타납니다. C# 개발에 필요한 기능을 제공하므로 **Install**을 클릭하여 C# 확장을 설치합니다."

    === "Visual Studio 2022"

        1. Visual Studio 2022에서 워크숍을 엽니다. 터미널 창에서 다음 명령을 실행합니다:

            ```powershell
            start build-your-first-agent-with-azure-ai-agent-service-workshop\src\csharp\workshop\AgentWorkshop.sln
            ```

            !!! note "솔루션을 열 때 사용할 프로그램을 묻는 메시지가 나타날 수 있습니다. **Visual Studio 2022**를 선택합니다."

## Azure AI Foundry 프로젝트 엔드포인트

다음으로, Azure AI Foundry에 로그인하여 에이전트 앱이 Azure AI Agents Service에 연결하는 데 사용하는 프로젝트 엔드포인트를 검색합니다.

1. [Azure AI Foundry](https://ai.azure.com){:target="_blank"} 웹사이트로 이동합니다.
2. **Sign in**을 선택하고 랩 환경의 **Resources** 탭 **상단 섹션**에 있는 **Username**과 **Password**를 사용합니다. **Username**과 **Password** 필드를 클릭하면 로그인 세부 정보가 자동으로 채워집니다.
    ![Azure 자격 증명](../media/azure-credentials.png){:width="500"}
3. Azure AI Foundry 소개를 읽고 **Got it**을 클릭합니다.
4. [All Resources](https://ai.azure.com/AllResources){:target="_blank"}로 이동하여 미리 프로비저닝된 AI 리소스 목록을 봅니다.
5. **Project** 유형의 **aip-**로 시작하는 리소스 이름을 선택합니다.

    ![프로젝트 선택](../media/ai-foundry-project.png){:width="500"}

6. 소개 가이드를 검토하고 **Close**를 클릭합니다.
7. **Overview** 사이드바 메뉴에서 **Endpoints and keys** -> **Libraries** -> **Azure AI Foundry** 섹션을 찾아 **Copy** 아이콘을 클릭하여 **Azure AI Foundry project endpoint**를 복사합니다.

    ![연결 문자열 복사](../media/project-connection-string.png){:width="500"}

=== "Python"

    ## 워크숍 구성

    1. VS Code에서 연 워크숍으로 다시 전환합니다.
    2. `.env.sample` 파일을 `.env`로 **이름 변경**합니다.

        - VS Code **Explorer** 패널에서 **.env.sample** 파일을 선택합니다.
        - 파일을 마우스 오른쪽 버튼으로 클릭하고 **Rename**을 선택하거나 <kbd>F2</kbd>를 누릅니다.
        - 파일 이름을 `.env`로 변경하고 <kbd>Enter</kbd>를 누릅니다.

    3. Azure AI Foundry에서 복사한 **Project endpoint**를 `.env` 파일에 붙여넣습니다.

        ```python
        PROJECT_ENDPOINT="<your_project_endpoint>"
        ```

        `.env` 파일은 이와 비슷해야 하지만 사용자의 프로젝트 엔드포인트가 포함되어야 합니다.

        ```python
        PROJECT_ENDPOINT="<your_project_endpoint>"
        MODEL_DEPLOYMENT_NAME="<your_model_deployment_name>"
        DEV_TUNNEL_URL="<your_dev_tunnel_url>"
        ```

    4. `.env` 파일을 저장합니다.

    ## 프로젝트 구조

    워크숍 전반에 걸쳐 작업할 주요 **하위 폴더**와 **파일**을 숙지하세요.

    5. **app.py** 파일: 메인 로직을 포함하는 앱의 진입점입니다.
    6. **sales_data.py** 파일: SQLite 데이터베이스에 대한 동적 SQL 쿼리를 실행하는 함수 로직입니다.
    7. **stream_event_handler.py** 파일: 토큰 스트리밍을 위한 이벤트 핸들러 로직을 포함합니다.
    8. **shared/files** 폴더: 에이전트 앱이 생성한 파일을 포함합니다.
    9. **shared/instructions** 폴더: LLM에 전달되는 지시사항을 포함합니다.

    ![랩 폴더 구조](../media/project-structure-self-guided-python.png)

=== "C#"

    ## 워크숍 구성

    1. 터미널을 열고 **src/csharp/workshop/AgentWorkshop.Client** 폴더로 이동합니다.

        ```powershell
        cd build-your-first-agent-with-azure-ai-agent-service-workshop\src\csharp\workshop\AgentWorkshop.Client
        ```

    2. Azure AI Foundry에서 복사한 **Project endpoint**를 사용자 비밀에 추가합니다.

        ```powershell
        dotnet user-secrets set "ConnectionStrings:AiAgentService" "<your_project_endpoint>"
        ```

    3. **Model deployment name**을 사용자 비밀에 추가합니다.

        ```powershell
        dotnet user-secrets set "Azure:ModelName" "gpt-4o"
        ```

    4. Bing 검색으로 그라운딩을 위해 **Bing connection ID**를 사용자 비밀에 추가합니다.

        ```powershell
        $subId = $(az account show --query id --output tsv)
        $rgName = "rg-agent-workshop"
        $aiAccount = "<ai_account_name>" # 실제 AI 계정 이름으로 교체
        $aiProject = "<ai_project_name>" # 실제 AI 프로젝트 이름으로 교체
        $bingConnectionId = "/subscriptions/$subId/resourceGroups/$rgName/providers/Microsoft.CognitiveServices/accounts/$aiAccount/projects/$aiProject/connections/groundingwithbingsearch"
        dotnet user-secrets set "Azure:BingConnectionId" "$bingConnectionId"
        ```

    ## 프로젝트 구조

    워크숍 전반에 걸쳐 작업할 주요 **하위 폴더**와 **파일**을 숙지하세요.

    ### 워크숍 폴더

    - **Lab1.cs, Lab2.cs, Lab3.cs** 파일: 각 랩의 진입점으로 에이전트 로직을 포함합니다.
    - **Program.cs** 파일: 메인 로직을 포함하는 앱의 진입점입니다.
    - **SalesData.cs** 파일: SQLite 데이터베이스에 대한 동적 SQL 쿼리를 실행하는 함수 로직입니다.

    ### shared 폴더

    - **files** 폴더: 에이전트 앱이 생성한 파일을 포함합니다.
    - **fonts** 폴더: Code Interpreter가 사용하는 다국어 폰트를 포함합니다.
    - **instructions** 폴더: LLM에 전달되는 지시사항을 포함합니다.

    ![랩 폴더 구조](../media/project-structure-self-guided-csharp.png)

## 프로 팁

!!! tips
    1. 랩 환경의 오른쪽 패널에 있는 **Burger Menu**는 **Split Window View**와 랩을 종료하는 옵션을 포함한 추가 기능을 제공합니다. **Split Window View**를 사용하면 랩 환경을 전체 화면으로 최대화하여 화면 공간을 최적화할 수 있습니다. 랩의 **Instructions**와 **Resources** 패널이 별도의 창에서 열립니다.
    2. 랩 환경에서 랩 지침이 스크롤하기 어려우면 지침의 URL을 복사하여 **컴퓨터의 로컬 브라우저**에서 열어 더 원활한 경험을 할 수 있습니다.
    3. 이미지를 보는 데 문제가 있으면 **이미지를 클릭하여 확대**하면 됩니다.

*GitHub Copilot을 사용하여 번역됨.*
