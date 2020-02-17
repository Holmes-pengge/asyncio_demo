import asyncio
import logging

PYTHONASYNCIODEBUG = 1


async def bug():
    raise Exception("not consumed")


async def main():
    # print("hello...")
    # await asyncio.sleep(2)
    # print("world...")
    # logging.getLogger("asyncio").setLevel(logging.WARNING)
    asyncio.create_task(bug())


asyncio.run(main(), debug=True)

# loop = asyncio.get_event_loop()
# loop.call_soon_threadsafe()
# asyncio.run_coroutine_threadsafe()

