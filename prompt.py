from fastmcp import FastMCP
mcp = FastMCP('prompt')

@mcp.prompt
def get_prompt(topic:str) -> str:
    """
    Returns a prompt that will do a detailed analysis on a topic
    Args:
        topic: the topic to do research on
    """

    return f"Do a detailed analysis on the following topic: {topic}"


