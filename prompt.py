from fastmcp import FastMCP
from fastmcp.prompts import Message

mcp = FastMCP('prompt')

@mcp.prompt
def get_prompt(topic:str) -> str:
    """
    Returns a prompt that will do a detailed analysis on a topic
    Args:
        topic: the topic to do research on
    """

    return f"Do a detailed analysis on the following topic: {topic}"


@mcp.prompt
def write_detailed_historical_report(topic:str, number_of_paragraphs: int) -> str:
    """
    Writes a detailed historical report
    Args:
        topic: the topic to do research on
        number_of_paragraphs: the number of paragraphs that the main body should be
    """
    return f"""
    Create a concise research report on the history of {topic},
    The report should contain 3 sections: INTRODUCTION, MAIN, and CONCLUSION,The MAIN secion should be {number_of_paragraphs} paragraphs long, include a timeline of key events.The CONCLUSION should be bullet points format.
    """
