import asyncio
import json
import random
from websockets_proxy import Proxy, proxy_connect
from websockets import connect

from settings import USER_PROXY_03, list_of_headers

# this script is written with the above checker server in mind
CHECKER_URL = 'wss://eu-swarm-ws-re.betconstruct.com/'
# CHECKER_URL = 'ws://address:port'

async def main():
    # async with websockets.connect('wss://eu-swarm-ws-re.betconstruct.com/') as ws:
    # async with connect(CHECKER_URL) as ws:
    #     async for msg in ws:
    #         ip_no_proxy = msg
    #         print("Your IP:", ip_no_proxy)
    # print('.')
    # be sure to create your "Proxy" objects inside an async function
    proxy = Proxy.from_url(USER_PROXY_03)
    async with proxy_connect(
        CHECKER_URL,
        proxy=proxy,
        user_agent_header=random.choice(list_of_headers)["User-Agent"]
    ) as ws:
        await ws.send(json.dumps({"command": "request_session",
                              "params": {"language": "spa", "site_id": "735", "release_date": "20/10/2022-18:12"},
                              "rid": "17190020389361"},))
        ompetitions = await ws.recv()
        print(ompetitions)
    #     async for msg in ws:
    #         ip_with_proxy = msg
    #         print("(async with) Proxy IP", ip_with_proxy)
    # print('.')

    # ws = await proxy_connect(CHECKER_URL, proxy=proxy)
    # async for msg in ws:
    #     ip_with_proxy = msg
    #     print("(await) Proxy IP", ip_with_proxy)
    # await ws.close()
    # print('.')


if __name__ == "__main__":
    asyncio.run(main())
