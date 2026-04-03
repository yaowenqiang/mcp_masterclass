from fastmcp import FastMCP

mcp = FastMCP('streamable_server')

@mcp.tool
def greeting(name: str) -> str:
    "Send a greeting"
    return f"Hi, {name}"
