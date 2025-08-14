## 학습할 내용

이 랩에서는 모델 컨텍스트 프로토콜(MCP)과 [PostgreSQL Vector](https://github.com/pgvector/pgvector){:target="_blank"} 확장이 활성화된 PostgreSQL 데이터베이스를 사용하여 Azure AI 에이전트에서 의미 검색 기능을 활성화합니다.

## 소개

이 랩은 모델 컨텍스트 프로토콜(MCP)과 PostgreSQL을 사용하여 의미 검색으로 Azure AI 에이전트를 업그레이드합니다. 제품명과 설명이 OpenAI 임베딩 모델(text-embedding-3-small)로 벡터로 변환되어 데이터베이스에 저장되었습니다. 이를 통해 에이전트가 사용자 의도를 이해하고 더 정확한 응답을 제공할 수 있습니다.

## 랩 실습

이전 랩에서는 에이전트에게 판매 데이터에 대해 질문할 수 있었지만 정확한 일치로 제한되었습니다. 이 랩에서는 모델 컨텍스트 프로토콜(MCP)을 사용하여 의미 검색을 구현함으로써 에이전트의 기능을 확장합니다. 이를 통해 에이전트가 정확히 일치하지 않는 쿼리를 이해하고 응답할 수 있게 되어 더 복잡한 질문으로 사용자를 지원하는 능력이 향상됩니다.

1. 브라우저의 웹 채팅 탭에 다음 질문을 붙여넣습니다:

    ```text
    What 18 amp circuit breakers do we sell?
    ```

    에이전트가 다음과 같은 메시지로 응답합니다: "재고에서 특정 18암페어 차단기를 찾을 수 없습니다. 하지만 다른 유형의 차단기가 있을 수 있습니다. 일반 차단기나 기타 관련 제품을 검색해드릴까요? 😊"

## 에이전트 앱 중지

VS Code에서 <kbd>Shift + F5</kbd>를 눌러 에이전트 앱을 중지합니다.

## 의미 검색 구현

이 섹션에서는 모델 컨텍스트 프로토콜(MCP)을 사용하여 의미 검색을 구현하여 에이전트의 기능을 향상시킵니다.

1. <kbd>F1</kbd>을 눌러 VS Code 명령 팔레트를 **엽니다**.
2. **Open File**을 입력하고 **File: Open File...**를 선택합니다.
3. 파일 선택기에 다음 경로를 **붙여넣고** <kbd>Enter</kbd>를 누릅니다:

    ```text
    /workspace/src/python/mcp_server/sales_analysis/sales_analysis.py
    ```

4. 100번째 줄 주변으로 스크롤하여 `semantic_search_products` 메서드를 찾습니다. 이 메서드는 판매 데이터에서 의미 검색을 수행하는 역할을 합니다. **@mcp.tool()** 데코레이터가 주석 처리된 것을 확인할 수 있습니다. 이 데코레이터는 메서드를 MCP 도구로 등록하여 에이전트가 호출할 수 있게 하는 데 사용됩니다.

5. 줄 시작 부분의 `#`을 제거하여 `@mcp.tool()` 데코레이터의 주석을 해제합니다. 이렇게 하면 의미 검색 도구가 활성화됩니다.

    ```python
    # @mcp.tool()
    async def semantic_search_products(
        ctx: Context,
        query_description: Annotated[str, Field(
        ...
    ```

6. 다음으로, 의미 검색 도구를 사용하도록 에이전트 지침을 활성화해야 합니다. `app.py` 파일로 다시 전환합니다.
7. 30번째 줄 주변으로 스크롤하여 `# INSTRUCTIONS_FILE = "instructions/mcp_server_tools_with_semantic_search.txt"` 줄을 찾습니다.
8. 시작 부분의 `#`을 제거하여 줄의 주석을 해제합니다. 이렇게 하면 에이전트가 의미 검색 도구를 사용할 수 있게 됩니다.

    ```python
    INSTRUCTIONS_FILE = "instructions/mcp_server_tools_with_semantic_search.txt"
    ```

## 에이전트 지침 검토

1. <kbd>F1</kbd>을 눌러 VS Code 명령 팔레트를 엽니다.
2. **Open File**을 입력하고 **File: Open File...**를 선택합니다.
3. 파일 선택기에 다음 경로를 붙여넣고 <kbd>Enter</kbd>를 누릅니다:

    ```text
    /workspace/src/shared/instructions/mcp_server_tools_with_semantic_search.txt
    ```

4. 파일의 지침을 검토합니다. 이 지침은 에이전트가 의미 검색 도구를 사용하여 판매 데이터에 대한 질문에 답변하도록 지시합니다.

## 의미 검색 도구로 에이전트 앱 시작

1. <kbd>F5</kbd>를 눌러 에이전트 앱을 **시작**합니다. 이렇게 하면 업데이트된 지침과 의미 검색 도구가 활성화된 상태로 에이전트가 시작됩니다.
2. 브라우저의 **웹 채팅** 탭으로 다시 전환합니다.
3. 채팅에 다음 질문을 입력합니다:

    ```text
    What 18 amp circuit breakers do we sell?
    ```

    이제 에이전트가 질문의 의미를 이해하고 관련 판매 데이터로 적절히 응답합니다.

    !!! info "참고"
        MCP 의미 검색 도구는 다음과 같이 작동합니다:

        1. 질문이 제품 설명과 동일한 OpenAI 임베딩 모델(text-embedding-3-small)을 사용하여 벡터로 변환됩니다.
        2. 이 벡터를 사용하여 PostgreSQL 데이터베이스에서 유사한 제품 벡터를 검색합니다.
        3. 에이전트가 결과를 받아 응답을 생성하는 데 사용합니다.

## 경영진 보고서 작성

이 워크샵의 마지막 프롬프트는 다음과 같습니다:

```plaintext
Write an executive report on the sales performance of different stores for these circuit breakers.
```

## 에이전트 앱 실행 유지

다음 랩에서 더 많은 도구와 기능으로 에이전트를 확장하는 데 사용할 것이므로 에이전트 앱을 실행 상태로 유지하세요.

*GitHub Copilot을 사용하여 번역되었습니다.*
