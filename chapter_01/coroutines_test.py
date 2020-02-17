import asyncio
import time

"""
要调用协程，asyncio有三种主要机制：
1. asyncio.run() 函数用来运行最高层级的入口点“main()” 函数
2. 等待一个协程
3. asyncio.create_task() 函数用来并发运行作为 asyncio 任务的多个协程 

"""


# 1. asyncio.run()  函数用来运行最高层级的入口点“main()” 函数
# async def main():
#     print("hello")
#     await asyncio.sleep(1)
#     print("world")
#
#
# asyncio.run(main())

# 2. 等待一个协程

# async def say_after(delay, what):
#     await asyncio.sleep(delay)
#     print(what)
#
#
# async def main():
#     print(f"started at {time.strftime('%X')}")
#     await say_after(1, "hello")
#     await say_after(2, "world")
#
#     print(f"finished at {time.strftime('%X')}")
#
#
# asyncio.run(main())

# 3. asyncio.create_task()  并发运行协程

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


async def main():
    task1 = asyncio.create_task(say_after(1, "hello"))
    task2 = asyncio.create_task(say_after(2, "world"))
    task3 = asyncio.get_running_loop().create_task(say_after(3, "hello, python"))
    task4 = asyncio.get_event_loop().create_task(say_after(4, "asdf qwer"))

    print(f"started at {time.strftime('%X')}")
    await task1
    await task2
    await task3
    await task4
    print(f"finished at {time.strftime('%X')}")


asyncio.run(main())
