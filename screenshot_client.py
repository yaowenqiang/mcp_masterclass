#!/usr/bin/env python3
"""
MCP Client for testing the screenshot server.
"""

import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    """Main client entry point."""

    # Create server parameters for connecting to the screenshot server
    server_params = StdioServerParameters(
        command="python",
        args=["/Users/yaojack/Code/python_project/mcp_masterclass/screenshot_server.py"],
    )

    print("🔌 Connecting to Screenshot MCP Server...")

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()

            print("✅ Connected successfully!\n")

            # List available tools
            tools = await session.list_tools()
            print("📦 Available tools:")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")
            print()

            # Test 1: Capture full screen
            print("📸 Test 1: Capturing full screen...")
            result = await session.call_tool("capture_screen", {})
            print("Result:")
            for content in result.content:
                if hasattr(content, 'text'):
                    print(f"  {content.text}")
            print()

            # Wait a bit before interactive screenshot
            print("⏳ Waiting 2 seconds before interactive screenshot...\n")
            await asyncio.sleep(2)

            # Test 2: Interactive capture (commented out by default)
            print("🖼️  Test 2: Interactive capture (select a region or window)...")
            print("   Please select a region or window to capture...")
            result = await session.call_tool("capture_screen_interactive", {})
            print("Result:")
            for content in result.content:
                if hasattr(content, 'text'):
                    print(f"  {content.text}")
            print()

            print("✨ All tests completed!")


if __name__ == "__main__":
    asyncio.run(main())
