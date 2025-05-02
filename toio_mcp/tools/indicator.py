"""
LED indicator tools for toio-mcp
"""

import asyncio
import logging
from typing import Dict, List, Optional

from mcp import MCPTool, MCPToolArgument, MCPToolArgumentType, MCPToolResult, MCPToolResultType

from ..cube_manager import CubeManager

logger = logging.getLogger(__name__)


def register_indicator_tools(server, cube_manager: CubeManager):
    """
    Register LED indicator tools with the MCP server

    Args:
        server: MCP server instance
        cube_manager: CubeManager instance
    """
    server.register_tool(
        MCPTool(
            name="set_indicator",
            description="Set the LED color of a toio Core Cube",
            execute=lambda **kwargs: _set_indicator(cube_manager, **kwargs),
            arguments=[
                MCPToolArgument(
                    name="cube_id",
                    description="Cube ID to control",
                    type=MCPToolArgumentType.STRING,
                    required=True,
                ),
                MCPToolArgument(
                    name="r",
                    description="Red component (0-255)",
                    type=MCPToolArgumentType.INTEGER,
                    required=True,
                ),
                MCPToolArgument(
                    name="g",
                    description="Green component (0-255)",
                    type=MCPToolArgumentType.INTEGER,
                    required=True,
                ),
                MCPToolArgument(
                    name="b",
                    description="Blue component (0-255)",
                    type=MCPToolArgumentType.INTEGER,
                    required=True,
                ),
                MCPToolArgument(
                    name="duration",
                    description="Duration in milliseconds (0 for continuous)",
                    type=MCPToolArgumentType.INTEGER,
                    required=False,
                    default=0,
                ),
            ],
            result_type=MCPToolResultType.OBJECT,
        )
    )

    server.register_tool(
        MCPTool(
            name="set_indicator_pattern",
            description="Set the LED pattern of a toio Core Cube",
            execute=lambda **kwargs: _set_indicator_pattern(cube_manager, **kwargs),
            arguments=[
                MCPToolArgument(
                    name="cube_id",
                    description="Cube ID to control",
                    type=MCPToolArgumentType.STRING,
                    required=True,
                ),
                MCPToolArgument(
                    name="pattern",
                    description="Pattern ID (1-3)",
                    type=MCPToolArgumentType.INTEGER,
                    required=True,
                ),
                MCPToolArgument(
                    name="repeat",
                    description="Number of repetitions (0 for infinite)",
                    type=MCPToolArgumentType.INTEGER,
                    required=False,
                    default=0,
                ),
            ],
            result_type=MCPToolResultType.OBJECT,
        )
    )


async def _set_indicator(
    cube_manager: CubeManager, cube_id: str, r: int, g: int, b: int, duration: int = 0
) -> MCPToolResult:
    """
    Set the LED color of a toio Core Cube

    Args:
        cube_manager: CubeManager instance
        cube_id: Cube ID to control
        r: Red component (0-255)
        g: Green component (0-255)
        b: Blue component (0-255)
        duration: Duration in milliseconds (0 for continuous)

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

        await cube.api.indicator.set_indicator(r, g, b, duration)
        return MCPToolResult(
            success=True,
            result={"set": True},
        )
    except Exception as e:
        logger.error(f"Error setting indicator: {e}")
        return MCPToolResult(
            success=False,
            error=str(e),
        )


async def _set_indicator_pattern(
    cube_manager: CubeManager, cube_id: str, pattern: int, repeat: int = 0
) -> MCPToolResult:
    """
    Set the LED pattern of a toio Core Cube

    Args:
        cube_manager: CubeManager instance
        cube_id: Cube ID to control
        pattern: Pattern ID (1-3)
        repeat: Number of repetitions (0 for infinite)

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

        # Define some predefined patterns
        if pattern == 1:
            # Rainbow pattern
            colors = [
                (255, 0, 0),    # Red
                (255, 127, 0),  # Orange
                (255, 255, 0),  # Yellow
                (0, 255, 0),    # Green
                (0, 0, 255),    # Blue
                (75, 0, 130),   # Indigo
                (148, 0, 211),  # Violet
            ]
            duration_per_color = 200
            for _ in range(repeat if repeat > 0 else 1):
                for r, g, b in colors:
                    await cube.api.indicator.set_indicator(r, g, b, duration_per_color)
                    await asyncio.sleep(duration_per_color / 1000)
                if repeat == 0:  # Infinite loop
                    _ = 0  # Reset counter to continue loop
        elif pattern == 2:
            # Breathing pattern
            max_brightness = 255
            steps = 50
            duration_per_step = 20
            for _ in range(repeat if repeat > 0 else 1):
                # Fade in
                for i in range(steps):
                    brightness = int(max_brightness * (i / steps))
                    await cube.api.indicator.set_indicator(brightness, brightness, brightness, duration_per_step)
                    await asyncio.sleep(duration_per_step / 1000)
                # Fade out
                for i in range(steps, 0, -1):
                    brightness = int(max_brightness * (i / steps))
                    await cube.api.indicator.set_indicator(brightness, brightness, brightness, duration_per_step)
                    await asyncio.sleep(duration_per_step / 1000)
                if repeat == 0:  # Infinite loop
                    _ = 0  # Reset counter to continue loop
        elif pattern == 3:
            # Blinking pattern
            for _ in range(repeat if repeat > 0 else 1):
                await cube.api.indicator.set_indicator(255, 0, 0, 200)  # Red
                await asyncio.sleep(0.2)
                await cube.api.indicator.set_indicator(0, 0, 0, 200)    # Off
                await asyncio.sleep(0.2)
                await cube.api.indicator.set_indicator(0, 255, 0, 200)  # Green
                await asyncio.sleep(0.2)
                await cube.api.indicator.set_indicator(0, 0, 0, 200)    # Off
                await asyncio.sleep(0.2)
                await cube.api.indicator.set_indicator(0, 0, 255, 200)  # Blue
                await asyncio.sleep(0.2)
                await cube.api.indicator.set_indicator(0, 0, 0, 200)    # Off
                await asyncio.sleep(0.2)
                if repeat == 0:  # Infinite loop
                    _ = 0  # Reset counter to continue loop
        else:
            return MCPToolResult(
                success=False,
                error=f"Invalid pattern ID: {pattern}. Must be 1-3.",
            )

        return MCPToolResult(
            success=True,
            result={"set": True},
        )
    except Exception as e:
        logger.error(f"Error setting indicator pattern: {e}")
        return MCPToolResult(
            success=False,
            error=str(e),
        )