from fastmcp import FastMCP
import requests


mcp = FastMCP('Crypto')

@mcp.tool
def get_cryptocurrency_price(crypto: str) -> str:
    """
    Gets the price of a cryptocurrency
    Args:
        crypto: symbol of the cryptocurrency(e.g., 'bitcoin', 'ethereum').
    """
    try:
        url = 'https://api.coingecko.com/api/v3/simple/price'
        params = {'ids': crypto.lower(), 'vs_currencies': 'usd'}

        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        price = data.get(crypto.lower()).get('usd')
        if price is not None:
            return f"The price of {crypto} is ${price} USD."
        else:
            return f"price of {crypto} not found."
    except Exception as e:
        raise Exception(f"Error fetching price for {crypto}: {e}")

