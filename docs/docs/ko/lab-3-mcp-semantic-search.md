## 학습 내용

이 랩에서는 Model Context Protocol (MCP)과 PostgreSQL 데이터베이스를 사용하여 Azure AI 에이전트에서 시맨틱 검색 기능을 활성화합니다.

## 소개

이 랩은 Model Context Protocol (MCP)과 PostgreSQL을 사용하여 시맨틱 검색으로 Azure AI 에이전트를 업그레이드합니다. 제품명과 설명이 OpenAI 임베딩 모델(text-embedding-3-small)로 벡터로 변환되어 데이터베이스에 저장되었습니다. 이를 통해 에이전트가 사용자 의도를 이해하고 더 정확한 응답을 제공할 수 있습니다.

## 랩 실습

이전 랩에서는 에이전트에게 판매 데이터에 대한 질문을 할 수 있었지만 정확한 일치에만 제한되었습니다. 이 랩에서는 Model Context Protocol (MCP)을 사용하여 시맨틱 검색을 구현함으로써 에이전트의 기능을 확장합니다. 이를 통해 에이전트가 정확히 일치하지 않는 쿼리를 이해하고 응답할 수 있게 되어 더 복잡한 질문으로 사용자를 도와주는 능력이 향상됩니다.

1. 브라우저의 웹 채팅 탭에 다음 질문을 붙여넣습니다:

    ```text
    18A 차단기로 다른 매장들은 어떤 성과를 보였나요?
    ```

    에이전트가 응답합니다: "저희 기록에서 18A 차단기에 대한 판매 데이터를 찾을 수 없습니다. 😱 하지만 탐색할 만한 유사한 제품에 대한 몇 가지 제안이 있습니다." 이는 에이전트가 키워드로 쿼리를 매칭하는 것에만 의존하고 질문의 시맨틱 의미를 이해하지 못하기 때문입니다. 그래도 LLM은 이미 가지고 있는 제품 컨텍스트에서 교육받은 제품 제안을 할 수 있습니다.

## 시맨틱 검색 구현

이 섹션에서는 Model Context Protocol (MCP)을 사용하여 시맨틱 검색을 구현하여 에이전트의 기능을 향상시킵니다.

1. <kbd>F1</kbd>을 눌러 VS Code 명령 팔레트를 **엽니다**.
2. **Open File**을 입력하고 **File: Open File...**을 선택합니다.
3. 다음 경로를 파일 선택기에 **붙여넣고** <kbd>Enter</kbd>를 누릅니다:

    ```text
    /workspace/src/python/mcp_server/sales_analysis/sales_analysis.py
    ```

4. 약 100줄 아래로 스크롤하여 `semantic_search_products` 메서드를 찾습니다. 이 메서드는 판매 데이터에서 시맨틱 검색을 수행하는 역할을 합니다. **@mcp.tool()** 데코레이터가 주석 처리되어 있는 것을 확인할 수 있습니다. 이 데코레이터는 메서드를 MCP 도구로 등록하여 에이전트가 호출할 수 있도록 하는 데 사용됩니다.

5. 줄 시작 부분의 `#`을 제거하여 `@mcp.tool()` 데코레이터의 주석을 해제합니다. 이는 시맨틱 검색 도구를 활성화합니다.

    ```python
    # @mcp.tool()
    async def semantic_search_products(
        ctx: Context,
        query_description: Annotated[str, Field(
        ...
    ```

6. 다음으로 에이전트 지침이 시맨틱 검색 도구를 사용하도록 활성화해야 합니다. `app.py` 파일로 다시 전환합니다.
7. 약 30줄 아래로 스크롤하여 `# INSTRUCTIONS_FILE = "instructions/mcp_server_tools_with_semantic_search.txt"` 줄을 찾습니다.
8. 시작 부분의 `#`을 제거하여 줄의 주석을 해제합니다. 이는 에이전트가 시맨틱 검색 도구를 사용할 수 있게 합니다.

    ```python
    INSTRUCTIONS_FILE = "instructions/mcp_server_tools_with_semantic_search.txt"
    ```

## 에이전트 지침 검토

1. <kbd>F1</kbd>을 눌러 VS Code 명령 팔레트를 엽니다.
2. **Open File**을 입력하고 **File: Open File...**을 선택합니다.
3. 다음 경로를 파일 선택기에 붙여넣고 <kbd>Enter</kbd>를 누릅니다:

    ```text
    /workspace/src/shared/instructions/mcp_server_tools_with_semantic_search.txt
    ```

4. 파일의 지침을 검토합니다. 이 지침들은 에이전트가 시맨틱 검색 도구를 사용하여 판매 데이터에 대한 질문에 답하도록 지시합니다.

## 시맨틱 검색 도구로 에이전트 앱 시작

1. <kbd>Shift + F5</kbd>를 눌러 현재 에이전트 앱을 **중지**합니다.
2. <kbd>F5</kbd>를 눌러 에이전트 앱을 **재시작**합니다. 이는 업데이트된 지침과 시맨틱 검색 도구가 활성화된 상태로 에이전트를 시작합니다.
3. 브라우저의 **웹 채팅** 탭으로 다시 전환합니다.
4. 채팅에 다음 질문을 입력합니다:

    ```text
    18A 차단기로 다른 매장들은 어떤 성과를 보였나요?
    ```

    에이전트는 이제 질문의 시맨틱 의미를 이해하고 관련 판매 데이터로 적절히 응답합니다.

    !!! info "참고"
        MCP 시맨틱 검색 도구는 다음과 같이 작동합니다:

        1. 질문이 제품 설명과 동일한 OpenAI 임베딩 모델(text-embedding-3-small)을 사용하여 벡터로 변환됩니다.
        2. 이 벡터는 PostgreSQL 데이터베이스에서 유사한 제품 벡터를 검색하는 데 사용됩니다.
        3. 에이전트가 결과를 받아 응답을 생성하는 데 사용합니다.

*Translated using GitHub Copilot.*
