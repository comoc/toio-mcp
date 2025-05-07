# toio-mcp

toio-mcp is a Model Context Protocol (MCP) server for toio Core Cube. It provides a set of tools to control toio Core Cubes via the MCP protocol.

## Features

- Scan and connect to toio Core Cubes
- Control motors
- Control LED indicators (including repeated patterns and turning off)
- Get position information
- Play sounds (sound effects and MIDI notes)
- Get button state
- Get battery level
- Get sensor information (motion detection, posture angle, magnetic sensor)

## Installation

### Requirements

- Python 3.11 or higher
- [toio.py](https://github.com/toio/toio.py)
- [uv](https://docs.astral.sh/uv/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) 1.7.1 or higher

### Step 1. Install `uv`
Follow the `Getting started` guide for `uv` to install it.

### Step 2. Clone the toio-mcp repository
```bash
git clone https://github.com/comoc/toio-mcp.git
cd toio-mcp
```

### Step 3. Install dependencies
```bash
uv sync
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
- `set_repeated_indicator`: Set repeated LED indicator patterns
- `turn_off_indicator`: Turn off LED indicators

#### Position tools

- `get_position`: Get the position of a toio Core Cube

#### Sound tools

- `play_sound_effect`: Play a sound effect
- `play_midi`: Play a MIDI note
- `stop_sound`: Stop sound playback

#### Button tools

- `get_button_state`: Get the button state

#### Battery tools

- `get_battery_level`: Get the battery level

#### Sensor tools

- `get_motion_detection`: Get motion detection information
- `get_posture_angle`: Get posture angle information
- `get_magnetic_sensor`: Get magnetic sensor information

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

# toio-mcp (日本語)

toio-mcp は、toio Core Cube 用の Model Context Protocol (MCP) サーバーです。MCPプロトコルを通じてtoio Core Cubeを制御するためのツールセットを提供します。

## 特徴

- toio Core Cubeのスキャンと接続
- モーター制御
- LED制御（繰り返しパターンや消灯を含む）
- 位置情報の取得
- サウンド再生（効果音やMIDI音）
- ボタン状態の取得
- バッテリー残量の取得
- センサー情報の取得（モーション検出、姿勢角度、磁気センサー）

## インストール

### 必要条件

- Python 3.11以上
- [toio.py](https://github.com/toio/toio.py)
- [uv](https://docs.astral.sh/uv/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) 1.7.1以上

### ステップ1. uvのインストール
`uv`のGetting startedに従って`uv`インストールしてください。

### ステップ2. toio-mcpレポジトリのクローン
```bash
git clone https://github.com/comoc/toio-mcp.git
cd toio-mcp
```

### ステップ3. 依存関係のインストール
```bash
uv sync
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
- `set_repeated_indicator`: 繰り返しLEDインジケーターパターンを設定
- `turn_off_indicator`: LEDインジケーターを消灯

#### 位置情報ツール

- `get_position`: toio Core Cubeの位置情報を取得

#### サウンドツール

- `play_sound_effect`: 効果音を再生
- `play_midi`: MIDI音を再生
- `stop_sound`: サウンド再生を停止

#### ボタンツール

- `get_button_state`: ボタンの状態を取得

#### バッテリーツール

- `get_battery_level`: バッテリー残量を取得

#### センサーツール

- `get_motion_detection`: モーション検出情報を取得
- `get_posture_angle`: 姿勢角度情報を取得
- `get_magnetic_sensor`: 磁気センサー情報を取得

## ライセンス

このプロジェクトはMITライセンスの下で提供されています - 詳細はLICENSEファイルを参照してください。
