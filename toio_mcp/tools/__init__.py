"""
toio-mcp tools package
"""

from typing import Dict, List, Optional, Any
from mcp.server.fastmcp import FastMCP
from toio.cube.api.id_information import PositionId, StandardId, PositionIdMissed, StandardIdMissed

from ..cube_manager import CubeManager

def register_tools(server: FastMCP, cube_manager: CubeManager):
    """
    Register all tools with the MCP server
    
    Args:
        server: MCP server instance
        cube_manager: CubeManager instance
    """
    # Scanner tools
    server.add_tool(
        _scan_cubes_wrapper(cube_manager),
        name="scan_cubes",
        description="Scan for toio Core Cubes"
    )
    
    server.add_tool(
        _connect_cube_wrapper(cube_manager),
        name="connect_cube",
        description="Connect to a toio Core Cube"
    )
    
    server.add_tool(
        _disconnect_cube_wrapper(cube_manager),
        name="disconnect_cube",
        description="Disconnect from a toio Core Cube"
    )
    
    server.add_tool(
        _get_connected_cubes_wrapper(cube_manager),
        name="get_connected_cubes",
        description="Get a list of connected cubes"
    )
    
    # Motor tools
    server.add_tool(
        _motor_control_wrapper(cube_manager),
        name="motor_control",
        description="Control the motors of a toio Core Cube"
    )
    
    server.add_tool(
        _motor_stop_wrapper(cube_manager),
        name="motor_stop",
        description="Stop the motors of a toio Core Cube"
    )
    
    # LED tools
    server.add_tool(
        _set_indicator_wrapper(cube_manager),
        name="set_indicator",
        description="Set the LED color of a toio Core Cube"
    )
    
    # Position tools
    server.add_tool(
        _get_position_wrapper(cube_manager),
        name="get_position",
        description="Get the position of a toio Core Cube"
    )

# Wrapper functions for tools
def _scan_cubes_wrapper(cube_manager: CubeManager):
    async def wrapper(num: int = 1, timeout: float = 5.0) -> Dict[str, Any]:
        return await _scan_cubes(cube_manager, num, timeout)
    return wrapper

def _connect_cube_wrapper(cube_manager: CubeManager):
    async def wrapper(device_id: str) -> Dict[str, Any]:
        return await _connect_cube(cube_manager, device_id)
    return wrapper

def _disconnect_cube_wrapper(cube_manager: CubeManager):
    async def wrapper(cube_id: str) -> Dict[str, Any]:
        return await _disconnect_cube(cube_manager, cube_id)
    return wrapper

def _get_connected_cubes_wrapper(cube_manager: CubeManager):
    async def wrapper() -> Dict[str, Any]:
        return await _get_connected_cubes(cube_manager)
    return wrapper

def _motor_control_wrapper(cube_manager: CubeManager):
    async def wrapper(cube_id: str, left: int, right: int, duration: int = 0) -> Dict[str, Any]:
        return await _motor_control(cube_manager, cube_id, left, right, duration)
    return wrapper

def _motor_stop_wrapper(cube_manager: CubeManager):
    async def wrapper(cube_id: str) -> Dict[str, Any]:
        return await _motor_stop(cube_manager, cube_id)
    return wrapper

def _set_indicator_wrapper(cube_manager: CubeManager):
    async def wrapper(cube_id: str, r: int, g: int, b: int, duration: int = 0) -> Dict[str, Any]:
        return await _set_indicator(cube_manager, cube_id, r, g, b, duration)
    return wrapper

def _get_position_wrapper(cube_manager: CubeManager):
    async def wrapper(cube_id: str) -> Dict[str, Any]:
        return await _get_position(cube_manager, cube_id)
    return wrapper

async def _scan_cubes(cube_manager: CubeManager, num: int = 1, timeout: float = 5.0):
    """
    Scan for toio Core Cubes

    Args:
        cube_manager: CubeManager instance
        num: Number of cubes to scan for
        timeout: Scan timeout in seconds

    Returns:
        Dict with list of devices
    """
    try:
        devices = await cube_manager.scan_cubes(num=num, timeout=timeout)
        return {"devices": devices}
    except Exception as e:
        return {"error": str(e)}

