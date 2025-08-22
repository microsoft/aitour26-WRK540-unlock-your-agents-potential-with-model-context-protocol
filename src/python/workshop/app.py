"""
Azure AI Agent Web Application

This web application creates an AI agent that can interact with a PostgreSQL database
using Model Context Protocol (MCP) tools and provides a REST API for chat.

To run: python app.py
REST API available at: http://127.0.0.1:8006
"""

import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, AsyncGenerator, Dict

from azure.ai.agents.aio import AgentsClient
from azure.ai.agents.models import Agent, AsyncToolSet, CodeInterpreterTool, McpTool
from azure.ai.projects.aio import AIProjectClient
from azure.monitor.opentelemetry import configure_azure_monitor
from chat_manager import ChatManager, ChatRequest
from config import Config
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, Response, StreamingResponse
from opentelemetry import trace
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from utilities import Utilities

trace_scenario = "Zava Agent Initialization"
tracer = trace.get_tracer("zava_agent.tracing")
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

Utilities.suppress_logs()

# Agent Instructions
INSTRUCTIONS_FILE = "instructions/mcp_server_tools_with_code_interpreter.txt"
# INSTRUCTIONS_FILE = "instructions/mcp_server_tools_with_semantic_search.txt"

RESPONSE_TIMEOUT_SECONDS = 60

trace_scenario = "Zava Agent Initialization"


class AgentManager:
    """Manages Azure AI Agent lifecycle and dependencies."""

    async def _setup_agent_tools(self) -> None:
        """Setup MCP tools and code interpreter."""
        logger.info("Setting up Agent tools...")
        self.toolset = AsyncToolSet()

        # Add code interpreter tool
        # code_interpreter = CodeInterpreterTool()
        # self.toolset.add(code_interpreter)

        # Add MCP tools
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

    def __init__(self) -> None:
        self.utilities = Utilities()
        self.agents_client: AgentsClient | None = None
        self.project_client: AIProjectClient | None = None
        self.agent: Agent | None = None
        self.tracer = tracer
        self.application_insights_connection_string = Config.APPLICATIONINSIGHTS_CONNECTION_STRING

    async def initialize(self, instructions_file: str) -> bool:
        """Initialize the agent with tools and instructions."""
        try:
            # Validate configuration
            Config.validate_required_env_vars()

            # Load LLM instructions
            instructions = self.utilities.load_instructions(instructions_file)

            # Validate Azure Entra ID Authentication
            credential = await self.utilities.validate_azure_authentication()

            # Create clients
            self.agents_client = AgentsClient(
                credential=credential,
                endpoint=Config.PROJECT_ENDPOINT,
            )

            self.project_client = AIProjectClient(
                credential=credential,
                endpoint=Config.PROJECT_ENDPOINT,
            )

            await self._setup_agent_tools()

            configure_azure_monitor(connection_string=self.application_insights_connection_string)

            with self.tracer.start_as_current_span(trace_scenario):
                # Create agent
                self.agent = await self.agents_client.create_agent(
                    model=Config.GPT_MODEL_DEPLOYMENT_NAME,
                    name=Config.AGENT_NAME,
                    instructions=instructions,
                    toolset=self.toolset,
                    temperature=Config.TEMPERATURE,
                )
                logger.info("Created agent, ID: %s", self.agent.id)

            return True

        except Exception as e:
            logger.error("Agent initialization failed: %s", str(e))
            return False

    @property
    def is_initialized(self) -> bool:
        """Check if agent is properly initialized."""
        return all([self.agents_client, self.project_client, self.agent])


# Global service instance
agent_manager = AgentManager()
agent_service = ChatManager(agent_manager)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    """Handle startup and shutdown events"""
    # Startup
    logger.info("Initializing agent service on startup...")

    # Initialize agent
    success = await agent_manager.initialize(INSTRUCTIONS_FILE)

    if not success:
        logger.warning("Agent initialization failed. Check your configuration.")
    elif agent_manager.is_initialized and agent_manager.agent:
        logger.info("✅ Agent initialized successfully with ID: %s", agent_manager.agent.id)

    yield


# FastAPI app with lifespan
app = FastAPI(title="Azure AI Agent Service", lifespan=lifespan)
HTTPXClientInstrumentor().instrument()  # Instrument httpx client for tracing


@app.get("/health")
async def health_check() -> Response:
    """Health check endpoint."""
    if agent_manager.is_initialized:
        # Agent is properly initialized - healthy
        return Response(status_code=200)
    # Agent is not initialized - unhealthy
    logger.warning("Health check failed: Agent manager is not initialized")
    return Response(status_code=503)


@app.post("/chat/stream")
@app.get("/chat/stream")
async def stream_chat(request: ChatRequest) -> StreamingResponse:
    """Stream chat responses."""

    async def generate_stream() -> AsyncGenerator[str, None]:
        async for response in agent_service.process_chat_message(request):
            yield f"data: {response.model_dump_json()}\n\n"

    return StreamingResponse(
        generate_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
            "Access-Control-Allow-Origin": "*",
            "Content-Encoding": "identity",
        },
    )


@app.delete("/chat/clear")
async def clear_chat(request: ChatRequest) -> Dict[str, Any]:
    """Clear the chat session and thread for a specific session."""
    try:
        if not agent_manager.is_initialized or not agent_manager.agents_client or not agent_manager.agent:
            raise HTTPException(status_code=500, detail="Agent not initialized")

        # Get session_id and rls_user_id from the request object
        session_id = request.session_id or "default"
        rls_user_id = request.rls_user_id or "00000000-0000-0000-0000-000000000000"

        # Clear the specific session and its thread
        await agent_service.clear_session_thread(session_id)

        return {
            "status": "success",
            "message": f"Chat session '{session_id}' cleared successfully",
            "rls_user_id": rls_user_id,
        }
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        session_id_for_log = request.session_id or "default"
        logger.error("Error clearing chat for session %s: %s", session_id_for_log, e)
        raise HTTPException(status_code=500, detail=f"Failed to clear chat: {e!s}") from e


@app.get("/files/{filename}")
async def serve_file(filename: str) -> FileResponse:
    """Serve files from the shared files directory."""
    files_dir = Path(agent_service.utilities.shared_files_path) / "files"
    file_path = files_dir / filename

    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    # Security check: ensure the file is within the files directory
    try:
        file_path.resolve().relative_to(files_dir.resolve())
    except ValueError as exc:
        raise HTTPException(status_code=403, detail="Access denied") from exc

    return FileResponse(path=str(file_path))


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8006))
    logger.info("Starting agent service on port %d", port)
    uvicorn.run(app, host="127.0.0.1", port=port)
