"""
Scanner tools for toio-mcp
"""

import logging
from typing import Dict, List, Optional

from mcp.server.fastmcp.tools.base import Tool as MCPTool
from mcp.types import Tool, ToolsCapability

from ..cube_manager import CubeManager

logger = logging.getLogger(__name__)


def register_scanner_tools(server, cube_manager: CubeManager):
    """
    Register scanner tools with the MCP server

    Args:
        server: MCP server instance
        cube_manager: CubeManager instance
    """
    server.register_tool(
        MCPTool(
            name="scan_cubes",
            description="Scan for toio Core Cubes",
            execute=lambda **kwargs: _scan_cubes(cube_manager, **kwargs),
            arguments=[
                MCPToolArgument(
                    name="num",
                    description="Number of cubes to scan for",
                    type=MCPToolArgumentType.INTEGER,
                    required=False,
                    default=1,
                ),
                MCPToolArgument(
                    name="timeout",
                    description="Scan timeout in seconds",
                    type=MCPToolArgumentType.NUMBER,
                    required=False,
                    default=5.0,
                ),
            ],
            result_type=MCPToolResultType.OBJECT,
        )
    )

    server.register_tool(
        MCPTool(
            name="connect_cube",
            description="Connect to a toio Core Cube",
            execute=lambda **kwargs: _connect_cube(cube_manager, **kwargs),
            arguments=[
                MCPToolArgument(
                    name="device_id",
                    description="Device ID to connect to",
                    type=MCPToolArgumentType.STRING,
                    required=True,
                ),
            ],
            result_type=MCPToolResultType.OBJECT,
        )
    )

    server.register_tool(
        MCPTool(
            name="disconnect_cube",
            description="Disconnect from a toio Core Cube",
            execute=lambda **kwargs: _disconnect_cube(cube_manager, **kwargs),
            arguments=[
                MCPToolArgument(
                    name="cube_id",
                    description="Cube ID to disconnect from",
                    type=MCPToolArgumentType.STRING,
                    required=True,
                ),
            ],
            result_type=MCPToolResultType.OBJECT,
        )
    )

    server.register_tool(
        MCPTool(
            name="get_connected_cubes",
            description="Get a list of connected cubes",
            execute=lambda **kwargs: _get_connected_cubes(cube_manager, **kwargs),
            arguments=[],
            result_type=MCPToolResultType.OBJECT,
        )
    )


async def _scan_cubes(cube_manager: CubeManager, num: int = 1, timeout: float = 5.0) -> MCPToolResult:
    """
    Scan for toio Core Cubes

    Args:
        cube_manager: CubeManager instance
        num: Number of cubes to scan for
        timeout: Scan timeout in seconds

    Returns:
        MCPToolResult with list of devices
    """
    try:
        devices = await cube_manager.scan_cubes(num=num, timeout=timeout)
        return MCPToolResult(
            success=True,
            result={"devices": devices},
        )
    except Exception as e:
        logger.error(f"Error scanning for cubes: {e}")
        return MCPToolResult(
            success=False,
            error=str(e),
        )


async def _connect_cube(cube_manager: CubeManager, device_id: str) -> MCPToolResult:
    """
    Connect to a toio Core Cube

    Args:
        cube_manager: CubeManager instance
        device_id: Device ID to connect to

    Returns:
        MCPToolResult with cube ID
    """
    try:
        cube_id = await cube_manager.connect_cube(device_id)
        return MCPToolResult(
            success=True,
            result={"cube_id": cube_id},
        )
    except Exception as e:
        logger.error(f"Error connecting to cube: {e}")
        return MCPToolResult(
            success=False,
            error=str(e),
        )


async def _disconnect_cube(cube_manager: CubeManager, cube_id: str) -> MCPToolResult:
    """
    Disconnect from a toio Core Cube

    Args:
        cube_manager: CubeManager instance
        cube_id: Cube ID to disconnect from

    Returns:
        MCPToolResult with success status
    """
    try:
        success = await cube_manager.disconnect_cube(cube_id)
        return MCPToolResult(
            success=success,
            result={"disconnected": success},
        )
    except Exception as e:
        logger.error(f"Error disconnecting from cube: {e}")
        return MCPToolResult(
            success=False,
            error=str(e),
        )


async def _get_connected_cubes(cube_manager: CubeManager) -> MCPToolResult:
    """
    Get a list of connected cubes

    Args:
        cube_manager: CubeManager instance

    Returns:
        MCPToolResult with list of cube IDs
    """
    try:
        cubes = cube_manager.get_connected_cubes()
        return MCPToolResult(
            success=True,
            result={"cubes": cubes},
        )
    except Exception as e:
        logger.error(f"Error getting connected cubes: {e}")
        return MCPToolResult(
            success=False,
            error=str(e),
        )