async def _connect_cube(cube_manager: CubeManager, device_id: str):
    """
    Connect to a toio Core Cube

    Args:
        cube_manager: CubeManager instance
        device_id: Device ID to connect to

    Returns:
        Dict with cube ID
    """
    try:
        cube_id = await cube_manager.connect_cube(device_id)
        return {"cube_id": cube_id}
    except Exception as e:
        return {"error": str(e)}

async def _disconnect_cube(cube_manager: CubeManager, cube_id: str):
    """
    Disconnect from a toio Core Cube

    Args:
        cube_manager: CubeManager instance
        cube_id: Cube ID to disconnect from

    Returns:
        Dict with success status
    """
    try:
        success = await cube_manager.disconnect_cube(cube_id)
        return {"disconnected": success}
    except Exception as e:
        return {"error": str(e)}

async def _get_connected_cubes(cube_manager: CubeManager):
    """
    Get a list of connected cubes

    Args:
        cube_manager: CubeManager instance

    Returns:
        Dict with list of cube IDs
    """
    try:
        cubes = cube_manager.get_connected_cubes()
        return {"cubes": cubes}
    except Exception as e:
        return {"error": str(e)}

async def _motor_control(cube_manager: CubeManager, cube_id: str, left: int, right: int, duration: int = 0):
    """
    Control the motors of a toio Core Cube

    Args:
        cube_manager: CubeManager instance
        cube_id: Cube ID to control
        left: Left motor speed (-100 to 100)
        right: Right motor speed (-100 to 100)
        duration: Duration in milliseconds (0 for continuous)

    Returns:
        Dict with success status
    """
    try:
        cube = cube_manager.get_cube(cube_id)
        if cube is None:
            return {"error": f"Cube with ID {cube_id} not found"}

        await cube.api.motor.motor_control(left, right, duration)
        return {"controlled": True}
    except Exception as e:
        return {"error": str(e)}

async def _motor_stop(cube_manager: CubeManager, cube_id: str):
    """
    Stop the motors of a toio Core Cube

    Args:
        cube_manager: CubeManager instance
        cube_id: Cube ID to stop

    Returns:
        Dict with success status
    """
    try:
        cube = cube_manager.get_cube(cube_id)
        if cube is None:
            return {"error": f"Cube with ID {cube_id} not found"}

        await cube.api.motor.motor_control(0, 0)
        return {"stopped": True}
    except Exception as e:
        return {"error": str(e)}

async def _set_indicator(cube_manager: CubeManager, cube_id: str, r: int, g: int, b: int, duration: int = 0):
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
        Dict with success status
    """
    try:
        cube = cube_manager.get_cube(cube_id)
        if cube is None:
            return {"error": f"Cube with ID {cube_id} not found"}

        from toio.cube.api.indicator import Color, IndicatorParam
        color = Color(r, g, b)
        param = IndicatorParam(duration_ms=duration, color=color)
        await cube.api.indicator.turn_on(param)
        return {"set": True}
    except Exception as e:
        return {"error": str(e)}

async def _get_position(cube_manager: CubeManager, cube_id: str):
    """
    Get the position of a toio Core Cube

    Args:
        cube_manager: CubeManager instance
        cube_id: Cube ID to get position from

    Returns:
        Dict with position information
    """
    try:
        cube = cube_manager.get_cube(cube_id)
        if cube is None:
            return {"error": f"Cube with ID {cube_id} not found"}

        position = await cube.api.id_information.read()
        if position is None:
            return {"error": "Failed to get position information"}

        result = {}
        
        # Handle different types of position information
        if isinstance(position, PositionId):
            result = {
                "type": "position_id",
                "center_x": position.center.point.x,
                "center_y": position.center.point.y,
                "center_angle": position.center.angle,
                "sensor_x": position.sensor.point.x,
                "sensor_y": position.sensor.point.y,
                "sensor_angle": position.sensor.angle,
            }
        elif isinstance(position, StandardId):
            result = {
                "type": "standard_id",
                "value": position.value,
                "angle": position.angle,
            }
        elif isinstance(position, PositionIdMissed):
            result = {
                "type": "position_id_missed",
            }
        elif isinstance(position, StandardIdMissed):
            result = {
                "type": "standard_id_missed",
            }
        return result
    except Exception as e:
        return {"error": str(e)}