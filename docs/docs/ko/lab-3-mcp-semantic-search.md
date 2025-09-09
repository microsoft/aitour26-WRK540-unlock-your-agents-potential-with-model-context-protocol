## 학습할 내용

이 랩에서는 MCP 서버와 [PostgreSQL Vector](https://github.com/pgvector/pgvector){:target="\_blank"} 확장이 활성화된 PostgreSQL 데이터베이스를 사용하여 Azure AI 에이전트에서 시맨틱 검색 기능을 활성화합니다.

## 소개

이 랩은 MCP 서버와 PostgreSQL을 사용하여 시맨틱 검색으로 Azure AI 에이전트를 업그레이드합니다.

Zava의 모든 제품 이름과 설명은 OpenAI 임베딩 모델(text-embedding-3-small)로 벡터로 변환되어 데이터베이스에 저장되었습니다. 이를 통해 에이전트는 사용자 의도를 이해하고 더 정확한 응답을 제공할 수 있습니다.

??? info "개발자용: PostgreSQL 시맨틱 검색은 어떻게 작동하나요?"

    ### 제품 설명 및 이름 벡터화

    Zava 제품 이름과 설명이 어떻게 벡터화되었는지 자세히 알아보려면 [Zava DIY PostgreSQL 데이터베이스 생성기 README](https://github.com/microsoft/aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol/tree/main/data/database){:target="_blank"}를 참조하세요.

    === "Python"

        ### LLM이 MCP 서버 도구 호출

        사용자의 쿼리와 제공된 지침을 바탕으로 LLM은 관련 제품을 찾기 위해 MCP 서버 도구 `semantic_search_products`를 호출하기로 결정합니다.

        다음과 같은 일련의 이벤트가 발생합니다:

        1. MCP 도구 `semantic_search_products`가 사용자의 쿼리 설명과 함께 호출됩니다.
        1. MCP 서버는 OpenAI 임베딩 모델(text-embedding-3-small)을 사용하여 쿼리에 대한 벡터를 생성합니다. 쿼리를 벡터화하는 코드는 `generate_query_embedding` 메소드에 있습니다.
        1. 그런 다음 MCP 서버는 PostgreSQL 데이터베이스에 대해 시맨틱 검색을 수행하여 유사한 벡터를 가진 제품을 찾습니다.

        ### PostgreSQL 시맨틱 검색 개요

        `semantic_search_products` MCP 서버 도구는 벡터화된 쿼리를 사용하여 데이터베이스에서 가장 유사한 제품 벡터를 찾는 SQL 쿼리를 실행합니다. SQL 쿼리는 pgvector 확장에서 제공하는 `<->` 연산자를 사용하여 벡터 간의 거리를 계산합니다.

        ```python
        async def search_products_by_similarity(
            self, query_embedding: list[float], 
                rls_user_id: str, 
                max_rows: int = 20, 
                similarity_threshold: float = 30.0
        ) -> str:
                ...
                query = f"""
                    SELECT 
                        p.*,
                        (pde.description_embedding <=> $1::vector) as similarity_distance
                    FROM {SCHEMA_NAME}.product_description_embeddings pde
                    JOIN {SCHEMA_NAME}.products p ON pde.product_id = p.product_id
                    WHERE (pde.description_embedding <=> $1::vector) <= $3
                    ORDER BY similarity_distance
                    LIMIT $2
                """

                rows = await conn.fetch(query, embedding_str, max_rows, distance_threshold)
                ...
        ```

    === "C#"

        ### LLM이 MCP 서버 도구 호출

        사용자의 쿼리와 제공된 지침을 바탕으로 LLM은 관련 제품을 찾기 위해 MCP 서버 도구 `semantic_search_products`를 호출하기로 결정합니다.

        다음과 같은 일련의 이벤트가 발생합니다:

        1. MCP 도구 `semantic_search_products`가 사용자의 쿼리 설명과 함께 호출됩니다.
        2. MCP 서버는 OpenAI 임베딩 모델(text-embedding-3-small)을 사용하여 쿼리에 대한 벡터를 생성합니다. `EmbeddingGeneratorExtensions.cs` 파일의 `GenerateVectorAsync` 메소드를 참조하세요.
        3. 그런 다음 MCP 서버는 PostgreSQL 데이터베이스에 대해 시맨틱 검색을 수행하여 유사한 벡터를 가진 제품을 찾습니다.

        ### PostgreSQL 시맨틱 검색 개요

        `semantic_search_products` MCP 서버 도구는 벡터화된 쿼리를 사용하여 데이터베이스에서 가장 유사한 제품 벡터를 찾는 SQL 쿼리를 실행합니다. SQL 쿼리는 pgvector 확장에서 제공하는 `<->` 연산자를 사용하여 벡터 간의 거리를 계산합니다.

        ```csharp
        public async Task<IEnumerable<SemanticSearchResult>> SemanticSearchProductsAsync(
        ...
            await using var searchCmd = new NpgsqlCommand("""
            SELECT 
                p.*,
                (pde.description_embedding <=> $1::vector) as similarity_distance
            FROM retail.product_description_embeddings pde
            JOIN retail.products p ON pde.product_id = p.product_id
            WHERE (pde.description_embedding <=> $1::vector) <= $3
            ORDER BY similarity_distance
            LIMIT $2
            """, connection);
            searchCmd.Parameters.AddWithValue(new Vector(embeddings));
            searchCmd.Parameters.AddWithValue(maxRows);
            searchCmd.Parameters.AddWithValue(distanceThreshold);

            await using var reader = await searchCmd.ExecuteReaderAsync();
            var results = new List<SemanticSearchResult>();
        ```

## 랩 실습

이전 랩에서는 에이전트에게 판매 데이터에 대한 질문을 할 수 있었지만 정확한 일치로 제한되었습니다. 이 랩에서는 MCP(Model Context Protocol)를 사용하여 시맨틱 검색을 구현함으로써 에이전트의 기능을 확장합니다. 이를 통해 에이전트는 정확히 일치하지 않는 쿼리를 이해하고 응답할 수 있어 더 복잡한 질문으로 사용자를 지원하는 능력이 향상됩니다.

1. 브라우저의 웹 채팅 탭에 다음 질문을 붙여넣으세요:

   ```text
   What 18 amp circuit breakers do we sell?
   ```

   에이전트는 다음과 비슷한 메시지로 응답합니다:

   _"재고에서 특정 18 amp 차단기를 찾을 수 없었습니다. 하지만 다른 유형의 차단기가 있을 수 있습니다. 일반적인 차단기나 기타 관련 제품을 검색해 드릴까요? 😊"_

## 에이전트 앱 중지

VS Code에서 <kbd>Shift + F5</kbd>를 눌러 에이전트 앱을 중지하세요.

=== "Python"

    ## 시맨틱 검색 구현

    이 섹션에서는 MCP(Model Context Protocol)를 사용하여 시맨틱 검색을 구현하여 에이전트의 기능을 향상시킵니다.

    1. <kbd>F1</kbd>을 눌러 VS Code 명령 팔레트를 **엽니다**.
    2. **Open File**을 입력하고 **File: Open File...**을 선택합니다.
    3. 파일 선택기에 다음 경로를 **붙여넣고** <kbd>Enter</kbd>를 누릅니다:

        ```text
        /workspace/src/python/mcp_server/sales_analysis/sales_analysis.py
        ```

    4. 70행 근처로 스크롤하여 `semantic_search_products` 메소드를 찾습니다. 이 메소드는 판매 데이터에서 시맨틱 검색을 수행하는 역할을 합니다. **@mcp.tool()** 데코레이터가 주석 처리되어 있는 것을 볼 수 있습니다. 이 데코레이터는 메소드를 MCP 도구로 등록하여 에이전트가 호출할 수 있도록 하는 데 사용됩니다.

    5. 줄 시작 부분의 `#`를 제거하여 `@mcp.tool()` 데코레이터의 주석을 해제합니다. 이렇게 하면 시맨틱 검색 도구가 활성화됩니다.

        ```python
        # @mcp.tool()
        async def semantic_search_products(
            ctx: Context,
            query_description: Annotated[str, Field(
            ...
        ```

    6. 다음으로, 시맨틱 검색 도구를 사용하도록 에이전트 지침을 활성화해야 합니다. `app.py` 파일로 다시 전환합니다.
    7. 30행 근처로 스크롤하여 `# INSTRUCTIONS_FILE = "instructions/mcp_server_tools_with_semantic_search.txt"` 줄을 찾습니다.
    8. 시작 부분의 `#`를 제거하여 줄의 주석을 해제합니다. 이렇게 하면 에이전트가 시맨틱 검색 도구를 사용할 수 있게 됩니다.

        ```python
        INSTRUCTIONS_FILE = "instructions/mcp_server_tools_with_semantic_search.txt"
        ```

=== "C#"

    ## 시맨틱 검색 구현

    이 섹션에서는 MCP(Model Context Protocol)를 사용하여 시맨틱 검색을 구현하여 에이전트의 기능을 향상시킵니다.

    1. `McpAgentWorkshop.WorkshopApi` 프로젝트에서 `McpHost.cs` 파일을 엽니다.
    1. 다른 MCP 도구들이 MCP 서버에 등록된 곳을 찾아 `SemanticSearchTools` 클래스를 MCP 도구로 등록합니다.

        ```csharp
        builder.Services.AddMcpTool<SemanticSearchTools>();
        ```

        !!! info "참고"
            MCP 서버가 검색을 어떻게 수행할지 알아보기 위해 `SemanticSearchTools`의 구현을 읽어보세요.

    1. 다음으로, 시맨틱 검색 도구를 사용하도록 에이전트 지침을 활성화해야 합니다. `AgentService` 클래스로 돌아가서 상수 `InstructionsFile`을 `mcp_server_tools_with_semantic_search.txt`로 변경합니다.

## 에이전트 지침 검토

1. <kbd>F1</kbd>을 눌러 VS Code 명령 팔레트를 엽니다.
2. **Open File**을 입력하고 **File: Open File...**을 선택합니다.
3. 파일 선택기에 다음 경로를 붙여넣고 <kbd>Enter</kbd>를 누릅니다:

   ```text
   /workspace/src/shared/instructions/mcp_server_tools_with_semantic_search.txt
   ```

4. 파일의 지침을 검토합니다. 이 지침들은 에이전트가 시맨틱 검색 도구를 사용하여 판매 데이터에 대한 질문에 답하도록 지시합니다.

## 시맨틱 검색 도구로 에이전트 앱 시작

1. <kbd>F5</kbd>를 눌러 에이전트 앱을 **시작**합니다. 이렇게 하면 업데이트된 지침과 시맨틱 검색 도구가 활성화된 상태로 에이전트가 시작됩니다.
2. 브라우저에서 **웹 채팅**을 엽니다.
3. 채팅에 다음 질문을 입력합니다:

    ```text
    What 18 amp circuit breakers do we sell?
    ```

    이제 에이전트는 질문의 시맨틱 의미를 이해하고 관련 판매 데이터로 적절히 응답합니다.

    !!! info "참고"
        MCP 시맨틱 검색 도구는 다음과 같이 작동합니다:

        1. 질문은 제품 설명과 동일한 OpenAI 임베딩 모델(text-embedding-3-small)을 사용하여 벡터로 변환됩니다.
        2. 이 벡터는 PostgreSQL 데이터베이스에서 유사한 제품 벡터를 검색하는 데 사용됩니다.
        3. 에이전트는 결과를 받아 응답을 생성하는 데 사용합니다.

## 임원 보고서 작성

이 워크샵의 마지막 프롬프트는 다음과 같습니다:

```plaintext
이 차단기들에 대한 다양한 매장의 판매 성과에 대한 임원 보고서를 작성하세요.
```

## 에이전트 앱 실행 상태 유지

다음 랩에서 안전한 에이전트 데이터 액세스를 탐색하는 데 사용할 것이므로 에이전트 앱을 실행 상태로 유지하세요.

*GitHub Copilot을 사용하여 번역됨.*
