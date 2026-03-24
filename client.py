from mcp import clientSession, StdioServerparemeters, types
from mcp.client.stdio import stdio_client
import asyncio
import traceback

server_params = StdioServerparemeters(
    command='uv',
    args=['run', 'weather.py'],
)

async def run():
    try:
        print('starting stdio_client')
        async with stdio_client(server_params) as (read, write):
            print('client connected, creating sesion...')
            async with clientSession(read, write) as sesion:
                print('Initializing session...')
                await session.initialize()

                print('list tools...')
                tools = await session.list_tools()
                print('Avaiable tools:', tools)

                print('Calling tools')
                result = await session.call_tool('get_weather', arguments={'location':'california'})
                print('Tool result', result)
    except Exception as e:
        print('An error occurred:')
        traceback.print_exc()

if __name__ == '__main__':
    asyncio.run(run())
