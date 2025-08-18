"""
Azure AI Agent Web Application

This web application creates an AI agent that can interact with a PostgreSQL database
using Model Context Protocol (MCP) tools and provides a REST API for chat.

To run: python app.py
REST API available at: http://127.0.0.1:8006
"""

import asyncio
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
from mcp_client import MCPClient
from models import RlsUserRequest, RlsUserResult
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

    async def _setup_agent_tools(self, rls_user_id: str) -> AsyncToolSet:
        """Setup MCP tools and code interpreter for a specific RLS user."""
        toolset = AsyncToolSet()

        # Add code interpreter tool
        code_interpreter = CodeInterpreterTool()
        toolset.add(code_interpreter)

        logger.info("Setting up Agent tools for RLS user: %s", rls_user_id)
        if Config.MAP_MCP_FUNCTIONS:
            mcp_client = MCPClient.create_default(rls_user_id)
            function_tools = await mcp_client.build_function_tools()
            toolset.add(function_tools)
        else:
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
            # PostgreSQL Row Level Security (RLS) User ID header
            mcp_tools.update_headers("x-rls-user-id", rls_user_id)
            # Disabled as specified in allowed tools
            mcp_tools.set_approval_mode("never")
            toolset.add(mcp_tools)

        return toolset

    def __init__(self) -> None:
        self.utilities = Utilities()
        self.agents_client: AgentsClient | None = None
        self.project_client: AIProjectClient | None = None
        self.agent: Agent | None = None
        self.agents_by_rls_user_id: Dict[str, Agent] = {}
        self.current_rls_user_id = Config.Rls.ZAVA_HEADOFFICE_USER_ID
        self.tracer = tracer
        self.application_insights_connection_string = Config.APPLICATIONINSIGHTS_CONNECTION_STRING
        self._agent_lock = asyncio.Lock()

    async def get_or_create_agent_for_rls_user(self, rls_user_id: str, rls_user_name: str) -> Agent:
        """Get existing agent for RLS user or create a new one."""
        if rls_user_id in self.agents_by_rls_user_id:
            return self.agents_by_rls_user_id[rls_user_id]

        # Check if agent already exists in the service
        target_agent_name = f"{Config.AGENT_NAME} - {rls_user_name}"

        if self.agents_client:
            known_agents = self.agents_client.list_agents()
            async for agent in known_agents:
                if agent.name == target_agent_name:
                    self.agents_by_rls_user_id[rls_user_id] = agent
                    return agent

        # Create new agent if not found
        new_agent = await self.create_agent(rls_user_id, rls_user_name)
        self.agents_by_rls_user_id[rls_user_id] = new_agent
        return new_agent

    async def create_agent(self, rls_user_id: str, rls_user_name: str) -> Agent:
        """Create a new agent for a specific RLS user."""
        agent_name = f"{Config.AGENT_NAME} - {rls_user_name}"
        logger.info("Creating new agent: %s", agent_name)

        if not self.agents_client:
            raise ValueError("AgentsClient is not initialized")

        # Load LLM instructions
        instructions = self.utilities.load_instructions(INSTRUCTIONS_FILE)

        # Setup tools for this specific RLS user
        toolset = await self._setup_agent_tools(rls_user_id)

        with self.tracer.start_as_current_span(trace_scenario):
            # Create agent
            agent = await self.agents_client.create_agent(
                model=Config.GPT_MODEL_DEPLOYMENT_NAME,
                name=agent_name,
                instructions=instructions,
                toolset=toolset,
                temperature=Config.TEMPERATURE,
            )
            logger.info("Created agent, ID: %s", agent.id)

            # Enable auto function calls
            if toolset.definitions and Config.MAP_MCP_FUNCTIONS:
                self.agents_client.enable_auto_function_calls(tools=toolset)

        return agent

    async def set_rls_user_id(self, rls_user_id: str, rls_user_name: str) -> str:
        """Set the RLS user ID and switch to appropriate agent."""
        if not rls_user_id.strip():
            raise ValueError("RLS User ID cannot be empty")

        async with self._agent_lock:
            self.current_rls_user_id = rls_user_id
            await self.get_or_create_agent_for_rls_user(rls_user_id, rls_user_name)
            self.agent = self.agents_by_rls_user_id[rls_user_id]

            logger.info("Switched to agent for RLS User ID: %s", rls_user_id)
            return f"Successfully switched to agent for RLS User ID: {rls_user_id}"

    def get_current_rls_user_id(self) -> str:
        """Get the current RLS user ID."""
        return self.current_rls_user_id

    async def initialize(self) -> bool:
        """Initialize the agent with tools and instructions."""
        try:
            # Validate configuration
            Config.validate_required_env_vars()

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

            configure_azure_monitor(connection_string=self.application_insights_connection_string)

            # Initialize with default RLS user ID
            await self.get_or_create_agent_for_rls_user(self.current_rls_user_id, "Head Office")
            self.agent = self.agents_by_rls_user_id[self.current_rls_user_id]

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
    success = await agent_manager.initialize()

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
async def clear_chat(session_id: str = "default") -> Dict[str, Any]:
    """Clear the chat session and thread for a specific session."""
    try:
        if not agent_manager.is_initialized or not agent_manager.agents_client or not agent_manager.agent:
            raise HTTPException(status_code=500, detail="Agent not initialized")

        # Clear the specific session and its thread
        await agent_service.clear_session_thread(session_id)

        return {
            "status": "success",
            "message": f"Chat session '{session_id}' cleared successfully",
        }
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error("Error clearing chat for session %s: %s", session_id, e)
        raise HTTPException(status_code=500, detail=f"Failed to clear chat: {e!s}") from e


@app.post("/agent/rls-user")
async def set_rls_user(request: RlsUserRequest) -> RlsUserResult:
    """Set the RLS user ID for the agent service."""
    try:
        if not agent_manager.is_initialized:
            raise HTTPException(status_code=500, detail="Agent not initialized")

        message = await agent_manager.set_rls_user_id(request.id, request.name)
        return RlsUserResult(message=message, rls_user_id=request.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        logger.error("Error setting RLS user ID: %s", e)
        raise HTTPException(status_code=500, detail=f"Failed to set RLS user ID: {e!s}") from e


@app.get("/agent/rls-user")
async def get_rls_user() -> Dict[str, str]:
    """Get the current RLS user ID from the agent service."""
    try:
        if not agent_manager.is_initialized:
            raise HTTPException(status_code=500, detail="Agent not initialized")

        current_rls_user_id = agent_manager.get_current_rls_user_id()
        return {"rls_user_id": current_rls_user_id}
    except Exception as e:
        logger.error("Error getting RLS user ID: %s", e)
        raise HTTPException(status_code=500, detail=f"Failed to get RLS user ID: {e!s}") from e


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
