from fastmcp import FastMCP

mcp = FastMCP('recources')

@mcp.resource('inventory://overview')
def get_inventory_overview() -> str:
    """
    Returns overview of inventory
    """

    # Sample inventory overview

    overview = """
    Inventory Overview:
    - Coffee
    - Tea
    - Cookies
    """

    return overview.strip()
