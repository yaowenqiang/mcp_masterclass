#!/usr/bin/env python3
"""
MCP Client for testing the fastmcp screenshot server.
"""

import asyncio
from fastmcp import Client

client = Client("python fastmcp_screenshot_server.py")


async def main():
    async with client:
        # List available tools
        tools = await client.list_tools()
        print("Available tools:")
        for tool in tools:
            print(f"  - {tool.name}: {tool.description}")
        print()

        # Get screen size
        print("--- get_screen_size ---")
        result = await client.call_tool("get_screen_size", {})
        print(result)
        print()

        # Capture full screen
        print("--- capture_full_screen ---")
        result = await client.call_tool(
            "capture_full_screen",
            {"save_path": "screenshots/full_screen.png"},
        )
        # Only print the text part (skip the base64 blob for readability)
        text = result[0].text if result else ""
        print(text.split("\n\n")[0])  # first line only
        print()

        # Capture a region (top-left 400x300)
        print("--- capture_region ---")
        result = await client.call_tool(
            "capture_region",
            {"left": 0, "top": 0, "width": 400, "height": 300, "save_path": "screenshots/region.png"},
        )
        text = result[0].text if result else ""
        print(text.split("\n\n")[0])
        print()

        print("All tests completed!")


if __name__ == "__main__":
    asyncio.run(main())
