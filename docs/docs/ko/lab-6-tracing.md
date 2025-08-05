**TBC: 이 레이블은 사용자가 에이전트가 응답에서 사용하는 성가신 이모지를 제거하도록 에이전트 지침 파일을 업데이트하게 합니다.**

## 소개

추적은 실행 중 단계 순서, 입력, 출력을 보여줌으로써 에이전트의 동작을 이해하고 디버깅하는 데 도움이 됩니다. Azure AI Foundry에서 추적을 통해 에이전트가 요청을 처리하고, 도구를 호출하고, 응답을 생성하는 방법을 관찰할 수 있습니다. Azure AI Foundry 포털을 사용하거나 OpenTelemetry 및 Application Insights와 통합하여 추적 데이터를 수집하고 분석할 수 있어 에이전트를 문제 해결하고 최적화하기가 더 쉬워집니다.

<!-- ## 랩 실습

=== "Python"

      1. `app.py` 파일을 엽니다.
      2. 추적을 활성화하기 위해 `AZURE_TELEMETRY_ENABLED` 변수를 `True`로 변경합니다:

         ```python
         AZURE_TELEMETRY_ENABLED = True
         ```

        !!! info "참고"
            이 설정은 에이전트의 텔레메트리를 활성화합니다. `app.py`의 `initialize` 함수에서 텔레메트리 클라이언트가 Azure Monitor로 데이터를 보내도록 구성됩니다.

            ```python
             if AZURE_TELEMETRY_ENABLED:
                 configure_azure_monitor(connection_string=await self.project_client.telemetry.get_connection_string())
            ```         

=== "C#"

      tbd -->

## 에이전트 앱 실행

1. <kbd>F5</kbd>를 눌러 앱을 실행합니다.
2. **Preview in Editor**를 선택하여 새 편집기 탭에서 에이전트 앱을 엽니다.

### 에이전트와 대화 시작

에이전트 앱에 다음 프롬프트를 복사하여 붙여넣고 대화를 시작합니다:

```plaintext
상위 5개 제품 카테고리를 분석하고 온라인 스토어의 성과를 물리적 매장의 평균과 비교하는 경영진 보고서를 작성하세요.
```

## 추적 보기

Azure AI Foundry 포털이나 OpenTelemetry를 사용하여 에이전트 실행의 추적을 볼 수 있습니다. 추적은 에이전트 실행 중 단계 순서, 도구 호출, 데이터 교환을 보여줍니다. 이 정보는 에이전트의 성능을 디버깅하고 최적화하는 데 중요합니다.

### Azure AI Foundry 포털 사용

Azure AI Foundry 포털에서 추적을 보려면 다음 단계를 따르세요:

1. **[Azure AI Foundry](https://ai.azure.com/)** 포털로 이동합니다.
2. 프로젝트를 선택합니다.
3. 왼쪽 메뉴에서 **Tracing** 탭을 선택합니다.
4. 여기서 에이전트가 생성한 추적을 볼 수 있습니다.

   ![](media/ai-foundry-tracing.png)

### 추적 자세히 살펴보기

1. 추적이 나타나는 데 몇 분이 걸릴 수 있으므로 최신 추적을 보려면 **Refresh** 버튼을 클릭해야 할 수 있습니다.
2. `Zava Agent Initialization`이라는 추적을 선택하여 세부 정보를 봅니다.
   ![](media/ai-foundry-trace-agent-init.png)
3. `creare_agent Zava DIY Sales Agent` 추적을 선택하여 에이전트 생성 프로세스의 세부 정보를 봅니다. `Input & outputs` 섹션에서 에이전트 지침을 볼 수 있습니다.
4. 다음으로 `Zava Agent Chat Request: Write an executive...` 추적을 선택하여 채팅 요청의 세부 정보를 봅니다. `Input & outputs` 섹션에서 사용자 입력과 에이전트의 응답을 볼 수 있습니다.

<!-- https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/continuous-evaluation-agents -->

*Translated using GitHub Copilot.*
