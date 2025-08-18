import asyncio
import logging
import re

from azure.ai.agents.aio import AgentsClient
from azure.ai.agents.models import (
    AsyncAgentEventHandler,
    IncompleteRunDetails,
    MessageDeltaChunk,
    RunCompletionUsage,
    RunStatus,
    RunStep,
    RunStepDeltaChunk,
    ThreadMessage,
    ThreadRun,
)
from utilities import Utilities

logger = logging.getLogger(__name__)


class WebStreamEventHandler(AsyncAgentEventHandler[str]):
    """Handle LLM streaming events and tokens for web interface output."""

    markdown_pattern = re.compile(r"!?\[[^\]]*\]\(sandbox:/mnt/data[^)]*\)")

    def __init__(self, utilities: Utilities, agents_client: AgentsClient) -> None:
        super().__init__()
        # Only keep the variables that are actually used
        self.agents_client = agents_client
        self.util = utilities
        self.assistant_message = ""
        self.token_queue: asyncio.Queue = asyncio.Queue()
        self._is_closed = False
        self.run_id: str | None = None
        self.run_status: str | None = None
        self.usage: RunCompletionUsage | None = None
        self.incomplete_details: IncompleteRunDetails | None = None

        # Buffer for filtering markdown images and links
        self.text_buffer = ""
        # Maximum buffer size to prevent memory issues
        self.max_buffer_size = 1000

    async def cleanup(self) -> None:
        """Clean up resources and drain the queue."""
        if self._is_closed:
            return

        self._is_closed = True
        # Clear the text buffer
        self.text_buffer = ""

        # Drain any remaining items in the queue
        try:
            while not self.token_queue.empty():
                try:
                    self.token_queue.get_nowait()
                except asyncio.QueueEmpty:
                    break
        except Exception as e:
            logger.error("Error during WebStreamEventHandler cleanup: %s", e)

    async def put_safely(self, item: dict | str | None) -> bool:
        """Safely put an item in the queue, handling closed state."""
        if self._is_closed:
            return False
        try:
            await self.token_queue.put(item)
            return True
        except Exception as e:
            logger.warning("Failed to put item in queue: %s", e)
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

    async def _process_buffered_text(self) -> None:
        """Process buffered text, filtering out complete markdown image and link patterns."""
        if not self.text_buffer:
            return

        # Look for complete markdown image and link patterns
        matches = list(self.markdown_pattern.finditer(self.text_buffer))

        if matches:
            # Remove complete markdown image and link patterns
            filtered_text = self.markdown_pattern.sub("", self.text_buffer)

            # Send the filtered text if there's any content left
            if filtered_text:
                await self.put_safely({"type": "text", "content": filtered_text})

            # Clear the buffer since we processed complete patterns
            self.text_buffer = ""
        else:
            # Check if buffer might contain a partial markdown pattern
            # Look for potential start of markdown image: ![ or link: [
            # Also check for just ! which might be the start of ![
            image_start_idx = self.text_buffer.rfind("![")
            link_start_idx = self.text_buffer.rfind("[")
            exclamation_idx = self.text_buffer.rfind("!")

            # Determine the partial pattern start index
            partial_start_idx = -1

            # If we have ![, it takes precedence
            if image_start_idx != -1:
                partial_start_idx = image_start_idx
            # If we have a standalone [ (not part of ![)
            elif link_start_idx != -1:
                if image_start_idx == -1 or link_start_idx > image_start_idx + 1:
                    partial_start_idx = link_start_idx
            # If we have a standalone ! that might become ![
            elif exclamation_idx != -1 and exclamation_idx == len(self.text_buffer) - 1:
                partial_start_idx = exclamation_idx

            if partial_start_idx != -1:
                # Keep potential partial pattern in buffer, send the rest
                text_to_send = self.text_buffer[:partial_start_idx]
                self.text_buffer = self.text_buffer[partial_start_idx:]

                if text_to_send:
                    await self.put_safely({"type": "text", "content": text_to_send})
            else:
                # No potential patterns, send all buffered text
                await self.put_safely({"type": "text", "content": self.text_buffer})
                self.text_buffer = ""

        # Prevent buffer from growing too large
        if len(self.text_buffer) > self.max_buffer_size:
            # Send the buffer content and reset to prevent memory issues
            await self.put_safely({"type": "text", "content": self.text_buffer})
            self.text_buffer = ""

    async def on_message_delta(self, delta: MessageDeltaChunk) -> None:
        """Override to capture tokens for web streaming, filtering out markdown images and links."""
        if delta.text:
            self.assistant_message += delta.text

            # Add to buffer for processing
            self.text_buffer += delta.text

            # Process the buffer to filter out markdown images and links
            await self._process_buffered_text()

    async def on_thread_message(self, message: ThreadMessage) -> None:
        """Override to capture files and send them to web interface."""
        # Get files and store their information
        files = await self.util.get_files(message, self.agents_client)

        # Send file information to web interface
        if files:
            for file_info in files:
                # logger.debug("Sending file info: %s", file_info)
                await self.put_safely({"type": "file", "file_info": file_info})

    async def on_thread_run(self, run: ThreadRun) -> None:
        """Handle thread run events"""
        # Store the run ID for later access
        self.run_id = run.id
        self.run_status = run.status
        self.usage = run.usage
        self.incomplete_details = run.incomplete_details

        logger.info("Run status: %s, ID: %s", run.status, run.id)

        if run.status == RunStatus.FAILED or run.status == "incomplete":
            logger.error("Run failed. Error: %s", run.last_error)
            logger.error("Thread ID: %s", run.thread_id)
            logger.error("Run ID: %s", run.id)
            logger.error("Incomplete details: %s", run.incomplete_details)

    async def on_run_step(self, step: RunStep) -> None:
        pass

    async def on_run_step_delta(self, delta: RunStepDeltaChunk) -> None:
        pass

    async def on_error(self, data: str) -> None:
        logger.error("An error occurred. Data: %s", data)

    async def on_done(self) -> None:
        """Handle stream completion and flush any remaining buffered content."""
        # Flush any remaining content in the buffer
        if self.text_buffer:
            # For final flush, remove any markdown images and links but send remaining content
            filtered_text = self.markdown_pattern.sub("", self.text_buffer)
            if filtered_text:
                await self.put_safely({"type": "text", "content": filtered_text})
            self.text_buffer = ""

    async def on_unhandled_event(self, event_type: str, event_data: object) -> None:
        """Handle unhandled events."""
        logger.warning("Unhandled Event Type: %s, Data: %s", event_type, event_data)
