# Screenshot MCP Server

一个用于在 macOS 上获取屏幕截图的 MCP (Model Context Protocol) Server。

## 功能

- **capture_screen**: 截取整个屏幕
- **capture_screen_interactive**: 交互式截图（可以选择区域或窗口）

## 安装

### 1. 安装依赖

```bash
pip install -e .
```

或使用 uv:

```bash
uv pip install -e .
```

### 2. 配置 Claude Desktop

在 Claude Desktop 的配置文件中添加此 server。

**macOS 配置文件位置**: `~/Library/Application Support/Claude/claude_desktop_config.json`

添加以下配置:

```json
{
  "mcpServers": {
    "screenshot": {
      "command": "python",
      "args": ["/Users/yaojack/Code/python_project/mcp_masterclass/screenshot_server.py"]
    }
  }
}
```

## 使用方法

### 在 Claude Desktop 中使用

重启 Claude Desktop 后，你可以直接在对话中使用：

- "请截取整个屏幕"
- "请截取屏幕的某个区域"
- "帮我截图并保存"

### 工具说明

#### capture_screen
截取整个屏幕并保存为临时文件。

参数:
- `filename` (可选): 自定义文件名（不含扩展名）

#### capture_screen_interactive
交互式截图，允许你选择区域或窗口。

参数:
- `filename` (可选): 自定义文件名（不含扩展名）

截图完成后，可以点击返回的文件路径直接打开查看。

## 系统要求

- macOS
- Python 3.10+
- mcp Python SDK

## 开发

### 运行 server

```bash
python screenshot_server.py
```

### 运行测试 Client

项目包含一个独立的测试 client，可以直接测试 server 功能：

```bash
python screenshot_client.py
```

这个 client 会：
1. 连接到 screenshot server
2. 列出所有可用的工具
3. 自动截取全屏
4. 等待 2 秒后启动交互式截图（你可以选择区域或窗口）

### 在 Claude Desktop 中使用

在 Claude Desktop 中重启应用，然后尝试使用截图功能。

## 注意事项

- 截图会保存为 PNG 格式
- 默认保存在系统临时目录
- 使用 `open <file_path>` 命令可以快速打开截图
