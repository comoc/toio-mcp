# toio-mcp

toio-mcp is a Model Context Protocol (MCP) server for toio Core Cube. It provides a set of tools to control toio Core Cubes via the MCP protocol.

## Features

- Scan and connect to toio Core Cubes
- Control motors
- Control LED indicators
- Get position information

## Installation

### Requirements

- Python 3.10 or higher
- [toio.py](https://github.com/toio/toio.py)
- MCP SDK 1.6.0 or higher

Install toio.py according to the toio.py Setup Guide.

```bash
# Clone the repository
git clone https://github.com/yourusername/toio-mcp.git
cd toio-mcp

# Install dependencies
pip install -e .
```

## Usage

### Usage with Claude Desktop or Cline

Add the following configuration to your MCP settings file:

```json
{
  "mcpServers": {
    "toio-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "<path to toio-mcp directory>",
        "run",
        "server.py"
      ],
      "alwaysAllow": [
        "add"
      ],
      "disabled": false
    }
  }
}
```

By default, the server listens on `127.0.0.1:8000`. You can change the host and port using command-line options:

```bash
python -m toio_mcp --host 0.0.0.0 --port 8080
```

### Available tools

#### Scanner tools

- `scan_cubes`: Scan for toio Core Cubes
- `connect_cube`: Connect to a toio Core Cube
- `disconnect_cube`: Disconnect from a toio Core Cube
- `get_connected_cubes`: Get a list of connected cubes

#### Motor tools

- `motor_control`: Control the motors of a toio Core Cube
- `motor_stop`: Stop the motors of a toio Core Cube

#### LED tools

- `set_indicator`: Set the LED color of a toio Core Cube

#### Position tools

- `get_position`: Get the position of a toio Core Cube

## Examples

### Scanning for cubes

```python
from mcp.client import ClientSession

async def main():
    async with ClientSession("http://localhost:8000") as client:
        # Scan for cubes
        result = await client.call_tool("scan_cubes", {"num": 1})
        print(f"Found cubes: {result}")
        
        # Connect to the first cube
        if result["devices"]:
            device_id = result["devices"][0]["device_id"]
            result = await client.call_tool("connect_cube", {"device_id": device_id})
            cube_id = result["cube_id"]
            print(f"Connected to cube: {cube_id}")
            
            # Control the motors
            await client.call_tool("motor_control", {"cube_id": cube_id, "left": 50, "right": 50})
            await asyncio.sleep(2)
            await client.call_tool("motor_stop", {"cube_id": cube_id})
            
            # Set the LED color
            await client.call_tool("set_indicator", {"cube_id": cube_id, "r": 255, "g": 0, "b": 0})
            await asyncio.sleep(1)
            
            # Get the position
            result = await client.call_tool("get_position", {"cube_id": cube_id})
            print(f"Position: {result}")
            
            # Disconnect from the cube
            await client.call_tool("disconnect_cube", {"cube_id": cube_id})
            print(f"Disconnected from cube: {cube_id}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

# toio-mcp (日本語)

toio-mcp は、toio Core Cube 用の Model Context Protocol (MCP) サーバーです。MCPプロトコルを通じてtoio Core Cubeを制御するためのツールセットを提供します。

## 特徴

- toio Core Cubeのスキャンと接続
- モーター制御
- LED制御
- 位置情報の取得

## インストール

### 必要条件

- Python 3.10以上
- [toio.py](https://github.com/toio/toio.py)
- MCP SDK 1.6.0以上

toio.pyのセットアップガイドに従ってtoio.pyをインストールしてください。

```bash
# リポジトリをクローン
git clone https://github.com/yourusername/toio-mcp.git
cd toio-mcp

# 依存関係をインストール
pip install -e .
```

## 使用方法

### Claude DesktopやClineでの使用

MCPの設定ファイルに以下の設定を追加します：

```json
{
  "mcpServers": {
    "toio-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "<toio-mcpディレクトリへのパス>",
        "run",
        "server.py"
      ],
      "alwaysAllow": [
        "add"
      ],
      "disabled": false
    }
  }
}
```

デフォルトでは、サーバーは `127.0.0.1:8000` でリッスンします。コマンドラインオプションを使用してホストとポートを変更できます：

```bash
python -m toio_mcp --host 0.0.0.0 --port 8080
```

### 利用可能なツール

#### スキャナーツール

- `scan_cubes`: toio Core Cubeをスキャン
- `connect_cube`: toio Core Cubeに接続
- `disconnect_cube`: toio Core Cubeから切断
- `get_connected_cubes`: 接続されているCubeのリストを取得

#### モーターツール

- `motor_control`: toio Core Cubeのモーターを制御
- `motor_stop`: toio Core Cubeのモーターを停止

#### LEDツール

- `set_indicator`: toio Core CubeのLEDの色を設定

#### 位置情報ツール

- `get_position`: toio Core Cubeの位置情報を取得

## 使用例

### Cubeのスキャンと接続

```python
from mcp.client import ClientSession

async def main():
    async with ClientSession("http://localhost:8000") as client:
        # Cubeをスキャン
        result = await client.call_tool("scan_cubes", {"num": 1})
        print(f"Found cubes: {result}")
        
        # 最初のCubeに接続
        if result["devices"]:
            device_id = result["devices"][0]["device_id"]
            result = await client.call_tool("connect_cube", {"device_id": device_id})
            cube_id = result["cube_id"]
            print(f"Connected to cube: {cube_id}")
            
            # モーターを制御
            await client.call_tool("motor_control", {"cube_id": cube_id, "left": 50, "right": 50})
            await asyncio.sleep(2)
            await client.call_tool("motor_stop", {"cube_id": cube_id})
            
            # LEDの色を設定
            await client.call_tool("set_indicator", {"cube_id": cube_id, "r": 255, "g": 0, "b": 0})
            await asyncio.sleep(1)
            
            # 位置情報を取得
            result = await client.call_tool("get_position", {"cube_id": cube_id})
            print(f"Position: {result}")
            
            # Cubeから切断
            await client.call_tool("disconnect_cube", {"cube_id": cube_id})
            print(f"Disconnected from cube: {cube_id}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## ライセンス

このプロジェクトはMITライセンスの下で提供されています - 詳細はLICENSEファイルを参照してください。
