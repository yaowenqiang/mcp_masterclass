from fastmcp import Client
import asyncio
config = {
    "mcpServers": {
        "airbnb": {
              "command": "npx",
              "args": [
                "-y",
                "@openbnb/mcp-server-airbnb",
                "--ignore-robots-txt"
              ]
        }
    }
}

client = Client(config)

async def run():
    async with client:
        # Tools are prefixed with server names
        tools = await client.list_tools()
        print(tools)
        result = await client.call_tool('airbnb_search', arguments={'location':'London'})
        print(result)
    

if __name__ == '__main__':
    asyncio.run(run())
