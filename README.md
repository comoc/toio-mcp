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

### Step 1. Install `uv`
Follow the `Getting started` guide for `uv` to install it.

### Step 2. Clone the toio-mcp repository
```bash
git clone https://github.com/comoc/toio-mcp.git
```

### Step 3-A. Install dependencies using `uv`
```bash
cd toio-mcp
uv sync
```

### Step 3-B. Alternatively, install dependencies using `pip`  
First, follow the setup guide for `toio.py` to install it.  
Then, use `pip` to install the dependencies.
```bash
cd toio-mcp

# Install in normal mode
pip install .

# Or, install in development mode
pip install -e .
```

## Usage

### Usage with Cline or Roo Code

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

### ステップ1. uvのインストール
`uv`のGetting startedに従って`uv`インストールしてください。

### ステップ2. toio-mcpレポジトリのクローン
```bash
git clone https://github.com/comoc/toio-mcp.git
```

### ステップ3-A. uvを使った依存関係のインストール
```bash
cd toio-mcp
uv sync
```

### ステップ3-B. あるいは、pipを使った依存関係のインストール  
まず、toio.pyのセットアップガイドに従ってtoio.pyをインストールしてください。  
次に、`pip`を使って、依存関係をインストールしてください。
```bash
cd toio-mcp

# 通常モードでのインストール
pip install .

# または、開発モードでのインストール
pip install -e .
```

## 使用方法

### ClineやRoo Codeでの使用

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
