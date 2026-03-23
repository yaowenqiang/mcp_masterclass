# Screenshot MCP Server 使用指南

本文档详细介绍如何使用 Screenshot MCP Server。

## 目录

- [简介](#简介)
- [快速开始](#快速开始)
- [详细配置](#详细配置)
- [使用示例](#使用示例)
- [API 参考](#api-参考)
- [故障排除](#故障排除)
- [高级用法](#高级用法)

## 简介

Screenshot MCP Server 是一个基于 MCP (Model Context Protocol) 的服务器，允许 AI 助手通过简单的命令在 macOS 上截取屏幕截图。

### 主要特性

- 全屏截图
- 交互式区域/窗口截图
- PNG 格式输出
- 临时文件自动管理
- 与 Claude Desktop 无缝集成

### 系统要求

- macOS 10.15+
- Python 3.10 或更高版本
- Claude Desktop (可选，用于集成使用)

## 快速开始

### 步骤 1: 安装依赖

```bash
# 进入项目目录
cd /Users/yaojack/Code/python_project/mcp_masterclass

# 安装项目依赖
pip install -e .
```

或使用 uv (更快的包管理器):

```bash
uv pip install -e .
```

### 步骤 2: 测试 Server

使用独立的测试 client 验证 server 是否正常工作：

```bash
python screenshot_client.py
```

预期输出：

```
🔌 Connecting to Screenshot MCP Server...
✅ Connected successfully!

📦 Available tools:
  - capture_screen: Take a screenshot of the entire screen (macOS only)
  - capture_screen_interactive: Take an interactive screenshot (macOS only). Allows you to select a region or window.

📸 Test 1: Capturing full screen...
Result:
  Screenshot saved to: /var/folders/.../tmpXXX.png
  File size: 1234567 bytes

  You can open it with: open /var/folders/.../tmpXXX.png

⏳ Waiting 2 seconds before interactive screenshot...

🖼️  Test 2: Interactive capture (select a region or window)...
   Please select a region or window to capture...
Result:
  Screenshot saved to: /var/folders/.../tmpXXX.png
  File size: 234567 bytes

  You can open it with: open /var/folders/.../tmpXXX.png

✨ All tests completed!
```

### 步骤 3: 配置 Claude Desktop (可选)

如果你想在 Claude Desktop 中使用此 server，需要配置客户端。

#### 3.1 找到配置文件

Claude Desktop 的配置文件位于：

```
~/Library/Application Support/Claude/claude_desktop_config.json
```

#### 3.2 编辑配置文件

如果配置文件不存在，创建它。如果存在，添加以下内容：

```json
{
  "mcpServers": {
    "screenshot": {
      "command": "python",
      "args": [
        "/Users/yaojack/Code/python_project/mcp_masterclass/screenshot_server.py"
      ]
    }
  }
}
```

注意：如果你的项目路径不同，请相应调整 `args` 中的路径。

#### 3.3 重启 Claude Desktop

关闭并重新打开 Claude Desktop 应用。

## 详细配置

### 配置选项

Claude Desktop 配置文件支持多个 MCP servers。如果你已经配置了其他 servers，只需添加新的 server 条目：

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/allowed/path"]
    },
    "screenshot": {
      "command": "python",
      "args": [
        "/Users/yaojack/Code/python_project/mcp_masterclass/screenshot_server.py"
      ]
    }
  }
}
```

### 环境变量

如果你的 Python 解释器不在默认路径中，可以指定完整路径：

```json
{
  "mcpServers": {
    "screenshot": {
      "command": "/usr/local/bin/python3",
      "args": [
        "/Users/yaojack/Code/python_project/mcp_masterclass/screenshot_server.py"
      ]
    }
  }
}
```

### 虚拟环境

如果你使用虚拟环境，指定虚拟环境中的 Python：

```json
{
  "mcpServers": {
    "screenshot": {
      "command": "/path/to/venv/bin/python",
      "args": [
        "/Users/yaojack/Code/python_project/mcp_masterclass/screenshot_server.py"
      ]
    }
  }
}
```

## 使用示例

### 在 Claude Desktop 中使用

配置完成后，在 Claude Desktop 对话中直接使用自然语言：

#### 示例 1: 截取全屏

```
你：请帮我截取全屏

Claude：好的，我来截取全屏...
[调用 capture_screen 工具]
截图已保存到：/var/folders/.../tmpXXX.png
```

#### 示例 2: 交互式截图

```
你：我想截取屏幕上的某个区域

Claude：好的，我使用交互式截图工具，请选择要截取的区域...
[调用 capture_screen_interactive 工具]
截图已保存
```

#### 示例 3: 自定义文件名

```
你：帮我截图并保存为 "my_screenshot"

Claude：好的，我来截取全屏并保存...
[调用 capture_screen 工具，传入 filename="my_screenshot"]
```

### 使用独立 Client

你也可以在自己的 Python 项目中作为 client 使用：

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def take_screenshot():
    server_params = StdioServerParameters(
        command="python",
        args=["/path/to/screenshot_server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # 截取全屏
            result = await session.call_tool("capture_screen", {})

            # 打印结果
            for content in result.content:
                print(content.text)

# 运行
asyncio.run(take_screenshot())
```

## API 参考

### capture_screen

截取整个屏幕。

**参数：**

```json
{
  "filename": "string (optional)" // 自定义文件名，不含扩展名
}
```

**返回：**

```
Screenshot saved to: /var/folders/.../tmpXXX.png
File size: 1234567 bytes

You can open it with: open /var/folders/.../tmpXXX.png
```

**示例调用：**

```python
# 不带参数
await session.call_tool("capture_screen", {})

# 带自定义文件名
await session.call_tool("capture_screen", {"filename": "my_screen"})
```

### capture_screen_interactive

交互式截图，允许选择区域或窗口。

**参数：**

```json
{
  "filename": "string (optional)" // 自定义文件名，不含扩展名
}
```

**返回：**

```
Screenshot saved to: /var/folders/.../tmpXXX.png
File size: 123456 bytes

You can open it with: open /var/folders/.../tmpXXX.png
```

**行为：**

1. 鼠标光标变为十字准线
2. 用户可以：
   - 点击并拖动以选择矩形区域
   - 按 Space 然后点击窗口来截取整个窗口
   - 按 Escape 取消截图
3. 选定后自动截图并保存

**示例调用：**

```python
await session.call_tool("capture_screen_interactive", {})
```

## 故障排除

### 问题 1: "ModuleNotFoundError: No module named 'mcp'"

**原因：** MCP SDK 未安装。

**解决方案：**

```bash
pip install mcp
```

或重新安装项目：

```bash
pip install -e .
```

### 问题 2: Claude Desktop 中看不到工具

**原因：**
- 配置文件路径错误
- 配置文件格式不正确
- Python 路径不正确
- Server 启动失败

**解决方案：**

1. 检查配置文件路径：
```bash
ls ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

2. 验证 Python 路径：
```bash
which python
```

3. 手动测试 server：
```bash
python screenshot_server.py
```

4. 查看 Claude Desktop 日志：
```bash
~/Library/Logs/Claude/
```

### 问题 3: 截图失败

**原因：** macOS 权限问题。

**解决方案：**

1. 打开"系统设置" > "隐私与安全性"
2. 找到"屏幕录制"
3. 确保你的终端应用或 Claude Desktop 有权限

### 问题 4: "command not found: python"

**原因：** Python 不在 PATH 中或命令名称不同。

**解决方案：**

1. 检查 Python 命令：
```bash
# 尝试这些命令
python3 --version
python --version
which python3
```

2. 在配置文件中使用完整路径或正确的命令名：
```json
{
  "mcpServers": {
    "screenshot": {
      "command": "python3",  // 或 /usr/local/bin/python3
      "args": [...]
    }
  }
}
```

### 问题 5: 交互式截图无响应

**原因：** 某些环境下交互式截图需要图形界面。

**解决方案：**
- 确保在图形界面环境下运行（不在纯 SSH 会话中）
- 使用 `capture_screen` 代替交互式模式

## 高级用法

### 自定义截图保存位置

修改 server 代码中的保存逻辑：

```python
# 在 screenshot_server.py 中修改
save_path = "/Users/yourname/Pictures/screenshots/"
os.makedirs(save_path, exist_ok=True)

tmp_path = os.path.join(save_path, f"{filename}.png")
```

### 批量截图

使用 client 循环截图：

```python
async def batch_screenshot(count=5, interval=2):
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            for i in range(count):
                result = await session.call_tool("capture_screen", {
                    "filename": f"batch_screenshot_{i+1}"
                })
                print(f"Screenshot {i+1}/{count} taken")
                await asyncio.sleep(interval)
```

### 与其他 MCP Servers 集成

结合其他 servers 使用，例如文件系统 server：

```json
{
  "mcpServers": {
    "screenshot": {
      "command": "python",
      "args": ["/path/to/screenshot_server.py"]
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/yourname/Pictures"]
    }
  }
}
```

这样你可以在截图后直接操作文件。

## 最佳实践

1. **定期清理临时文件**：截图保存在临时目录，定期清理
2. **使用有意义的文件名**：在批量操作时使用描述性文件名
3. **处理大文件**：高分辨率截图可能很大，注意磁盘空间
4. **权限管理**：确保 Python 解释器和 Claude Desktop 有必要的屏幕权限

## 更多资源

- [MCP 协议规范](https://modelcontextprotocol.io/)
- [Claude Desktop 文档](https://claude.ai/desktop)
- [macOS screencapture 手册](https://ss64.com/osx/screencapture.html)

## 支持

如有问题，请检查：
1. 本文档的故障排除部分
2. 项目 README.md
3. Claude Desktop 日志文件
