이 워크샵 애플리케이션은 교육 및 적응을 위해 설계되었으며, 바로 프로덕션 사용을 위한 것이 아닙니다. 그럼에도 불구하고 보안을 위한 몇 가지 모범 사례를 보여줍니다.

## 악성 SQL 공격

LLM 생성 SQL의 일반적인 우려사항은 인젝션이나 유해한 쿼리의 위험입니다. 이러한 위험은 데이터베이스 권한을 제한함으로써 완화됩니다.

이 앱은 에이전트에 대해 제한된 권한을 가진 PostgreSQL을 사용하며 보안 환경에서 실행됩니다. Row-Level Security (RLS)는 에이전트가 할당된 매장의 데이터에만 액세스하도록 보장합니다.

엔터프라이즈 환경에서는 일반적으로 데이터가 간소화된 스키마를 가진 읽기 전용 데이터베이스나 웨어하우스로 추출됩니다. 이는 에이전트에 대한 안전하고 성능이 뛰어나며 읽기 전용 액세스를 보장합니다.

## 샌드박싱

이는 [Azure AI 에이전트 서비스 코드 인터프리터](https://learn.microsoft.com/azure/ai-services/agents/how-to/tools/code-interpreter?view=azure-python-preview&tabs=python&pivots=overview){:target="_blank"}를 사용하여 요청 시 코드를 생성하고 실행합니다. 코드는 에이전트의 범위를 벗어나는 작업을 수행하지 못하도록 샌드박스 실행 환경에서 실행됩니다.

*Translated using GitHub Copilot.*
