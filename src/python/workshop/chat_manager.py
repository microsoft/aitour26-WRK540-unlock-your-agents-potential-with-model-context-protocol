"""
Agent Service Module

Contains the AgentService class for handling chat message processing
and streaming responses.
"""

import asyncio
import contextlib
import logging
from datetime import datetime
from typing import AsyncGenerator, Dict, Protocol, cast

from azure.ai.agents.aio import AgentsClient
from azure.ai.agents.models import (
    Agent,
    AgentThread,
    AsyncToolSet,
    RunCompletionUsage,
    TruncationObject,
    TruncationStrategy,
)
from azure.ai.projects.aio import AIProjectClient
from config import Config
from opentelemetry import trace
from pydantic import BaseModel
from stream_event_handler import WebStreamEventHandler
from utilities import Utilities

# Get tracer instance
tracer = trace.get_tracer("zava_agent.tracing")
logger = logging.getLogger(__name__)


RESPONSE_TIMEOUT_SECONDS = 60


class AgentManagerProtocol(Protocol):
    """Protocol for AgentManager to avoid circular imports."""

    agents_client: AgentsClient | None
    project_client: AIProjectClient | None
    agent: Agent | None
    agents_by_rls_user_id: Dict[str, Agent]
    current_rls_user_id: str
    application_insights_connection_string: str

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
        self.session_threads: Dict[str, AgentThread] = {}
        self._session_lock = asyncio.Lock()

    async def get_or_create_thread(self, session_id: str) -> AgentThread:
        """Get existing thread for session or create a new one."""
        async with self._session_lock:
            if session_id in self.session_threads:
                return self.session_threads[session_id]

            if not self.agent_manager.agents_client:
                raise ValueError("AgentsClient is not initialized")

            # Create new thread for this session
            thread = await self.agent_manager.agents_client.threads.create()
            self.session_threads[session_id] = thread
            logger.info("Created new thread %s for session %s", thread.id, session_id)

            return thread

    async def clear_session_thread(self, session_id: str) -> None:
        """Clear thread for a specific session."""
        async with self._session_lock:
            if session_id in self.session_threads:
                thread = self.session_threads[session_id]
                if self.agent_manager.agents_client and self.agent_manager.agent:
                    with tracer.start_as_current_span("Zava Agent Chat Thread Deletion") as span:
                        await self.agent_manager.agents_client.threads.delete(thread.id)
                        span.set_attribute("thread_id", thread.id)
                        span.set_attribute("session_id", session_id)
                        span.set_attribute("agent_id", self.agent_manager.agent.id)
                        span.set_attribute("date_time", datetime.now().isoformat())
                del self.session_threads[session_id]

        logger.info("Cleared thread for session %s", session_id)

    async def process_chat_message(self, request: ChatRequest) -> AsyncGenerator[ChatResponse, None]:
        """Process chat message and stream responses."""
        usage: RunCompletionUsage | None = None
        run_status = None
        incomplete_details = None

        if not request.message.strip():
            yield ChatResponse(error="Empty message")
            return

        if not self.agent_manager.is_initialized:
            yield ChatResponse(error="Agent not initialized")
            return

        # Type guards - ensure all required components are available
        if not self.agent_manager.agents_client or not self.agent_manager.agent:
            yield ChatResponse(error="Agent components not properly initialized")
            return

        # Get or create session
        session_id = request.session_id or "default"
        try:
            # Create a span for this chat request
            message_preview = request.message[:50] + "..." if len(request.message) > 50 else request.message
            span_name = f"Zava Agent Chat Request: {message_preview}"

            with tracer.start_as_current_span(span_name) as span:
                # Get or create thread for this session
                session_thread = await self.get_or_create_thread(session_id)

                web_handler = None
                stream_task = None

                # Create the web streaming event handler with proper resource management
                web_handler = WebStreamEventHandler(self.utilities, self.agent_manager.agents_client)

                # Add some attributes to the span for better observability
                span.set_attribute("user_message", request.message)
                span.set_attribute("operation_type", "chat_request")
                span.set_attribute("agent_id", self.agent_manager.agent.id)
                span.set_attribute("thread_id", session_thread.id)
                span.set_attribute("session_id", session_id)

                # Create message in thread

                await self.agent_manager.agents_client.messages.create(
                    thread_id=session_thread.id,
                    role="user",
                    content=request.message,
                )

                # Start the stream in a background task
                async def run_stream() -> None:
                    # Capture references with type casts since we've already checked they're not None
                    agents_client = cast(AgentsClient, self.agent_manager.agents_client)
                    agent = cast(Agent, self.agent_manager.agent)
                    thread = session_thread  # Use the session-specific thread

                    # Limit context to last 5 messages (instead of default auto truncation)
                    truncation_strategy = TruncationObject(
                        type=TruncationStrategy.LAST_MESSAGES,  # or "last_messages"
                        last_messages=5,
                    )

                    try:
                        async with await agents_client.runs.stream(
                            thread_id=thread.id,
                            agent_id=agent.id,
                            event_handler=web_handler,
                            max_completion_tokens=Config.MAX_COMPLETION_TOKENS,
                            max_prompt_tokens=Config.MAX_PROMPT_TOKENS,
                            temperature=Config.TEMPERATURE,
                            top_p=Config.TOP_P,
                            truncation_strategy=truncation_strategy,
                        ) as stream:
                            await stream.until_done()

                        # Update the method-level variables
                        nonlocal usage, run_status, incomplete_details
                        usage = web_handler.usage
                        run_status = web_handler.run_status
                        incomplete_details = web_handler.incomplete_details

                    except Exception as e:
                        # cancel the run if it fails
                        if web_handler.run_id:
                            try:
                                await agents_client.runs.cancel(thread_id=thread.id, run_id=web_handler.run_id)
                            except Exception as cancel_error:
                                logger.warning("⚠️ Failed to cancel run %s: %s", web_handler.run_id, cancel_error)
                        logger.error("❌ Error in agent stream: %s", e)
                        # Send error to client safely
                        await web_handler.put_safely({"type": "error", "error": str(e)})
                        span.set_attribute("error", True)
                        span.set_attribute("error_message", str(e))
                    finally:
                        # Signal end of stream safely
                        await web_handler.put_safely(None)

                # Start the stream task
                stream_task = asyncio.create_task(run_stream())

            # Stream tokens as they arrive
            tokens_processed = 0
            try:
                while True:
                    try:
                        # Monitor queue health
                        queue_size = web_handler.get_queue_size()
                        if queue_size > 100:  # Warn if queue gets too large
                            logger.warning("⚠️ Token queue size is large: %d", queue_size)

                        # Wait for next token with timeout
                        item = await asyncio.wait_for(web_handler.token_queue.get(), timeout=RESPONSE_TIMEOUT_SECONDS)
                        if item is None:  # End of stream signal
                            break

                        tokens_processed += 1

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
                if stream_task and not stream_task.done():
                    stream_task.cancel()
                    with contextlib.suppress(asyncio.CancelledError):
                        await stream_task

                # Clean up any remaining items in the queue to prevent memory leaks
                if web_handler:
                    remaining_items = web_handler.get_queue_size()
                    if remaining_items > 0:
                        logger.info("🧹 Cleaning up %d remaining items in token queue", remaining_items)
                    await web_handler.cleanup()

            # Send completion signal
            if usage:
                yield ChatResponse(
                    content=f"</br></br>Token usage: Prompt: {usage.prompt_tokens}, Completion: {usage.completion_tokens}, Total: {usage.total_tokens}"
                )
            if incomplete_details:
                yield ChatResponse(content=f"</br>{incomplete_details.reason}")

            yield ChatResponse(done=True)
            logger.info("✅ Processed %d tokens successfully", tokens_processed)

        except Exception as e:
            logger.error("❌ Processing chat message: %s", e)
            yield ChatResponse(error=f"Streaming error: {e!s}")
