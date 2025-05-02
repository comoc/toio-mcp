"""
Motor control tools for toio-mcp
"""

import logging
from typing import Dict, Optional

from mcp import MCPTool, MCPToolArgument, MCPToolArgumentType, MCPToolResult, MCPToolResultType

from ..cube_manager import CubeManager

logger = logging.getLogger(__name__)


def register_motor_tools(server, cube_manager: CubeManager):
    """
    Register motor control tools with the MCP server

    Args:
        server: MCP server instance
        cube_manager: CubeManager instance
    """
    server.register_tool(
        MCPTool(
            name="motor_control",
            description="Control the motors of a toio Core Cube",
            execute=lambda **kwargs: _motor_control(cube_manager, **kwargs),
            arguments=[
                MCPToolArgument(
                    name="cube_id",
                    description="Cube ID to control",
                    type=MCPToolArgumentType.STRING,
                    required=True,
                ),
                MCPToolArgument(
                    name="left",
                    description="Left motor speed (-100 to 100)",
                    type=MCPToolArgumentType.INTEGER,
                    required=True,
                ),
                MCPToolArgument(
                    name="right",
                    description="Right motor speed (-100 to 100)",
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
            name="motor_stop",
            description="Stop the motors of a toio Core Cube",
            execute=lambda **kwargs: _motor_stop(cube_manager, **kwargs),
            arguments=[
                MCPToolArgument(
                    name="cube_id",
                    description="Cube ID to stop",
                    type=MCPToolArgumentType.STRING,
                    required=True,
                ),
            ],
            result_type=MCPToolResultType.OBJECT,
        )
    )

    server.register_tool(
        MCPTool(
            name="motor_control_target",
            description="Move a toio Core Cube to a target position",
            execute=lambda **kwargs: _motor_control_target(cube_manager, **kwargs),
            arguments=[
                MCPToolArgument(
                    name="cube_id",
                    description="Cube ID to control",
                    type=MCPToolArgumentType.STRING,
                    required=True,
                ),
                MCPToolArgument(
                    name="x",
                    description="Target X coordinate",
                    type=MCPToolArgumentType.INTEGER,
                    required=True,
                ),
                MCPToolArgument(
                    name="y",
                    description="Target Y coordinate",
                    type=MCPToolArgumentType.INTEGER,
                    required=True,
                ),
                MCPToolArgument(
                    name="angle",
                    description="Target angle in degrees",
                    type=MCPToolArgumentType.INTEGER,
                    required=False,
                    default=0,
                ),
                MCPToolArgument(
                    name="speed",
                    description="Movement speed (1-255)",
                    type=MCPToolArgumentType.INTEGER,
                    required=False,
                    default=100,
                ),
                MCPToolArgument(
                    name="timeout",
                    description="Timeout in milliseconds",
                    type=MCPToolArgumentType.INTEGER,
                    required=False,
                    default=5000,
                ),
            ],
            result_type=MCPToolResultType.OBJECT,
        )
    )


async def _motor_control(
    cube_manager: CubeManager, cube_id: str, left: int, right: int, duration: int = 0
) -> MCPToolResult:
    """
    Control the motors of a toio Core Cube

    Args:
        cube_manager: CubeManager instance
        cube_id: Cube ID to control
        left: Left motor speed (-100 to 100)
        right: Right motor speed (-100 to 100)
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

        await cube.api.motor.motor_control(left, right, duration)
        return MCPToolResult(
            success=True,
            result={"controlled": True},
        )
    except Exception as e:
        logger.error(f"Error controlling motors: {e}")
        return MCPToolResult(
            success=False,
            error=str(e),
        )


async def _motor_stop(cube_manager: CubeManager, cube_id: str) -> MCPToolResult:
    """
    Stop the motors of a toio Core Cube

    Args:
        cube_manager: CubeManager instance
        cube_id: Cube ID to stop

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

        await cube.api.motor.motor_control(0, 0)
        return MCPToolResult(
            success=True,
            result={"stopped": True},
        )
    except Exception as e:
        logger.error(f"Error stopping motors: {e}")
        return MCPToolResult(
            success=False,
            error=str(e),
        )


async def _motor_control_target(
    cube_manager: CubeManager,
    cube_id: str,
    x: int,
    y: int,
    angle: int = 0,
    speed: int = 100,
    timeout: int = 5000,
) -> MCPToolResult:
    """
    Move a toio Core Cube to a target position

    Args:
        cube_manager: CubeManager instance
        cube_id: Cube ID to control
        x: Target X coordinate
        y: Target Y coordinate
        angle: Target angle in degrees
        speed: Movement speed (1-255)
        timeout: Timeout in milliseconds

    Returns:
        MCPToolResult with success status
    """
    try:
        from toio.cube import (
            CubeLocation,
            MovementType,
            Point,
            RotationOption,
            Speed,
            SpeedChangeType,
            TargetPosition,
        )

        cube = cube_manager.get_cube(cube_id)
        if cube is None:
            return MCPToolResult(
                success=False,
                error=f"Cube with ID {cube_id} not found",
            )

        await cube.api.motor.motor_control_target(
            timeout=timeout,
            movement_type=MovementType.Linear,
            speed=Speed(
                max=speed, speed_change_type=SpeedChangeType.AccelerationAndDeceleration
            ),
            target=TargetPosition(
                cube_location=CubeLocation(point=Point(x=x, y=y), angle=angle),
                rotation_option=RotationOption.AbsoluteOptimal,
            ),
        )
        return MCPToolResult(
            success=True,
            result={"controlled": True},
        )
    except Exception as e:
        logger.error(f"Error controlling motors to target: {e}")
        return MCPToolResult(
            success=False,
            error=str(e),
        )