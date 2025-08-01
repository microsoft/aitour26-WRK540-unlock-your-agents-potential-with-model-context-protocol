"""
Agent Service Module

Contains the AgentService class for handling chat message processing
and streaming responses.
"""

import asyncio
import contextlib
from typing import AsyncGenerator, Dict, List, Protocol, cast

from azure.ai.agents.aio import AgentsClient
from azure.ai.agents.models import Agent, AgentThread, AsyncToolSet
from config import Config
from opentelemetry import trace
from pydantic import BaseModel
from stream_event_handler import WebStreamEventHandler
from utilities import Utilities

# Get tracer instance
tracer = trace.get_tracer("zava_agent.tracing")

RESPONSE_TIMEOUT_SECONDS = 60


class AgentManagerProtocol(Protocol):
    """Protocol for AgentManager to avoid circular imports."""

    agents_client: AgentsClient | None
    agent: Agent | None
    thread: AgentThread | None
    toolset: AsyncToolSet

    @property
    def is_initialized(self) -> bool: ...


# Pydantic models for API
class ChatRequest(BaseModel):
    message: str
    session_id: str | None = "default"


class ChatResponse(BaseModel):
    content: str | None = None
    file_info: Dict | None = None
    error: str | None = None
    done: bool = False


class ChatManager:
    """REST API service for the Azure AI Agent."""

    def __init__(self, agent_manager: AgentManagerProtocol) -> None:
        self.agent_manager = agent_manager
        self.utilities = Utilities()
        self.chat_sessions: Dict[str, List[Dict]] = {}

    async def process_chat_message(self, request: ChatRequest) -> AsyncGenerator[ChatResponse, None]:
        """Process chat message and stream responses."""
        if not request.message.strip():
            yield ChatResponse(error="Empty message")
            return

        if not self.agent_manager.is_initialized:
            yield ChatResponse(error="Agent not initialized")
            return

        # Type guards - ensure all required components are available
        if not self.agent_manager.agents_client or not self.agent_manager.agent or not self.agent_manager.thread:
            yield ChatResponse(error="Agent components not properly initialized")
            return

        # Get or create session
        session_id = request.session_id or "default"
        if session_id not in self.chat_sessions:
            self.chat_sessions[session_id] = []

        # Add user message to session
        self.chat_sessions[session_id].append({"role": "user", "content": request.message})

        try:
            # Create the web streaming event handler
            web_handler = WebStreamEventHandler(self.utilities, self.agent_manager.agents_client)

            # Create a span for this chat request
            message_preview = request.message[:50] + "..." if len(request.message) > 50 else request.message
            span_name = f"Zava Agent Chat Request: {message_preview}"

            with tracer.start_as_current_span(span_name) as span:
                # Add some attributes to the span for better observability
                span.set_attribute("user_message", request.message)
                span.set_attribute("operation_type", "chat_request")
                span.set_attribute("agent_id", self.agent_manager.agent.id)
                span.set_attribute("thread_id", self.agent_manager.thread.id)

                # Create message in thread
                with tracer.start_as_current_span("create_user_message") as message_span:
                    await self.agent_manager.agents_client.messages.create(
                        thread_id=self.agent_manager.thread.id,
                        role="user",
                        content=request.message,
                    )
                    message_span.set_attribute("thread_id", self.agent_manager.thread.id)

                # Start the agent stream
                with tracer.start_as_current_span("agent_stream_processing") as stream_span:
                    # Start the stream in a background task
                    async def run_stream() -> None:
                        # Capture references with type casts since we've already checked they're not None
                        agents_client = cast(AgentsClient, self.agent_manager.agents_client)
                        agent = cast(Agent, self.agent_manager.agent)
                        thread = cast(AgentThread, self.agent_manager.thread)
                        toolset = cast(AsyncToolSet, self.agent_manager.toolset)

                        try:
                            async with await agents_client.runs.stream(
                                thread_id=thread.id,
                                agent_id=agent.id,
                                event_handler=web_handler,
                                max_completion_tokens=Config.MAX_COMPLETION_TOKENS,
                                max_prompt_tokens=Config.MAX_PROMPT_TOKENS,
                                temperature=Config.TEMPERATURE,
                                top_p=Config.TOP_P,
                                tool_resources=toolset.resources,
                            ) as stream:
                                await stream.until_done()

                        except Exception as e:
                            print(f"❌ Error in agent stream: {e}")
                            # Send error to client
                            await web_handler.token_queue.put({"type": "error", "error": str(e)})
                            span.set_attribute("error", True)
                            span.set_attribute("error_message", str(e))
                            stream_span.set_attribute("error", True)
                            stream_span.set_attribute("error_message", str(e))
                        finally:
                            # Signal end of stream
                            await web_handler.token_queue.put(None)

                    # Start the stream task
                    stream_task = asyncio.create_task(run_stream())

            # Stream tokens as they arrive
            try:
                while True:
                    try:
                        # Wait for next token with timeout
                        item = await asyncio.wait_for(web_handler.token_queue.get(), timeout=RESPONSE_TIMEOUT_SECONDS)
                        if item is None:  # End of stream signal
                            break

                        # Yield response based on type
                        if isinstance(item, dict):
                            if item.get("type") == "text":
                                yield ChatResponse(content=item["content"])
                            elif item.get("type") == "file":
                                yield ChatResponse(file_info=item["file_info"])
                            elif item.get("type") == "error":
                                yield ChatResponse(error=item["error"])
                        else:
                            # Backwards compatibility for plain text
                            yield ChatResponse(content=str(item))

                    except asyncio.TimeoutError:
                        yield ChatResponse(error="Response timeout after 60 seconds")
                        break
            finally:
                # Ensure the stream task is properly cleaned up
                if not stream_task.done():
                    stream_task.cancel()
                    with contextlib.suppress(asyncio.CancelledError):
                        await stream_task

            # Add complete message to session
            if web_handler.assistant_message:
                self.chat_sessions[session_id].append({"role": "assistant", "content": web_handler.assistant_message})

            # Send completion signal
            yield ChatResponse(done=True)

        except Exception as e:
            yield ChatResponse(error=f"Streaming error: {e!s}")
