import asyncio


async def downloader(url):
    print('start fetch...')
    await asyncio.sleep(2)
    print('end fetch...')


def parser(response):
    pass


def save(data):
    pass


def spider_man():
    import time
    start_time = time.time()
    tasks = [downloader('www.baidu.com') for i in range(100)]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    print(time.time() - start_time)


if __name__ == '__main__':
    spider_man()