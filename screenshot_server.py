#!/usr/bin/env python3
"""
MCP Server for taking screenshots on macOS.
"""

import asyncio
import subprocess
import tempfile
import os
from pathlib import Path
from typing import Any
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)

# Create server instance
server = Server("screenshot-server")


@server.list_resources()
async def handle_list_resources() -> list[Resource]:
    """List available resources."""
    return []


@server.read_resource()
async def handle_read_resource(uri: str) -> str:
    """Read a specific resource."""
    return ""


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="capture_screen",
            description="Take a screenshot of the entire screen (macOS only)",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Optional filename to save the screenshot (without extension). If not provided, a temporary name will be used.",
                    },
                },
            },
        ),
        Tool(
            name="capture_screen_interactive",
            description="Take an interactive screenshot (macOS only). Allows you to select a region or window.",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Optional filename to save the screenshot (without extension). If not provided, a temporary name will be used.",
                    },
                },
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any] | None) -> list[TextContent | ImageContent | EmbeddedResource]:
    """Handle tool calls."""
    if name == "capture_screen":
        return await capture_screen(arguments or {})
    elif name == "capture_screen_interactive":
        return await capture_screen_interactive(arguments or {})
    else:
        raise ValueError(f"Unknown tool: {name}")


async def capture_screen(arguments: dict[str, Any]) -> list[TextContent]:
    """Capture the entire screen."""
    filename = arguments.get("filename", "screenshot")

    # Create temp file
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
        tmp_path = tmp_file.name

    try:
        # Use macOS screencapture command
        result = subprocess.run(
            ["screencapture", "-x", tmp_path],
            capture_output=True,
            text=True,
            check=True,
        )

        # Get file size
        file_size = os.path.getsize(tmp_path)

        return [
            TextContent(
                type="text",
                text=f"Screenshot saved to: {tmp_path}\nFile size: {file_size} bytes\n\nYou can open it with: open {tmp_path}"
            )
        ]
    except subprocess.CalledProcessError as e:
        return [TextContent(type="text", text=f"Error taking screenshot: {e.stderr}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Unexpected error: {str(e)}")]


async def capture_screen_interactive(arguments: dict[str, Any]) -> list[TextContent]:
    """Capture screen with interactive selection."""
    filename = arguments.get("filename", "screenshot")

    # Create temp file
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
        tmp_path = tmp_file.name

    try:
        # Use macOS screencapture command with interactive mode
        # -i flag allows interactive region/window selection
        result = subprocess.run(
            ["screencapture", "-i", tmp_path],
            capture_output=True,
            text=True,
            check=True,
        )

        # Check if screenshot was actually taken (user might have cancelled)
        if not os.path.exists(tmp_path) or os.path.getsize(tmp_path) == 0:
            return [TextContent(type="text", text="Screenshot was cancelled or failed.")]

        file_size = os.path.getsize(tmp_path)

        return [
            TextContent(
                type="text",
                text=f"Screenshot saved to: {tmp_path}\nFile size: {file_size} bytes\n\nYou can open it with: open {tmp_path}"
            )
        ]
    except subprocess.CalledProcessError as e:
        return [TextContent(type="text", text=f"Error taking screenshot: {e.stderr}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Unexpected error: {str(e)}")]


async def main():
    """Main entry point for the server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="screenshot-server",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
