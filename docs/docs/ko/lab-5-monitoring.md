## 소개

모니터링은 Azure AI Foundry 에이전트 서비스를 사용 가능하고, 성능이 좋으며, 신뢰할 수 있게 유지합니다. Azure Monitor는 메트릭과 로그를 수집하고, 실시간 인사이트를 제공하며, 경고를 보냅니다. 대시보드와 사용자 정의 경고를 사용하여 주요 메트릭을 추적하고, 트렌드를 분석하며, 사전에 대응하세요. Azure 포털, CLI, REST API 또는 클라이언트 라이브러리를 통해 모니터링에 액세스하세요.

## 랩 실습

1. VS Code 파일 탐색기에서 `workshop` 폴더의 `resources.txt` 파일을 엽니다.
1. `AI Project Name` 키의 값을 클립보드에 **복사**합니다.
1. [Azure AI Foundry 포털](https://ai.azure.com){:target="_blank"} 페이지로 이동합니다.
1. foundry 프로젝트 목록에서 프로젝트를 선택합니다.

## 모니터링 대시보드 열기

1. `resources.txt`에서 `Application Insights Name`의 값을 클립보드에 복사합니다.
1. AI Foundry 포털로 돌아가서 왼쪽 메뉴의 **Monitoring** 섹션을 선택합니다.
1. 복사한 `Application Insights Name`을 `Application Insights resource name` 드롭다운 목록에 붙여넣습니다.
1. 드롭다운 목록에서 **Application Insights** 리소스를 선택합니다.
1. **Connect**를 선택합니다.

### 모니터링 대시보드 탐색

`Application analytics` 대시보드에서 사용 가능한 정보를 익히세요.

!!!tip "모니터링 도구에 표시되는 데이터를 필터링하기 위해 날짜 범위를 선택할 수 있습니다."

![이미지는 애플리케이션 모니터링 대시보드를 보여줍니다](../media/monitor_usage.png)

### 리소스 사용량 모니터링

더 깊이 파고들어 `Resource Usage`를 선택하여 AI 프로젝트의 리소스 소비에 대한 상세한 메트릭을 볼 수 있습니다. 마찬가지로 시간 범위별로 데이터를 필터링할 수 있습니다.

*GitHub Copilot을 사용하여 번역됨.*
