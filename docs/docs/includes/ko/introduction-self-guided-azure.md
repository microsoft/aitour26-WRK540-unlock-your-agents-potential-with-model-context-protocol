!!! danger 
    계속하기 전에 Codespace 또는 Dev Container가 완전히 구축되고 준비되었는지 확인하세요.

## Azure 인증

에이전트 앱이 Azure AI 에이전트 서비스와 모델에 액세스할 수 있도록 Azure로 인증합니다. 다음 단계를 따르세요:

1. VS Code에서 <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>`</kbd>를 **눌러** 새 터미널 창을 엽니다. 그런 다음 다음 명령을 실행합니다:

    ```shell
    az login --use-device-code
    ```

    !!! warning
        여러 Azure 테넌트가 있는 경우 다음을 사용하여 올바른 테넌트를 지정하세요:

        ```shell
        az login --use-device-code --tenant <tenant_id>
        ```

2. 다음 단계를 따라 인증합니다:

    1. **인증 코드**를 클립보드에 **복사**합니다.
    2. <kbd>ctrl</kbd> 또는 <kbd>cmd</kbd> 키를 **누르고 유지**합니다.
    3. 인증 URL을 **선택**하여 브라우저에서 엽니다.
    4. 코드를 **붙여넣고** **다음**을 클릭합니다.
    5. **계정을 선택**하고 로그인합니다.
    6. **계속**을 선택합니다
    7. VS Code의 터미널 창으로 **돌아갑니다**.
    8. 메시지가 표시되면 구독을 **선택**합니다.

3. 다음 단계를 위해 터미널 창을 열어두세요.

## Azure 리소스 배포

이 배포는 Azure 구독에 다음 리소스를 생성합니다.

- **rg-zava-agent-wks-nnnn**이라는 리소스 그룹
- **fdy-zava-agent-wks-nnnn**이라는 **Azure AI Foundry 허브**
- **prj-zava-agent-wks-nnnn**이라는 **Azure AI Foundry 프로젝트**
- 두 개의 모델이 배포됩니다: **gpt-4o-mini**와 **text-embedding-3-small**. [가격 참조.](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/){:target="_blank"}

!!! warning "최소한 다음 모델 할당량이 있는지 확인하세요"
    - gpt-4o-mini Global Standard SKU에 대한 120K TPM 할당량(에이전트가 빈번한 모델 호출을 수행하므로).
    - text-embedding-3-small 모델 Global Standard SKU에 대한 50K TPM.
    - [AI Foundry 관리 센터](https://ai.azure.com/managementCenter/quota){:target="_blank"}에서 할당량을 확인하세요."

### 자동 배포

다음 bash 스크립트를 실행하여 워크샵에 필요한 리소스의 배포를 자동화합니다. `deploy.sh` 스크립트는 기본적으로 `westus` 지역에 리소스를 배포합니다. 스크립트를 실행하려면:

=== "Linux/Mac OS"

    ```bash
    cd infra && ./deploy.sh
    ```

=== "Windows"

    ```powershell
    cd infra && .\deploy.ps1
    ```
<!-- !!! note "Windows에서는 `deploy.sh` 대신 `deploy.ps1`을 실행하세요" -->

### 워크샵 구성

=== "Python"

    #### Azure 리소스 구성

    배포 스크립트는 프로젝트 및 모델 엔드포인트, 모델 배포 이름, Application Insights 연결 문자열이 포함된 **.env** 파일을 생성합니다. .env 파일은 `src/python/workshop` 폴더에 자동으로 저장됩니다. 
    
    **.env** 파일은 다음과 비슷하게 보이며 값이 업데이트됩니다:

    ```python
    PROJECT_ENDPOINT="<your_project_endpoint>"
    GPT_MODEL_DEPLOYMENT_NAME="<your_model_deployment_name>"
    EMBEDDING_MODEL_DEPLOYMENT_NAME="<your_embedding_model_deployment_name>"
    APPLICATIONINSIGHTS_CONNECTION_STRING="<your_application_insights_connection_string>"
    DEV_TUNNEL_URL="<your_dev_tunnel_url>"
    AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED="true"
    AZURE_OPENAI_ENDPOINT="<your_azure_openai_endpoint>"
    ```

    #### Azure 리소스 이름

    `workshop` 폴더에서 `resources.txt`라는 파일도 찾을 수 있습니다. 이 파일에는 배포 중에 생성된 Azure 리소스의 이름이 포함되어 있습니다. 

    다음과 유사하게 보입니다:

    ```plaintext
    Azure AI Foundry Resources:
    - Resource Group Name: rg-zava-agent-wks-nnnn
    - AI Project Name: prj-zava-agent-wks-nnnn
    - Foundry Resource Name: fdy-zava-agent-wks-nnnn
    - Application Insights Name: appi-zava-agent-wks-nnnn
    ```

=== "C#"

    스크립트는 [ASP.NET Core 개발 시크릿](https://learn.microsoft.com/aspnet/core/security/app-secrets){:target="_blank"}용 Secret Manager를 사용하여 프로젝트 변수를 안전하게 저장합니다.

    VS Code에서 C# 워크스페이스를 연 후 다음 명령을 실행하여 시크릿을 볼 수 있습니다:

    ```bash
    dotnet user-secrets list
    ```

*GitHub Copilot을 사용하여 번역되었습니다.*
