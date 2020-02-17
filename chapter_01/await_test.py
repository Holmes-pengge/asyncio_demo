import asyncio
import concurrent.futures
import time

"""
1. 可等待对象：
如果一个对象可以在 await语句中使用，那么它就是  可等待对象。
许多 asyncio 的 API 都被设计成 接受 可等待对象。
2. 可等待对象的三种主要类型：
2.1 协程
协程函数：定义形式为 async def;
协程对象: 调用协程函数 所返回的对象;
2.2 任务
2.3 Future
"""


##########################################################################
# 1. 协程 Python的协程属于 可等待对象，因此可以在其它协程中 被等待
# async def nested():
#     return 42
#
#
# async def main():
#     nested()  # 会报错 RuntimeWarning: Enable tracemalloc to get the object allocation traceback
#     print(await nested())  # print 42
#
# asyncio.run(main())
##########################################################################

##########################################################################

# 2. 任务： 被用来设置日程，以便执行协程
# 如果 一个【协程】被 asyncio.create_task() 等函数打包成一个 【任务】，该协程将自动排入日程 准备立即运行


# async def nested():
#     return 42
#
#
# async def main():
#     task = asyncio.create_task(nested())  # nested() 这个协程被 asyncio.create_task（）打包成了 task
#     await task
#
#
# asyncio.run(main())


##########################################################################

##########################################################################
# 3. Future 对象
# Future 是一种特殊的 低层级可等待对象， 表示一个 异步操作 的最终结果
# 当一个 Future 对象被等待，意味着协程将保持等待 直到该 Future 对象在其它地方执行完毕。
# 在 asyncio 中需要 Future 对象 以便允许通过 async/await 使用基于回调的代码
# 通常情况下，没有必要在应用层级的代码中 创建 Future对象。
# Future 对象有时会由 库和 某些 asyncio API 暴露给用户，用作可等待对象

# async def main():
#     await function_that_returns_a_future_object()
#
#     await asyncio.gather(function_that_returns_a_future_object(), some_python_coroutine())

def blocking_io():
    with open(r'D:\work\code\workcode\ebay_spider\exception.log', 'rb') as fp:
        return fp.read(100)


def cpu_bound():
    return sum(i * i for i in range(10 ** 7))


async def main():
    loop = asyncio.get_running_loop()
    # options:
    # 1. run in the default loop's executor:
    result = await loop.run_in_executor(None, blocking_io)
    print("default thread pool", result)

    # 2. run in a custom thread pool
    with concurrent.futures.ThreadPoolExecutor() as pool1:
        result = await loop.run_in_executor(pool1, blocking_io)
        print("custom thread pool", result)

    # 3. run in a custom process pool:
    with concurrent.futures.ProcessPoolExecutor() as pool2:
        result = await loop.run_in_executor(pool2, cpu_bound)
        print("custom process pool", result)


asyncio.run(main())  # asyncio 程序的主入口点，应该只被运行一次
##########################################################################
