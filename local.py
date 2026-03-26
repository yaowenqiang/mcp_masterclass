from fastmcp import FastMCP

mcp = FastMCP('LocalNotes')

@mcp.tool
def add_note_to_file(content: str) -> str:
    """
    Appends the given content to a user's local.txt file.
    Args:
        content (str): The text to appended.
    """

    file_name = 'note.txt'

    try:
        with open(file_name, 'a', encoding='utf-8') as file:
            file.write(content + '\n')
            return f"Content append to {file_name}"
    except Exception as e:
        return f"Error appending to file: {file_name} {str(e)}"

@mcp.tool
def read_notes() -> str:
    """
    Reads and returns the contents of the user's local notes.txt file.
    """

    file_name = 'note.txt'

    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            notes = file.read()
            return notes if notes else "No notes found."
    except Exception as e:
        return f"Error reading file: {file_name} {str(e)}"
