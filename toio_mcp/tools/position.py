"""
Position tools for toio-mcp
"""

import asyncio
import logging
from typing import Dict, List, Optional

from mcp import MCPTool, MCPToolArgument, MCPToolArgumentType, MCPToolResult, MCPToolResultType

from ..cube_manager import CubeManager

logger = logging.getLogger(__name__)


def register_position_tools(server, cube_manager: CubeManager):
    """
    Register position tools with the MCP server

    Args:
        server: MCP server instance
        cube_manager: CubeManager instance
    """
    server.register_tool(
        MCPTool(
            name="get_position",
            description="Get the position of a toio Core Cube",
            execute=lambda **kwargs: _get_position(cube_manager, **kwargs),
            arguments=[
                MCPToolArgument(
                    name="cube_id",
                    description="Cube ID to get position from",
                    type=MCPToolArgumentType.STRING,
                    required=True,
                ),
            ],
            result_type=MCPToolResultType.OBJECT,
        )
    )

    server.register_tool(
        MCPTool(
            name="register_position_notification",
            description="Register for position notifications from a toio Core Cube",
            execute=lambda **kwargs: _register_position_notification(cube_manager, **kwargs),
            arguments=[
                MCPToolArgument(
                    name="cube_id",
                    description="Cube ID to register for notifications",
                    type=MCPToolArgumentType.STRING,
                    required=True,
                ),
            ],
            result_type=MCPToolResultType.OBJECT,
        )
    )

    server.register_tool(
        MCPTool(
            name="unregister_position_notification",
            description="Unregister from position notifications from a toio Core Cube",
            execute=lambda **kwargs: _unregister_position_notification(cube_manager, **kwargs),
            arguments=[
                MCPToolArgument(
                    name="cube_id",
                    description="Cube ID to unregister from notifications",
                    type=MCPToolArgumentType.STRING,
                    required=True,
                ),
            ],
            result_type=MCPToolResultType.OBJECT,
        )
    )


async def _get_position(cube_manager: CubeManager, cube_id: str) -> MCPToolResult:
    """
    Get the position of a toio Core Cube

    Args:
        cube_manager: CubeManager instance
        cube_id: Cube ID to get position from

    Returns:
        MCPToolResult with position information
    """
    try:
        cube = cube_manager.get_cube(cube_id)
        if cube is None:
            return MCPToolResult(
                success=False,
                error=f"Cube with ID {cube_id} not found",
            )

        position = await cube.api.id_information.get()
        if position is None:
            return MCPToolResult(
                success=False,
                error="Failed to get position information",
            )

        result = {
            "position_id": position.position_id,
            "x": position.x,
            "y": position.y,
            "angle": position.angle,
        }
        return MCPToolResult(
            success=True,
            result=result,
        )
    except Exception as e:
        logger.error(f"Error getting position: {e}")
        return MCPToolResult(
            success=False,
            error=str(e),
        )


# Dictionary to store notification handlers
_notification_handlers = {}


def _position_notification_handler(cube_id: str, payload: bytearray):
    """
    Handler for position notifications

    Args:
        cube_id: Cube ID
        payload: Notification payload
    """
    from toio.cube import IdInformation

    id_info = IdInformation.is_my_data(payload)
    if id_info:
        logger.info(f"Position notification for cube {cube_id}: {id_info}")
        # In a real implementation, this would send the notification to clients
        # For example, through a WebSocket connection


async def _register_position_notification(cube_manager: CubeManager, cube_id: str) -> MCPToolResult:
    """
    Register for position notifications from a toio Core Cube

    Args:
        cube_manager: CubeManager instance
        cube_id: Cube ID to register for notifications

    Returns:
        MCPToolResult with success status
    """
    try:
        cube = cube_manager.get_cube(cube_id)
        if cube is None:
            return MCPToolResult(
                success=False,
                error=f"Cube with ID {cube_id} not found",
            )

        # Create a handler for this specific cube
        handler = lambda payload: _position_notification_handler(cube_id, payload)
        _notification_handlers[cube_id] = handler

        # Register the handler
        await cube.api.id_information.register_notification_handler(handler)

        return MCPToolResult(
            success=True,
            result={"registered": True},
        )
    except Exception as e:
        logger.error(f"Error registering position notification: {e}")
        return MCPToolResult(
            success=False,
            error=str(e),
        )


async def _unregister_position_notification(cube_manager: CubeManager, cube_id: str) -> MCPToolResult:
    """
    Unregister from position notifications from a toio Core Cube

    Args:
        cube_manager: CubeManager instance
        cube_id: Cube ID to unregister from notifications

    Returns:
        MCPToolResult with success status
    """
    try:
        cube = cube_manager.get_cube(cube_id)
        if cube is None:
            return MCPToolResult(
                success=False,
                error=f"Cube with ID {cube_id} not found",
            )

        # Get the handler for this cube
        handler = _notification_handlers.get(cube_id)
        if handler is None:
            return MCPToolResult(
                success=False,
                error=f"No notification handler registered for cube {cube_id}",
            )

        # Unregister the handler
        await cube.api.id_information.unregister_notification_handler(handler)
        del _notification_handlers[cube_id]

        return MCPToolResult(
            success=True,
            result={"unregistered": True},
        )
    except Exception as e:
        logger.error(f"Error unregistering position notification: {e}")
        return MCPToolResult(
            success=False,
            error=str(e),
        )