## 학습 내용

이 랩에서는 다음을 수행합니다:

- DevTunnel을 사용하여 로컬 MCP 서버를 클라우드 기반 에이전트 서비스에서 접근 가능하게 만들기
- Model Context Protocol을 사용한 실습 실험을 위한 환경 설정

## 소개

Model Context Protocol (MCP) 서버는 대형 언어 모델(LLM)과 외부 도구 및 데이터 소스 간의 통신을 처리하는 중요한 구성 요소입니다. MCP 서버를 로컬 머신에서 실행하지만 Azure AI Foundry 에이전트 서비스는 연결하기 위해 인터넷 액세스가 필요합니다. 로컬 MCP 서버를 인터넷에서 접근 가능하게 만들기 위해 DevTunnel을 사용합니다. 이를 통해 에이전트 서비스가 MCP 서버가 Azure에서 서비스로 실행되는 것처럼 통신할 수 있습니다.

## MCP의 인터페이스 옵션

MCP는 LLM을 도구와 연결하기 위한 두 가지 주요 인터페이스를 지원합니다:

- **Streamable HTTP Transport**: 웹 기반 API 및 서비스용
- **Stdio Transport**: 로컬 스크립트 및 명령줄 도구용

이 랩에서는 Streamable HTTP transport 인터페이스를 사용하여 Azure AI Foundry 에이전트 서비스와 통합합니다.

!!! note
    일반적으로는 프로덕션 환경에서 MCP 서버를 배포하지만, 이 워크샵에서는 개발 환경에서 로컬로 실행합니다. 이를 통해 전체 배포 없이 MCP 도구를 테스트하고 상호작용할 수 있습니다.

### MCP 서버용 DevTunnel 시작하기

1. 새 터미널에서 DevTunnel을 인증합니다. Azure 계정으로 로그인하라는 메시지가 표시되며, Azure AI Foundry 에이전트 서비스나 Azure Portal에 로그인할 때 사용한 계정과 동일한 계정을 사용하세요. 다음 명령을 실행합니다:

    ```bash
    devtunnel login
    ```

1. 다음으로, MCP 서버가 실행 중인 터미널에서 다음을 실행하여 DevTunnel을 시작합니다:

    ```bash
    devtunnel host -p 8000 --allow-anonymous
    ```

    이는 에이전트가 MCP 서버에 연결하는 데 필요한 URL을 출력합니다. 출력은 다음과 유사합니다:

    ```text
    Hosting port: 8000
    Connect via browser: https://<tunnel-id>-8000.aue.devtunnels.ms
    Inspect network activity: https://<tunnel-id>-8000-inspect.aue.devtunnels.ms
    ```

## DevTunnel 환경 변수 업데이트

1. **Connect via browser** URL을 클립보드에 복사합니다 - 다음 랩에서 에이전트를 구성할 때 필요합니다.
2. 워크샵 폴더의 `.env` 파일을 엽니다.
3. 복사한 URL로 `DEV_TUNNEL_URL` 변수를 업데이트합니다.

    ```text
    DEV_TUNNEL_URL=https://<tunnel-id>-8000.aue.devtunnels.ms
    ```

## 에이전트 앱 시작

1. 아래 텍스트를 클립보드에 복사합니다:

    ```text
    Debug: Select and Start Debugging
    ```

2. <kbd>F1</kbd>을 눌러 VS Code 명령 팔레트를 엽니다.
3. 텍스트를 명령 팔레트에 붙여넣고 **Debug: Select and Start Debugging**을 선택합니다.
4. 목록에서 **🌎🤖Debug Compound: Agent and MCP (http)**를 선택합니다. 이는 에이전트 앱과 웹 채팅 클라이언트를 시작합니다.

## 에이전트와 대화 시작

브라우저의 **Web Chat** 탭으로 전환합니다. 에이전트 앱이 실행되고 질문을 받을 준비가 된 것을 볼 수 있습니다.

### DevTunnel로 디버깅

DevTunnel을 사용하여 MCP 서버와 에이전트 앱을 디버깅할 수 있습니다. 이를 통해 네트워크 활동을 검사하고 실시간으로 문제를 해결할 수 있습니다.

1. DevTunnel 출력에서 **Inspect network activity** URL을 선택합니다.
2. 이는 MCP 서버와 에이전트 앱의 네트워크 활동을 볼 수 있는 새 탭을 브라우저에서 엽니다.
3. 이를 사용하여 워크샵 중에 발생하는 문제를 디버깅할 수 있습니다.

또한 특정 문제를 디버깅하기 위해 MCP 서버 코드와 에이전트 앱 코드에 중단점을 설정할 수 있습니다. 이를 위해:

1. `mcp_server` 폴더의 `sales_analysis.py` 파일을 엽니다.
2. 실행을 일시 중지하고 싶은 줄 번호 옆의 거터를 클릭하여 중단점을 설정합니다.
3. 실행이 중단점에 도달하면 디버그 콘솔에서 변수를 검사하고, 코드를 단계별로 실행하고, 표현식을 평가할 수 있습니다.

*Translated using GitHub Copilot.*
