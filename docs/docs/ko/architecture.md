## 솔루션 아키텍처

이 워크샵에서는 Zava 판매 에이전트를 만들게 됩니다. 이는 판매 데이터에 대한 질문에 답하고 Zava의 소매 DIY 비즈니스를 위한 차트를 생성하도록 설계된 대화형 에이전트입니다.

## 에이전트 앱의 구성 요소

1. **Microsoft Azure 서비스**

    이 에이전트는 Microsoft Azure 서비스를 기반으로 구축되었습니다.

      - **생성형 AI 모델**: 이 앱을 구동하는 기반 LLM은 [Azure OpenAI gpt-4o-mini](https://learn.microsoft.com/azure/ai-foundry/openai/concepts/models?tabs=global-standard%2Cstandard-chat-completions#how-do-i-access-the-gpt-4o-and-gpt-4o-mini-models){:target="_blank"} LLM입니다.

      - **제어 플레인**: 앱과 그 아키텍처 구성 요소는 브라우저를 통해 액세스할 수 있는 [Azure AI Foundry](https://ai.azure.com){:target="_blank"} 포털을 사용하여 관리 및 모니터링됩니다.

2. **Azure AI Foundry (SDK)**

    워크샵은 Azure AI Foundry SDK를 사용하여 [Python](https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme?view=azure-python-preview&context=%2Fazure%2Fai-services%2Fagents%2Fcontext%2Fcontext){:target="_blank"}으로 제공됩니다. SDK는 [코드 인터프리터](https://learn.microsoft.com/azure/ai-services/agents/how-to/tools/code-interpreter?view=azure-python-preview&tabs=python&pivots=overview){:target="_blank"} 및 [Model Context Protocol (MCP)](https://modelcontextprotocol.io/){:target="_blank"} 통합을 포함한 Azure AI 에이전트 서비스의 주요 기능을 지원합니다.

3. **데이터베이스**

    앱은 Zava 판매 데이터베이스로 구동되며, 이는 Zava의 소매 DIY 운영에 대한 포괄적인 판매 데이터를 포함한 pgvector 확장이 있는 [Azure Database for PostgreSQL flexible server](https://www.postgresql.org/){:target="_blank"}입니다.

    데이터베이스는 판매, 재고, 고객 데이터에 대한 복잡한 쿼리를 지원합니다. Row-Level Security (RLS)는 에이전트가 할당된 매장에만 액세스하도록 보장합니다.

4. **MCP 서버**

    Model Context Protocol (MCP) 서버는 에이전트와 PostgreSQL 데이터베이스 간의 브리지 역할을 하는 사용자 정의 Python 서비스입니다. 다음을 처리합니다:

     - **데이터베이스 스키마 검색**: 자동으로 데이터베이스 스키마를 검색하여 에이전트가 사용 가능한 데이터를 이해할 수 있도록 도와줍니다.
     - **쿼리 생성**: 자연어 요청을 SQL 쿼리로 변환합니다.
     - **도구 실행**: SQL 쿼리를 실행하고 에이전트가 사용할 수 있는 형식으로 결과를 반환합니다.
     - **시간 서비스**: 시간에 민감한 보고서 생성을 위한 시간 관련 데이터를 제공합니다.

## 워크샵 솔루션 확장

워크샵은 데이터베이스를 업데이트하고 Foundry 에이전트 서비스 지침을 사용자 정의하여 고객 지원과 같은 사용 사례에 쉽게 적용할 수 있습니다.

## 앱에서 시연된 모범 사례

앱은 또한 효율성과 사용자 경험을 위한 몇 가지 모범 사례를 보여줍니다.

- **비동기 API**:
  워크샵 샘플에서 Foundry 에이전트 서비스와 PostgreSQL은 모두 비동기 API를 사용하여 리소스 효율성과 확장성을 최적화합니다. 이 설계 선택은 FastAPI, ASP.NET 또는 Streamlit과 같은 비동기 웹 프레임워크로 애플리케이션을 배포할 때 특히 유리합니다.

- **토큰 스트리밍**:
  토큰 스트리밍은 LLM 기반 에이전트 앱의 인지된 응답 시간을 줄여 사용자 경험을 개선하기 위해 구현됩니다.

- **관찰 가능성**:
  앱에는 에이전트 성능, 사용 패턴, 지연 시간을 모니터링하기 위한 내장 [추적](https://learn.microsoft.com/azure/ai-foundry/agents/concepts/tracing){:target="_blank"} 및 [메트릭](https://learn.microsoft.com/azure/ai-foundry/agents/how-to/metrics){:target="_blank"}이 포함되어 있습니다. 이를 통해 문제를 식별하고 시간이 지남에 따라 에이전트를 최적화할 수 있습니다.

*Translated using GitHub Copilot.*
