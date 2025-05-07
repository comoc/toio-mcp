#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
toio-mcp server - MCP server for toio Core Cube
"""

import asyncio
import logging
import sys
from typing import Dict, List, Optional, Any, Union

import typer
from rich.logging import RichHandler
from mcp.server.fastmcp import FastMCP
from toio.cube import ToioCoreCube
from toio.scanner import BLEScanner
from toio.cube.api.id_information import PositionId, StandardId, PositionIdMissed, StandardIdMissed

# Configure logging
logging.basicConfig(
    level=logging.CRITICAL,
    format="%(message)s",
    datefmt="[%X]",
    # handlers=[RichHandler(rich_tracebacks=True)],
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger("toio-mcp")


#################################################
# CubeManager class
#################################################

class CubeManager:
    """
    CubeManager class for managing toio Core Cubes
    """

    def __init__(self):
        """Initialize CubeManager"""
        self._cubes: Dict[str, ToioCoreCube] = {}
        self._device_map: Dict[str, str] = {}  # device_id -> cube_id

    async def scan_cubes(self, num: int = 1, timeout: float = 5.0) -> List[Dict[str, str]]:
        """
        Scan for toio Core Cubes

        Args:
            num: Number of cubes to scan for
            timeout: Scan timeout in seconds

        Returns:
            List of dictionaries containing device information
        """
        logger.info(f"Scanning for {num} toio Core Cubes (timeout: {timeout}s)")
        try:
            devices = await BLEScanner.scan(num=num, timeout=timeout)
            result = []
            for device in devices:
                device_info = {
                    "device_id": device.device.address,
                    "name": device.name,
                    "rssi": device.advertisement.rssi,
                }
                result.append(device_info)
            logger.info(f"Found {len(result)} toio Core Cubes")
            return result
        except Exception as e:
            logger.error(f"Error scanning for toio Core Cubes: {e}")
            raise

    async def connect_cube(self, device_id: str) -> str:
        """
        Connect to a toio Core Cube

        Args:
            device_id: Device ID to connect to

        Returns:
            Cube ID of the connected cube
        """
        logger.info(f"Connecting to toio Core Cube with device_id: {device_id}")
        try:
            # Check if already connected
            if device_id in self._device_map:
                cube_id = self._device_map[device_id]
                logger.info(f"Already connected to cube with ID: {cube_id}")
                return cube_id

            # Scan for the device
            devices = await BLEScanner.scan(num=10, timeout=5.0)
            target_device = None
            for device in devices:
                if device.device.address == device_id:
                    target_device = device
                    break

            if target_device is None:
                raise ValueError(f"Device with ID {device_id} not found")

            # Connect to the device
            cube = ToioCoreCube(target_device.interface)
            await cube.connect()

            # Generate a cube ID and store the cube
            cube_id = f"cube_{len(self._cubes) + 1}"
            self._cubes[cube_id] = cube
            self._device_map[device_id] = cube_id

            logger.info(f"Connected to cube with ID: {cube_id}")
            return cube_id
        except Exception as e:
            logger.error(f"Error connecting to toio Core Cube: {e}")
            raise

    async def disconnect_cube(self, cube_id: str) -> bool:
        """
        Disconnect from a toio Core Cube

        Args:
            cube_id: Cube ID to disconnect from

        Returns:
            True if disconnected successfully, False otherwise
        """
        logger.info(f"Disconnecting from cube with ID: {cube_id}")
        try:
            if cube_id not in self._cubes:
                logger.warning(f"Cube with ID {cube_id} not found")
                return False

            cube = self._cubes[cube_id]
            await cube.disconnect()

            # Remove the cube from the dictionaries
            device_id = None
            for d_id, c_id in self._device_map.items():
                if c_id == cube_id:
                    device_id = d_id
                    break

            if device_id:
                del self._device_map[device_id]
            del self._cubes[cube_id]

            logger.info(f"Disconnected from cube with ID: {cube_id}")
            return True
        except Exception as e:
            logger.error(f"Error disconnecting from toio Core Cube: {e}")
            return False

    def get_connected_cubes(self) -> List[str]:
        """
        Get a list of connected cube IDs

        Returns:
            List of connected cube IDs
        """
        return list(self._cubes.keys())

    def get_cube(self, cube_id: str) -> Optional[ToioCoreCube]:
        """
        Get a cube by ID

        Args:
            cube_id: Cube ID to get

        Returns:
            ToioCoreCube instance or None if not found
        """
        return self._cubes.get(cube_id)

    async def disconnect_all(self) -> None:
        """
        Disconnect from all connected cubes
        """
        logger.info("Disconnecting from all cubes")
        cube_ids = list(self._cubes.keys())
        for cube_id in cube_ids:
            await self.disconnect_cube(cube_id)


#################################################
# Tool functions
#################################################

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


#################################################
# ToioMCPServer class
#################################################

class ToioMCPServer:
    """
    ToioMCPServer class for providing toio Core Cube functionality via MCP
    """

    def __init__(self):
        """Initialize ToioMCPServer"""
        self.cube_manager = CubeManager()
        self.server = FastMCP(name="toio-mcp")
        # Register tools
        self._register_tools()

    def _register_tools(self):
        """Register all tools with the MCP server"""
        # Scanner tools
        self.server.add_tool(
            _scan_cubes_wrapper(self.cube_manager),
            name="scan_cubes",
            description="Scan for toio Core Cubes"
        )
        
        self.server.add_tool(
            _connect_cube_wrapper(self.cube_manager),
            name="connect_cube",
            description="Connect to a toio Core Cube"
        )
        
        self.server.add_tool(
            _disconnect_cube_wrapper(self.cube_manager),
            name="disconnect_cube",
            description="Disconnect from a toio Core Cube"
        )
        
        self.server.add_tool(
            _get_connected_cubes_wrapper(self.cube_manager),
            name="get_connected_cubes",
            description="Get a list of connected cubes"
        )
        
        # Motor tools
        self.server.add_tool(
            _motor_control_wrapper(self.cube_manager),
            name="motor_control",
            description="Control the motors of a toio Core Cube"
        )
        
        self.server.add_tool(
            _motor_stop_wrapper(self.cube_manager),
            name="motor_stop",
            description="Stop the motors of a toio Core Cube"
        )
        
        # LED tools
        self.server.add_tool(
            _set_indicator_wrapper(self.cube_manager),
            name="set_indicator",
            description="Set the LED color of a toio Core Cube"
        )
        
        # Position tools
        self.server.add_tool(
            _get_position_wrapper(self.cube_manager),
            name="get_position",
            description="Get the position of a toio Core Cube"
        )

    def start(self):
        """Start the MCP server"""
        self.server.run(transport='stdio')

    async def stop(self):
        """Stop the MCP server"""
        await self.cube_manager.disconnect_all()


#################################################
# CLI interface
#################################################

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
        logging.getLogger().setLevel(logging.CRITICAL)
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
