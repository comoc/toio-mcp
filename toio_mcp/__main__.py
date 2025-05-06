"""
toio-mcp - MCP server for toio Core Cube (entry point)
"""

import asyncio
import logging
import sys
from typing import Optional

import typer
from rich.logging import RichHandler

from .server import create_server

app = typer.Typer()

# Configure logging
logging.basicConfig(
    level=logging.ERROR,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)
logger = logging.getLogger("toio_mcp")


@app.command()
def main(
    host: str = typer.Option("127.0.0.1", help="Host to bind the server to"),
    port: int = typer.Option(8000, help="Port to bind the server to"),
    log_level: str = typer.Option(
        "ERROR", help="Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)"
    ),
):
    """
    Start the toio-mcp server
    """
    # Set log level
    level = getattr(logging, log_level.upper(), None)
    if not isinstance(level, int):
        logger.warning(f"Invalid log level: {log_level}, using ERROR")
        level = logging.ERROR
    logger.setLevel(level)

    # Start the server
    logger.info(f"Starting toio-mcp server on {host}:{port}")
    server = None
    try:
        server = create_server()
        server.start()
    except KeyboardInterrupt:
        logger.info("Stopping server...")
        if server:
            asyncio.run(server.stop())
        logger.info("Server stopped")
    except Exception as e:
        logger.error(f"Error starting server: {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(app())