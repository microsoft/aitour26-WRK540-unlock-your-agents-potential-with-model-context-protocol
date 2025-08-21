import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for managing application settings."""

    # Agent configuration
    AGENT_NAME = "Zava DIY Sales Analysis Agent"

    # Azure configuration - loaded from environment variables
    GPT_MODEL_DEPLOYMENT_NAME: str = os.environ["GPT_MODEL_DEPLOYMENT_NAME"]
    EMBEDDING_MODEL_DEPLOYMENT_NAME: str = os.environ["EMBEDDING_MODEL_DEPLOYMENT_NAME"]
    PROJECT_ENDPOINT: str = os.environ["PROJECT_ENDPOINT"]
    APPLICATIONINSIGHTS_CONNECTION_STRING: str = os.environ["APPLICATIONINSIGHTS_CONNECTION_STRING"]
    DEV_TUNNEL_URL: str = ""  # Will be set after class definition

    # Model parameters
    MAX_COMPLETION_TOKENS = 2 * 10240
    MAX_PROMPT_TOKENS = 6 * 10240

    # The LLM is used to generate the SQL queries.
    # Set the temperature and top_p low to get more deterministic results.
    TEMPERATURE = 0.1
    TOP_P = 0.1

    # MCP configuration
    MAP_MCP_FUNCTIONS: bool = os.getenv("MAP_MCP_FUNCTIONS", "true").lower() in ("true", "1", "yes")

    @staticmethod
    def _compute_dev_tunnel_url() -> str:
        """Compute the dev tunnel URL at class definition time."""
        try:
            # Look for dev_tunnel.log in the shared scripts directory
            log_file_path = Path(__file__).parent / "dev_tunnel.log"
            with log_file_path.open("r") as file:
                for line in file:
                    line = line.strip()
                    if line.startswith("Connect via browser:"):
                        # Extract URLs from the line
                        urls_part = line.split("Connect via browser:")[1].strip()
                        urls = [url.strip() for url in urls_part.split(",")]
                        if len(urls) >= 2:
                            # Use the second URL and append /mcp
                            return urls[1].rstrip("/") + "/mcp"
            return ""
        except (FileNotFoundError, Exception):
            return ""

    class Rls:
        """RLS configuration for PostgreSQL Row Level Security."""

        ZAVA_HEADOFFICE_USER_ID: str = "00000000-0000-0000-0000-000000000000"
        ZAVA_SEATTLE_USER_ID: str = "f47ac10b-58cc-4372-a567-0e02b2c3d479"
        ZAVA_BELLEVUE_USER_ID: str = "6ba7b810-9dad-11d1-80b4-00c04fd430c8"
        ZAVA_TACOMA_USER_ID: str = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
        ZAVA_SPOKANE_USER_ID: str = "d8e9f0a1-b2c3-4567-8901-234567890abc"
        ZAVA_EVERETT_USER_ID: str = "3b9ac9fa-cd5e-4b92-a7f2-b8c1d0e9f2a3"
        ZAVA_REDOND_USER_ID: str = "e7f8a9b0-c1d2-3e4f-5678-90abcdef1234"
        ZAVA_KIRKLAND_USER_ID: str = "9c8b7a65-4321-fed0-9876-543210fedcba"
        ZAVA_ONLINE_USER_ID: str = "2f4e6d8c-1a3b-5c7e-9f0a-b2d4f6e8c0a2"

    @classmethod
    def validate_required_env_vars(cls) -> None:
        """Validate that all required environment variables are set."""
        required_vars = {
            "PROJECT_ENDPOINT": cls.PROJECT_ENDPOINT,
        }

        missing_vars = [var for var, value in required_vars.items() if not value]

        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

        if not cls.GPT_MODEL_DEPLOYMENT_NAME:
            raise ValueError("GPT_MODEL_DEPLOYMENT_NAME environment variable is required")

    @classmethod
    def get_config_summary(cls) -> str:
        """Get a summary of the current configuration."""
        return f"""
Configuration Summary:
- Agent Name: {cls.AGENT_NAME}
- Model Deployment: {cls.GPT_MODEL_DEPLOYMENT_NAME or "Not Set"}
- Temperature: {cls.TEMPERATURE}
- Top P: {cls.TOP_P}
- Max Completion Tokens: {cls.MAX_COMPLETION_TOKENS}
- Max Prompt Tokens: {cls.MAX_PROMPT_TOKENS}
"""


# Set the DEV_TUNNEL_URL value after class definition
Config.DEV_TUNNEL_URL = Config._compute_dev_tunnel_url()
