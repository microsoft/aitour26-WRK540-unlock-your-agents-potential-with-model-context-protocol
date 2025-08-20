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
from fastapi import FastAPI, Form, HTTPException
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

    async def _setup_agent_tools(self) -> None:
        """Setup MCP tools and code interpreter."""
        self.toolset = AsyncToolSet()

        # Add code interpreter tool
        code_interpreter = CodeInterpreterTool()
        self.toolset.add(code_interpreter)

        logger.info("Setting up Agent tools...")
        if Config.MAP_MCP_FUNCTIONS:
            # For function mapping, we'll create tools without RLS user ID
            # The RLS user ID will be passed via tool resources during run
            mcp_client = MCPClient.create_default("00000000-0000-0000-0000-000000000000")  # Default placeholder
            function_tools = await mcp_client.build_function_tools()
            self.toolset.add(function_tools)
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
            # Don't set RLS user ID header here - it will be set via tool resources per run
            mcp_tools.set_approval_mode("never")
            self.toolset.add(mcp_tools)

    def __init__(self) -> None:
        self.utilities = Utilities()
        self.agents_client: AgentsClient | None = None
        self.project_client: AIProjectClient | None = None
        self.agent: Agent | None = None
        self.tracer = tracer
        self.application_insights_connection_string = Config.APPLICATIONINSIGHTS_CONNECTION_STRING

    async def get_or_create_agent(self) -> Agent:
        """Get existing agent or create a new one."""
        if self.agent is not None:
            return self.agent

        if not self.agents_client:
            raise ValueError("AgentsClient is not initialized")

        # Check if agent already exists in the service
        # if self.agents_client:
        #     known_agents = self.agents_client.list_agents()
        #     async for agent in known_agents:
        #         if agent.name == Config.AGENT_NAME:
        #             logger.info("Found existing agent: %s", agent.name)
        #             self.agent = agent
        #             return agent

        # Create new agent if not found
        self.agent = await self.create_agent()
        return self.agent

    async def create_agent(self) -> Agent:
        """Create a new agent."""
        logger.info("Creating new agent: %s", Config.AGENT_NAME)

        if not self.agents_client:
            raise ValueError("AgentsClient is not initialized")

        # Load LLM instructions
        instructions = self.utilities.load_instructions(INSTRUCTIONS_FILE)

        # Setup tools (without RLS user specifics)
        await self._setup_agent_tools()

        with self.tracer.start_as_current_span(trace_scenario):
            # Create agent without RLS-specific configuration
            agent = await self.agents_client.create_agent(
                model=Config.GPT_MODEL_DEPLOYMENT_NAME,
                name=Config.AGENT_NAME,
                instructions=instructions,
                toolset=self.toolset,
                temperature=Config.TEMPERATURE,
            )
            logger.info("Created agent, ID: %s", agent.id)

            # Enable auto function calls
            if self.toolset.definitions and Config.MAP_MCP_FUNCTIONS:
                self.agents_client.enable_auto_function_calls(tools=self.toolset)

        return agent

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

            # Initialize single agent
            await self.get_or_create_agent()

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
async def set_rls_user(rls_user_id: str = Form(...)) -> RlsUserResult:
    """Set the RLS user ID for the agent service (compatibility endpoint)."""
    try:
        if not agent_manager.is_initialized:
            raise HTTPException(status_code=500, detail="Agent not initialized")

        # Validate the RLS user ID exists
        user_name_map = {
            Config.Rls.ZAVA_HEADOFFICE_USER_ID: "Head Office",
            Config.Rls.ZAVA_SEATTLE_USER_ID: "Seattle",
            Config.Rls.ZAVA_BELLEVUE_USER_ID: "Bellevue",
            Config.Rls.ZAVA_TACOMA_USER_ID: "Tacoma",
            Config.Rls.ZAVA_SPOKANE_USER_ID: "Spokane",
            Config.Rls.ZAVA_EVERETT_USER_ID: "Everett",
            Config.Rls.ZAVA_REDOND_USER_ID: "Redmond",
            Config.Rls.ZAVA_KIRKLAND_USER_ID: "Kirkland",
            Config.Rls.ZAVA_ONLINE_USER_ID: "Online",
        }

        if rls_user_id not in user_name_map:
            raise ValueError(f"Invalid RLS user ID: {rls_user_id}")

        user_name = user_name_map[rls_user_id]
        message = f"RLS user ID acknowledged: {user_name}"
        logger.info("RLS user ID set: %s (%s)", rls_user_id, user_name)

        return RlsUserResult(message=message, rls_user_id=rls_user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        logger.error("Error setting RLS user ID: %s", e)
        raise HTTPException(status_code=500, detail=f"Failed to set RLS user ID: {e!s}") from e


@app.get("/agent/rls-user")
async def get_rls_user() -> Dict[str, str]:
    """Get the current RLS user ID from the agent service (compatibility endpoint)."""
    try:
        if not agent_manager.is_initialized:
            raise HTTPException(status_code=500, detail="Agent not initialized")

        # Return default RLS user ID since we no longer maintain state
        default_rls_user_id = Config.Rls.ZAVA_HEADOFFICE_USER_ID
        return {"status": "success", "rls_user_id": default_rls_user_id}
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
