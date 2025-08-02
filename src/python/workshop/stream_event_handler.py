import asyncio

from azure.ai.agents.aio import AgentsClient
from azure.ai.agents.models import (
    AsyncAgentEventHandler,
    MessageDeltaChunk,
    RunStatus,
    RunStep,
    RunStepDeltaChunk,
    ThreadMessage,
    ThreadRun,
)
from utilities import Utilities


class WebStreamEventHandler(AsyncAgentEventHandler[str]):
    """Handle LLM streaming events and tokens for web interface output."""

    def __init__(self, utilities: Utilities, agents_client: AgentsClient) -> None:
        super().__init__()
        # Only keep the variables that are actually used
        self.agents_client = agents_client
        self.util = utilities
        self.assistant_message = ""
        self.token_queue: asyncio.Queue = asyncio.Queue()
        self._is_closed = False

    async def cleanup(self) -> None:
        """Clean up resources and drain the queue."""
        if self._is_closed:
            return
            
        self._is_closed = True
        
        # Drain any remaining items in the queue
        try:
            while not self.token_queue.empty():
                try:
                    self.token_queue.get_nowait()
                except asyncio.QueueEmpty:
                    break
        except Exception as e:
            print(f"⚠️ Warning: Error during WebStreamEventHandler cleanup: {e}")

    async def put_safely(self, item: dict | str | None) -> bool:
        """Safely put an item in the queue, handling closed state."""
        if self._is_closed:
            return False
        try:
            await self.token_queue.put(item)
            return True
        except Exception as e:
            print(f"⚠️ Warning: Failed to put item in queue: {e}")
            return False

    def get_queue_size(self) -> int:
        """Get the current size of the token queue."""
        try:
            return self.token_queue.qsize()
        except Exception:
            return 0
    
    def is_closed(self) -> bool:
        """Check if the handler has been closed."""
        return self._is_closed

    async def on_message_delta(self, delta: MessageDeltaChunk) -> None:
        """Override to capture tokens for web streaming instead of terminal output."""
        if delta.text:
            self.assistant_message += delta.text
            # Put token in queue for web streaming
            await self.put_safely({"type": "text", "content": delta.text})

    async def on_thread_message(self, message: ThreadMessage) -> None:
        """Override to capture files and send them to web interface."""
        # Get files and store their information
        files = await self.util.get_files(message, self.agents_client)

        # Send file information to web interface
        if files:
            for file_info in files:
                # print(f"🔍 DEBUG: Sending file info: {file_info}")  # Debug
                await self.put_safely({"type": "file", "file_info": file_info})

    async def on_thread_run(self, run: ThreadRun) -> None:
        """Handle thread run events"""

        print(f"Run status: {run.status}, ID: {run.id}")
        if run.status == RunStatus.FAILED:
            print(f"Run failed. Error: {run.last_error}")
            print(f"Thread ID: {run.thread_id}")
            print(f"Run ID: {run.id}")

    async def on_run_step(self, step: RunStep) -> None:
        pass

    async def on_run_step_delta(self, delta: RunStepDeltaChunk) -> None:
        pass

    async def on_error(self, data: str) -> None:
        print(f"An error occurred. Data: {data}")

    async def on_done(self) -> None:
        """Handle stream completion."""
        pass

    async def on_unhandled_event(self, event_type: str, event_data: object) -> None:
        """Handle unhandled events."""
        print(f"Unhandled Event Type: {event_type}, Data: {event_data}")
