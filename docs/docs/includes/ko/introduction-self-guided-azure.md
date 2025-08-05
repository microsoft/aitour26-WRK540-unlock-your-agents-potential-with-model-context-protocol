## Codespace 빌드 완료까지 대기

진행하기 전에 Codespace 또는 Dev Container가 완전히 빌드되어 준비되었는지 확인하세요. 인터넷 연결과 다운로드되는 리소스에 따라 몇 분이 걸릴 수 있습니다.

## Azure로 인증

에이전트 앱이 Azure AI 에이전트 서비스와 모델에 액세스할 수 있도록 Azure로 인증합니다. 다음 단계를 따르세요:

1. 워크샵 환경이 준비되고 VS Code에서 열려 있는지 확인합니다.
2. VS Code에서 **Terminal** > **New Terminal**을 통해 터미널을 열고 다음을 실행합니다:

    ```shell
    az login --use-device-code
    ```

    !!! note
        브라우저를 열고 Azure에 로그인하라는 메시지가 표시됩니다. 인증 코드를 복사하고:

        1. 계정 유형을 선택하고 **Next**를 클릭합니다.
        2. Azure 자격 증명으로 로그인합니다.
        3. 코드를 붙여넣습니다.
        4. **OK**를 클릭한 다음 **Done**을 클릭합니다.

    !!! warning
        여러 Azure 테넌트가 있는 경우 다음을 사용하여 올바른 테넌트를 지정하세요:

        ```shell
        az login --use-device-code --tenant <tenant_id>
        ```

3. 다음으로 명령줄에서 적절한 구독을 선택합니다.
4. 다음 단계를 위해 터미널 창을 열어둡니다.

## Azure 리소스 배포

이 배포는 **rg-zava-agent-wks-nnnn** 리소스 그룹 하에 Azure 구독에 다음 리소스를 생성합니다:

- **fdy-zava-agent-wks-nnnn**이라는 **Azure AI Foundry 허브**
- **prj-zava-agent-wks-nnnn**이라는 **Azure AI Foundry 프로젝트**
- 두 개의 모델이 배포됩니다: **gpt-4o-mini** 및 **text-embedding-3-small**. [가격 참조.](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/){:target="_blank"}

!!! warning "에이전트가 빈번한 모델 호출을 하므로 gpt-4o-mini Global Standard SKU에 대해 최소 120K TPM 할당량이 있는지 확인하세요. [AI Foundry 관리 센터](https://ai.azure.com/managementCenter/quota){:target="_blank"}에서 할당량을 확인하세요."

워크샵에 필요한 리소스 배포를 자동화하는 bash 스크립트를 제공했습니다.

### 자동화된 배포

`deploy.sh` 스크립트는 기본적으로 `westus` 지역에 리소스를 배포합니다. 스크립트를 실행하려면:

```bash
cd infra && ./deploy.sh
```

<!-- !!! note "Windows에서는 `deploy.sh` 대신 `deploy.ps1`을 실행하세요" -->

### 워크샵 구성

=== "Python"

    #### Azure 리소스 구성

    배포 스크립트는 프로젝트 및 모델 엔드포인트, 모델 배포 이름, Application Insights 연결 문자열이 포함된 **.env** 파일을 생성합니다. .env 파일은 자동으로 `src/python/workshop` 폴더에 저장됩니다.
    
    **.env** 파일은 다음과 유사하며 사용자의 값으로 업데이트됩니다:

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

    다음과 유사하게 보일 것입니다:

    ```plaintext
    Azure AI Foundry Resources:
    - Resource Group Name: rg-zava-agent-wks-nnnn
    - AI Project Name: prj-zava-agent-wks-nnnn
    - Foundry Resource Name: fdy-zava-agent-wks-nnnn
    - Application Insights Name: appi-zava-agent-wks-nnnn
    ```


=== "C#"

    스크립트는 [ASP.NET Core 개발 비밀](https://learn.microsoft.com/aspnet/core/security/app-secrets){:target="_blank"}의 Secret Manager를 사용하여 프로젝트 변수를 안전하게 저장합니다.

    VS Code에서 C# 워크스페이스를 연 후 다음 명령을 실행하여 비밀을 볼 수 있습니다:

    ```bash
    dotnet user-secrets list
    ```

*Translated using GitHub Copilot.*
