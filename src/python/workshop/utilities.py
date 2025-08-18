import logging
from pathlib import Path
from typing import List

from azure.ai.agents.aio import AgentsClient
from azure.ai.agents.models import FileInfo, ThreadMessage, VectorStore
from azure.core.exceptions import ClientAuthenticationError
from azure.identity.aio import DefaultAzureCredential
from terminal_colors import TerminalColors as tc

logger = logging.getLogger(__name__)


class Utilities:
    # property to get the relative path of shared files
    @property
    def shared_files_path(self) -> Path:
        """Get the path to the shared files directory."""
        return Path(__file__).parent.parent.parent.resolve() / "shared"

    @staticmethod
    def suppress_logs() -> None:
        """Suppress verbose Azure SDK logs to reduce noise in output."""
        for name in [
            "azure.core.pipeline.policies.http_logging_policy",
            "azure.ai.agents",
            "azure.ai.projects",
            "azure.core",
            "azure.identity",
            "uvicorn.access",
            "azure.monitor.opentelemetry.exporter.export._base",
        ]:
            logging.getLogger(name).setLevel(logging.WARNING)

    async def validate_azure_authentication(self) -> DefaultAzureCredential:
        """Validate Azure authentication before proceeding."""
        try:
            credential = DefaultAzureCredential()
            # Test credential by getting a token
            token = await credential.get_token("https://management.azure.com/.default")
            return credential
        except ClientAuthenticationError as e:
            logger.error("❌ Azure Authentication Failed")
            logger.error("🔧 To fix this issue, please run the following command:")
            logger.error("Azure CLI:")
            logger.error("   az login --use-device-code")
            logger.error("After authentication, run the program again.")
            raise e

    @property
    def get_credential(self) -> DefaultAzureCredential:
        """Get the Azure credential."""
        return DefaultAzureCredential()

    def load_instructions(self, instructions_file: str) -> str:
        """Load instructions from a file."""
        file_path = self.shared_files_path / instructions_file
        with file_path.open("r", encoding="utf-8", errors="ignore") as file:
            return file.read()

    def log_msg_green(self, msg: str) -> None:
        """Print a message in green."""
        logger.info("%s%s%s", tc.GREEN, msg, tc.RESET)

    def log_msg_purple(self, msg: str) -> None:
        """Print a message in purple."""
        logger.info("%s%s%s", tc.PURPLE, msg, tc.RESET)

    def log_token_blue(self, msg: str) -> None:
        """Print a token in blue."""
        logger.info("%s%s%s", tc.BLUE, msg, tc.RESET)

    async def get_file(self, agents_client: AgentsClient, file_id: str, attachment_name: str) -> dict:
        """Retrieve the file and save it to the local disk. Returns file info."""
        self.log_msg_green(f"Getting file with ID: {file_id}")

        attachment_part = attachment_name.split(":")[-1]
        file_name = Path(attachment_part).stem
        file_extension = Path(attachment_part).suffix
        if not file_extension:
            file_extension = ".png"
        file_name = f"{file_name}.{file_id}{file_extension}"

        folder_path = Path(self.shared_files_path) / "files"
        folder_path.mkdir(parents=True, exist_ok=True)
        file_path = folder_path / file_name
        logger.info("Saving file to: %s", file_path)

        # Save the file using a synchronous context manager
        with file_path.open("wb") as file:
            async for chunk in await agents_client.files.get_content(file_id):
                file.write(chunk)

        self.log_msg_green(f"File saved to {file_path}")

        # Return file information for web display
        return {
            "file_id": file_id,
            "file_name": file_name,
            "file_path": str(file_path),
            "relative_path": f"/files/{file_name}",
            "is_image": file_extension.lower() in [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"],
            "attachment_name": attachment_name,
        }

    async def get_files(self, message: ThreadMessage, agents_client: AgentsClient) -> List[dict]:
        """Get the image files from the message and kickoff download. Returns list of file info."""
        downloaded_files = []

        if message.image_contents:
            for index, image in enumerate(message.image_contents, start=0):
                attachment_name = (
                    "unknown"
                    if not message.file_path_annotations
                    else message.file_path_annotations[index].text + ".png"
                )
                file_info = await self.get_file(agents_client, image.image_file.file_id, attachment_name)
                downloaded_files.append(file_info)
        elif message.attachments:
            for index, attachment in enumerate(message.attachments, start=0):
                attachment_name = (
                    "unknown" if not message.file_path_annotations else message.file_path_annotations[index].text
                )
                if attachment.file_id:
                    file_info = await self.get_file(agents_client, attachment.file_id, attachment_name)
                    downloaded_files.append(file_info)

        return downloaded_files

    async def upload_file(self, agents_client: AgentsClient, file_path: Path, purpose: str = "assistants") -> FileInfo:
        """Upload a file to the project."""
        self.log_msg_purple(f"Uploading file: {file_path}")
        file_info = await agents_client.files.upload(file_path=str(file_path), purpose=purpose)
        self.log_msg_purple(f"File uploaded with ID: {file_info.id}")
        return file_info

    # type: ignore
    async def create_vector_store(
        self, agents_client: AgentsClient, files: List[str], vector_store_name: str
    ) -> VectorStore:
        """Upload a file to the project."""

        file_ids = []
        prefix = self.shared_files_path

        # Upload the files
        for file in files:
            file_path = prefix / file
            file_info = await self.upload_file(agents_client, file_path=file_path, purpose="assistants")
            file_ids.append(file_info.id)

        self.log_msg_purple("Creating the vector store")

        # Create a vector store
        vector_store = await agents_client.vector_stores.create_and_poll(file_ids=file_ids, name=vector_store_name)

        self.log_msg_purple("Vector store created and files added.")
        return vector_store
