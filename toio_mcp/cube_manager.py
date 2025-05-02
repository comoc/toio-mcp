"""
CubeManager - toio Core Cube management class
"""

import asyncio
import logging
from typing import Dict, List, Optional, Union

from toio.cube import ToioCoreCube
from toio.scanner import BLEScanner

logger = logging.getLogger(__name__)


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