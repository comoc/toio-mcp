# toio-mcp

toio-mcp is a Model Context Protocol (MCP) server for toio Core Cube. It provides a set of tools to control toio Core Cubes via the MCP protocol.

## Features

- Scan and connect to toio Core Cubes
- Control motors
- Control LED indicators
- Get position information

## Installation

### Requirements

- Python 3.11 or higher
- [toio.py](https://github.com/toio/toio.py)
- [uv](https://docs.astral.sh/uv/)
- MCP SDK 1.6.0 or higher

Install toio.py according to the toio.py Setup Guide.
Install uv according to the uv Getting started.

```bash
# Clone the repository
git clone https://github.com/comoc/toio-mcp.git
cd toio-mcp

# Install dependencies (Normal mode)
pip install .

# Install dependencies (Development mode. Not required)
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

- Python 3.11以上
- [toio.py](https://github.com/toio/toio.py)
- [uv](https://docs.astral.sh/uv/)
- MCP SDK 1.6.0以上

toio.pyのセットアップガイドに従ってtoio.pyをインストールしてください。
uvのGetting startedに従ってuvインストールしてください。

```bash
# リポジトリをクローン
git clone https://github.com/comoc/toio-mcp.git
cd toio-mcp

# 依存関係をインストール(通常モード)
pip install .

# 依存関係をインストール(開発モード. 必須ではない)
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

## ライセンス

このプロジェクトはMITライセンスの下で提供されています - 詳細はLICENSEファイルを参照してください。
