#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
toio-mcp server entry point
"""

import asyncio
import logging
import sys
from typing import Optional

import typer
from rich.logging import RichHandler

from toio_mcp.server import ToioMCPServer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)
logger = logging.getLogger("toio-mcp")

app = typer.Typer()


@app.command()
def main(
    host: str = typer.Option("127.0.0.1", help="Host to bind to"),
    port: int = typer.Option(8000, help="Port to bind to"),
    debug: bool = typer.Option(False, help="Enable debug logging"),
):
    """
    Start the toio-mcp server
    """
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")

    logger.info(f"Starting toio-mcp server on {host}:{port}")
    
    server = ToioMCPServer()
    
    try:
        server.start()
    except KeyboardInterrupt:
        logger.info("Stopping server...")
        asyncio.run(server.stop())
        logger.info("Server stopped")
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    app()
