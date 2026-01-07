"""
Logging configuration for the application.
"""

import logging
import sys
from typing import Any, Dict

from app.config.settings import get_settings


def setup_logging() -> None:
    """Configure logging for the application."""
    settings = get_settings()

    # Define log format
    log_format = "%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    # Get log level from settings
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)

    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
    )

    # Set specific loggers
    loggers_config: Dict[str, Any] = {
        "uvicorn": {"level": log_level},
        "uvicorn.access": {"level": log_level},
        "uvicorn.error": {"level": log_level},
        "sqlalchemy.engine": {
            "level": logging.WARNING if not settings.app_debug else logging.INFO
        },
        "httpx": {"level": logging.WARNING},
        "httpcore": {"level": logging.WARNING},
        "langchain": {"level": logging.WARNING},
        "langgraph": {"level": logging.INFO},
    }

    for logger_name, config in loggers_config.items():
        logger = logging.getLogger(logger_name)
        logger.setLevel(config["level"])


def get_logger(name: str) -> logging.Logger:
    """Get a logger with the specified name."""
    return logging.getLogger(name)
