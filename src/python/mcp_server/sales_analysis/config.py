import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# Load environment variables from .env file in the workshop folder
workshop_dir = Path(__file__).parent.parent.parent / "workshop"
env_path = workshop_dir / ".env"
load_dotenv(dotenv_path=env_path)


class Config:
    """Configuration class for managing application settings."""

    POSTGRES_URL: str = os.getenv("POSTGRES_URL") or "postgresql://store_manager:StoreManager123!@db:5432/zava"
    APPLICATIONINSIGHTS_CONNECTION_STRING: str = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING", "")

    @classmethod
    def validate_required_env_vars(cls) -> None:
        """Validate that all required environment variables are set."""
        required_vars = {
            "POSTGRES_URL": cls.POSTGRES_URL,
        }

        missing_vars = [var for var, value in required_vars.items() if not value]

        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

        if not cls.APPLICATIONINSIGHTS_CONNECTION_STRING:
            raise ValueError("APPLICATIONINSIGHTS_CONNECTION_STRING environment variable is required")
