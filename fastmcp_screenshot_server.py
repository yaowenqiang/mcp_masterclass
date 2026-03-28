#!/usr/bin/env python3
"""
MCP Server for taking screenshots, built with FastMCP + pyautogui (cross-platform).
"""

import base64
import io
import time
from pathlib import Path

import pyautogui
from fastmcp import FastMCP
from fastmcp.utilities.types import Image

mcp = FastMCP("screenshot")

@mcp.tool
def capture_screen_shoot() -> Image:
    """
    Capture the current screen and return the image, use this tool whenever the user requests
    a screenshoot of their activity.
    """
    buffer = io.BytesIO()
    screen_shot = pyautogui.screenshot()
    screen_shot.convert('RGB').save(buffer, format='JPEG', quality=60, optmize=True)
    return Image(data=buffer.getvalue(), format='jpeg')

@mcp.tool
def capture_full_screen(save_path: str | None = None) -> str:
    """
    Take a screenshot of the entire screen and return it as a base64-encoded PNG.
    Optionally save it to a file on disk.

    Args:
        save_path: Optional file path to save the screenshot (e.g. "screenshots/my_screen.png").
                   If None, the screenshot is only returned as base64.
    """
    screenshot = pyautogui.screenshot()

    # Save to file if path is provided
    if save_path:
        path = Path(save_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        screenshot.save(str(path))

    # Encode to base64
    buf = io.BytesIO()
    screenshot.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode("utf-8")

    size_info = f"Resolution: {screenshot.width}x{screenshot.height}"
    saved_info = f", Saved to: {save_path}" if save_path else ""
    return f"Screenshot captured ({size_info}{saved_info}).\n\n![screenshot](data:image/png;base64,{b64})"


@mcp.tool
def capture_region(
    left: int,
    top: int,
    width: int,
    height: int,
    save_path: str | None = None,
) -> str:
    """
    Take a screenshot of a specific region of the screen.

    Args:
        left: The x-coordinate of the left edge of the region (pixels).
        top: The y-coordinate of the top edge of the region (pixels).
        width: The width of the region in pixels.
        height: The height of the region in pixels.
        save_path: Optional file path to save the screenshot (e.g. "screenshots/region.png").
                   If None, the screenshot is only returned as base64.
    """
    region = (left, top, width, height)
    screenshot = pyautogui.screenshot(region=region)

    if save_path:
        path = Path(save_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        screenshot.save(str(path))

    buf = io.BytesIO()
    screenshot.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode("utf-8")

    size_info = f"Region: ({left}, {top}, {width}, {height})"
    saved_info = f", Saved to: {save_path}" if save_path else ""
    return f"Screenshot captured ({size_info}{saved_info}).\n\n![screenshot](data:image/png;base64,{b64})"


@mcp.tool
def get_screen_size() -> str:
    """
    Get the current screen resolution (width x height).
    Useful for determining coordinates before calling capture_region.
    """
    width, height = pyautogui.size()
    return f"Screen resolution: {width}x{height}"


@mcp.tool
def get_mouse_position() -> str:
    """
    Get the current mouse cursor position (x, y).
    Useful for determining coordinates before calling capture_region.
    """
    x, y = pyautogui.position()
    return f"Mouse position: ({x}, {y})"


if __name__ == "__main__":
    mcp.run()
