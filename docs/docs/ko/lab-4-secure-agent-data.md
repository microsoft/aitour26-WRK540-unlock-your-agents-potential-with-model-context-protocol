## 학습할 내용

이 랩에서는 MCP(Model Context Protocol)와 PostgreSQL 행 수준 보안(RLS)을 사용하여 에이전트 데이터를 보호합니다. 에이전트는 읽기 전용 데이터베이스 액세스를 가지며 데이터는 사용자 역할(본사 및 매장 관리자)에 의해 보호되어 승인된 사용자만 특정 정보에 액세스할 수 있도록 합니다.

## 소개

PostgreSQL 데이터베이스는 행 수준 보안(RLS)을 사용하여 사용자 역할별로 데이터 액세스를 제어합니다. 웹 채팅 클라이언트는 기본적으로 `본사` 역할(전체 데이터 액세스)로 설정되지만, `매장 관리자` 역할로 전환하면 역할별 데이터에만 액세스가 제한됩니다.

MCP 서버는 에이전트에게 Zava 데이터베이스에 대한 액세스를 제공합니다. 에이전트 서비스가 사용자 요청을 처리할 때, 사용자 역할(UUID)이 MCP Tools Resource Headers를 통해 MCP 서버로 전달되어 역할 기반 보안이 적용되도록 합니다.

정상적인 운영에서는 매장 관리자가 에이전트로 인증하고 사용자 역할이 그에 따라 설정됩니다. 하지만 이것은 워크샵이므로 역할을 수동으로 선택할 것입니다.

??? info "개발자용: PostgreSQL 행 수준 보안은 어떻게 작동하나요?"

    ### PostgreSQL RLS 보안 개요

    행 수준 보안(RLS)은 사용자 권한에 따라 데이터베이스 행을 자동으로 필터링합니다. 이를 통해 여러 사용자가 동일한 데이터베이스 테이블을 공유하면서도 액세스 권한이 있는 데이터만 볼 수 있습니다.
    
    이 시스템에서 본사 사용자는 모든 매장의 모든 데이터를 보고, 매장 관리자는 자신의 매장 정보만 볼 수 있도록 제한됩니다. 아래 예제는 `retail.orders` 테이블에 대해 RLS 정책이 어떻게 구현되는지 보여주며, `retail.order_items`, `retail.inventory`, `retail.customers` 테이블에도 동일한 정책이 적용됩니다.

    ```sql
    CREATE POLICY store_manager_orders ON retail.orders
    FOR ALL TO PUBLIC
    USING (
        -- 본사는 모든 데이터를 봄
        current_setting('app.current_rls_user_id', true) = '00000000-0000-0000-0000-000000000000'
        OR
        -- 매장 관리자는 자신의 매장 데이터만 봄
        EXISTS (SELECT 1 FROM retail.stores s WHERE s.store_id = retail.orders.store_id 
                AND s.rls_user_id::text = current_setting('app.current_rls_user_id', true))
    );
    ```

    **결과:** 매장 관리자는 자신의 매장 데이터만 보고, 본사는 모든 것을 봅니다 - 모두 동일한 데이터베이스와 테이블을 사용하면서.

    === "Python"

        사용자 역할을 설정하는 역할을 하는 코드는 `workshop/chat_manager.py` 파일에서 찾을 수 있습니다.

        ```python
        if request.rls_user_id:
            # RLS 사용자 ID 헤더로 동적 도구 리소스 생성
            mcp_tool_resource = MCPToolResource(
                server_label="ZavaSalesAnalysisMcpServer",
                headers={"x-rls-user-id": request.rls_user_id},
                require_approval="never",
            )
            tool_resources.mcp = [mcp_tool_resource]
        ```

*GitHub Copilot을 사용하여 번역됨.*
