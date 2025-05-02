"""
toio-mcp server - MCP server for toio Core Cube
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP

from .cube_manager import CubeManager
from .tools import register_tools

logger = logging.getLogger(__name__)


class ToioMCPServer:
    """
    ToioMCPServer class for providing toio Core Cube functionality via MCP
    """

    def __init__(self):
        """Initialize ToioMCPServer"""
        self.cube_manager = CubeManager()
        self.server = FastMCP(name="toio-mcp")
        # Register tools
        register_tools(self.server, self.cube_manager)

    def start(self):
        """Start the MCP server"""
        self.server.run(transport='stdio')

    async def stop(self):
        """Stop the MCP server"""
        await self.cube_manager.disconnect_all()


def create_server() -> ToioMCPServer:
    """Create a new ToioMCPServer instance"""
    return ToioMCPServer()