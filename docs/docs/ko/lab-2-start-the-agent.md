## 학습할 내용

이 랩에서는 코드 인터프리터를 활성화하여 자연어를 사용해 판매 데이터를 분석하고 차트를 생성합니다.

## 소개

이 랩에서는 Azure AI 에이전트를 두 가지 도구로 확장합니다:

- **코드 인터프리터:** 에이전트가 데이터 분석과 시각화를 위해 Python 코드를 생성하고 실행할 수 있게 합니다.
- **MCP 서버 도구:** 에이전트가 MCP 도구를 사용하여 외부 데이터 소스에 액세스할 수 있게 하며, 우리의 경우 PostgreSQL 데이터베이스의 데이터입니다.

## 랩 실습

### 코드 인터프리터와 MCP 서버 활성화

이 랩에서는 함께 작동하는 두 가지 강력한 도구를 활성화합니다: 코드 인터프리터(데이터 분석과 시각화를 위해 AI 생성 Python 코드를 실행)와 MCP 서버(PostgreSQL에 저장된 Zava의 판매 데이터에 대한 안전한 액세스 제공).

=== "Python"

    1. `app.py`를 **열기**합니다.
    2. **50행 근처로 스크롤**하여 에이전트의 도구 세트에 코드 인터프리터와 MCP 도구를 추가하는 줄을 찾습니다. 이 줄들은 현재 시작 부분에 `#`로 주석 처리되어 있습니다.
    3. 다음 줄들의 **주석을 해제**합니다:

        ```python
        
        # code_interpreter = CodeInterpreterTool()
        # self.toolset.add(code_interpreter)
        
        # mcp_tools = McpTool(
        #     server_label="ZavaSalesAnalysisMcpServer",
        #     server_url=Config.DEV_TUNNEL_URL,
        #     allowed_tools=[
        #         "get_multiple_table_schemas",
        #         "execute_sales_query",
        #         "get_current_utc_date",
        #         "semantic_search_products",
        #     ],
        # )

        # mcp_tools.set_approval_mode("never")  # No human in the loop
        # self.toolset.add(mcp_tools)
        ```

        !!! info "이 코드는 무엇을 하나요?"
            - **코드 인터프리터**: 에이전트가 데이터 분석과 시각화를 위해 Python 코드를 실행할 수 있게 합니다.
            - **MCP 서버 도구**: 특정 허용된 도구로 외부 데이터 소스에 대한 액세스를 제공하며 인간 승인이 필요하지 않습니다. 프로덕션 애플리케이션의 경우 민감한 작업에 대해 인간 승인 루프 활성화를 고려하세요.

    4. 주석을 해제한 코드를 **검토**합니다. 코드는 정확히 다음과 같아야 합니다:

        ```python

        주석 해제 후 코드는 다음과 같아야 합니다:

        ```python
        class AgentManager:
            """Manages Azure AI Agent lifecycle and dependencies."""

            async def _setup_agent_tools(self) -> None:
                """Setup MCP tools and code interpreter."""
                logger.info("Setting up Agent tools...")
                self.toolset = AsyncToolSet()

                code_interpreter = CodeInterpreterTool()
                self.toolset.add(code_interpreter)

                mcp_tools = McpTool(
                    server_label="ZavaSalesAnalysisMcpServer",
                    server_url=Config.DEV_TUNNEL_URL,
                    allowed_tools=[
                        "get_multiple_table_schemas",
                        "execute_sales_query",
                        "get_current_utc_date",
                        "semantic_search_products",
                    ],
                )

                mcp_tools.set_approval_mode("never")  # No human in the loop
                self.toolset.add(mcp_tools)
        ```

    ## 에이전트 앱 시작

    1. 아래 텍스트를 클립보드에 복사하세요:

    ```text
    Debug: Select and Start Debugging
    ```

    1. <kbd>F1</kbd>을 눌러 VS Code 명령 팔레트를 엽니다.
    1. 명령 팔레트에 텍스트를 붙여넣고 **Debug: Select and Start Debugging**을 선택합니다.
    1. 목록에서 **🌎🤖Debug Compound: Agent and MCP (http)**를 선택합니다. 이렇게 하면 에이전트 앱과 웹 채팅 클라이언트가 시작됩니다.

    이렇게 하면 다음 프로세스가 시작됩니다:

    1.  DevTunnel (workshop) 작업
    2.  웹 채팅 (workshop)
    3.  에이전트 매니저 (workshop)
    4.  MCP 서버 (workshop)

    VS Code에서 TERMINAL 패널에서 이것들이 실행 중인 것을 볼 수 있습니다.

    ![이미지는 VS Code TERMINAL 패널에서 실행 중인 프로세스들을 보여줍니다](../media/vs-code-processes.png)

    ## 에이전트 웹 채팅 클라이언트 열기

    === "@이벤트 참가자"

        다음 링크를 선택하여 브라우저에서 웹 채팅 앱을 엽니다.

        [웹 채팅 열기](http://localhost:8005){:target="_blank"}

    === "셀프 가이드 학습자"

        ## 포트 8005를 공용으로 설정

        브라우저에서 웹 채팅 클라이언트에 액세스하려면 포트 8005를 공용으로 설정해야 합니다.

        1. VS Code 하단 패널에서 **Ports** 탭을 선택합니다.
        2. **Web Chat App (8005)** 포트를 오른쪽 클릭하고 **Port Visibility**를 선택합니다.
        3. **Public**을 선택합니다.

        ![](../media/make-port-public.png)


        ## 브라우저에서 웹 채팅 클라이언트 열기

        1.  아래 텍스트를 클립보드에 복사하세요:

        ```text
        Open Port in Browser
        ```

        2.  <kbd>F1</kbd>을 눌러 VS Code 명령 팔레트를 엽니다.
        3.  명령 팔레트에 텍스트를 붙여넣고 **Open Port in Browser**를 선택합니다.
        4.  목록에서 **8005**를 선택합니다. 이렇게 하면 브라우저에서 에이전트 웹 채팅 클라이언트가 열립니다.

    ![](../media/agent_web_chat.png)

=== "C#"

    1. `McpAgentWorkshop.WorkshopApi` 프로젝트의 `Services` 폴더에서 `AgentService.cs`를 **엽니다**.
    2. `InitialiseAgentAsync` 메소드로 이동합니다.
    3. 다음 줄들의 **주석을 해제**합니다:

        ```csharp
        // var mcpTool = new MCPToolDefinition(
        //     ZavaMcpToolLabel,
        //     devtunnelUrl + "mcp");

        // var codeInterpreterTool = new CodeInterpreterToolDefinition();

        // IEnumerable<ToolDefinition> tools = [mcpTool, codeInterpreterTool];

        // persistentAgent = await persistentAgentsClient.Administration.CreateAgentAsync(
        //         name: AgentName,
        //         model: configuration.GetValue<string>("MODEL_DEPLOYMENT_NAME"),
        //         instructions: instructionsContent,
        //         temperature: modelTemperature,
        //         tools: tools);

        // logger.LogInformation("Agent created with ID: {AgentId}", persistentAgent.Id);
        ```

    ## 에이전트 앱 시작

    4. <kbd>F1</kbd>을 눌러 VS Code 명령 팔레트를 엽니다.
    5. 시작 구성으로 **Debug Aspire**를 선택합니다.

    디버거가 시작되면 Aspire 대시보드와 함께 브라우저 창이 열립니다. 모든 리소스가 시작되면 **Workshop Frontend** 링크를 클릭하여 워크샵 웹 애플리케이션을 시작할 수 있습니다.

    ![Aspire 대시보드](../media//lab-2-start-agent-aspire-dashboard.png)

    !!! tip "문제 해결"
        브라우저가 로드되지 않으면 페이지를 강제 새로고침해 보세요(Ctrl + F5 또는 Cmd + Shift + R). 여전히 로드되지 않으면 [문제 해결 가이드](./dotnet-troubleshooting.md)를 참조하세요.

## 에이전트와 대화 시작

웹 채팅 클라이언트에서 에이전트와 대화를 시작할 수 있습니다. 에이전트는 Zava의 판매 데이터에 대한 질문에 답하고 코드 인터프리터를 사용하여 시각화를 생성하도록 설계되었습니다.

1.  제품 판매 분석. 다음 질문을 복사하여 채팅에 붙여넣으세요:

    ```text
    Show the top 10 products by revenue by store for the last quarter
    ```

    잠시 후 에이전트는 각 매장별 수익 상위 10개 제품을 보여주는 테이블로 응답합니다.

    !!! info
        에이전트는 LLM이 세 개의 MCP 서버 도구를 호출하여 데이터를 가져와 테이블로 표시합니다:

        1. **get_current_utc_date()**: 현재 날짜와 시간을 가져와서 에이전트가 현재 날짜를 기준으로 지난 분기를 결정할 수 있게 합니다.
        2. **get_multiple_table_schemas()**: LLM이 유효한 SQL을 생성하는 데 필요한 데이터베이스 테이블의 스키마를 가져옵니다.
        3. **execute_sales_query**: PostgreSQL 데이터베이스에서 지난 분기 수익 상위 10개 제품을 가져오는 SQL 쿼리를 실행합니다.

    !!! tip
        === "Python"

            VS Code로 돌아가서 TERMINAL 패널에서 **MCP Server (workspace)**를 선택하면 Azure AI Foundry 에이전트 서비스가 MCP 서버에 한 호출을 볼 수 있습니다.

            ![](../media/mcp-server-in-action.png)

        === "C#"

            Aspire 대시보드에서 `dotnet-mcp-server` 리소스의 로그를 선택하여 Azure AI Foundry 에이전트 서비스가 MCP 서버에 한 호출을 볼 수 있습니다.

            또한 추적 보기를 열고 웹 채팅의 사용자 입력부터 에이전트 호출 및 MCP 도구 호출까지 애플리케이션의 엔드투엔드 추적을 찾을 수 있습니다.

            ![추적 개요](../media/lab-7-trace-overview.png)

2.  파이 차트 생성. 다음 질문을 복사하여 채팅에 붙여넣으세요:

    ```text
    Show sales by store as a pie chart for this financial year
    ```

    에이전트는 현재 회계연도의 매장별 판매 분포를 보여주는 파이 차트로 응답합니다.

    !!! info
        마법처럼 느껴질 수 있으니, 모든 것이 작동하도록 하는 뒤에서 일어나는 일을 살펴보겠습니다.

        Foundry 에이전트 서비스는 다음 단계를 조정합니다:

        1. 이전 질문과 같이, 에이전트는 쿼리에 필요한 테이블 스키마가 있는지 확인합니다. 없으면 **get_multiple_table_schemas()** 도구를 사용하여 현재 날짜와 데이터베이스 스키마를 가져옵니다.
        2. 그런 다음 에이전트는 **execute_sales_query** 도구를 사용하여 판매 데이터를 가져옵니다.
        3. 반환된 데이터를 사용하여 LLM은 파이 차트를 생성하는 Python 코드를 작성합니다.
        4. 마지막으로 코드 인터프리터는 Python 코드를 실행하여 차트를 생성합니다.

3.  Zava 판매 데이터에 대해 계속 질문하여 코드 인터프리터가 작동하는 것을 확인하세요. 시도해 볼 만한 몇 가지 후속 질문은 다음과 같습니다:

    - `판매를 주도하는 제품이나 카테고리를 결정하세요. 막대 차트로 보여주세요.`
    - `충격 사건(예: 한 지역에서 20% 판매 감소)이 전 세계 판매 분포에 미치는 영향은 무엇입니까? 그룹화된 막대 차트로 보여주세요.`
      - `충격 사건이 50%라면 어떨까요?`로 후속 질문하세요.
    - `평균보다 위 또는 아래의 판매를 가진 지역은 어디입니까? 평균 편차가 있는 막대 차트로 보여주세요.`
    - `평균보다 위 또는 아래의 할인을 가진 지역은 어디입니까? 평균 편차가 있는 막대 차트로 보여주세요.`
    - `몬테카를로 시뮬레이션을 사용하여 지역별 미래 판매를 시뮬레이션하여 신뢰 구간을 추정하세요. 생생한 색상을 사용한 신뢰 밴드가 있는 선으로 보여주세요.`

<!-- ## 에이전트 앱 중지

1. VS Code 편집기로 돌아갑니다.
1. <kbd>Shift + F5</kbd>를 눌러 에이전트 앱을 중지합니다. -->

## 에이전트 앱 실행 상태 유지

다음 랩에서 에이전트를 더 많은 도구와 기능으로 확장하는 데 사용할 것이므로 에이전트 앱을 실행 상태로 유지하세요.

*GitHub Copilot을 사용하여 번역됨.*
