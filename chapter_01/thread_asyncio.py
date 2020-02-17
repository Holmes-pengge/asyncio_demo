import asyncio
import aiohttp
import requests
from concurrent.futures import ThreadPoolExecutor
import time
from urllib.parse import urlparse
import socket

#
# def get_url(url):
#     # 通过socket 请求HTML
#     url = urlparse(url)
#     host = url.netloc
#     path = url.path
#     if path == "":
#         path = "/"
#     # 建立socket 链接
#     client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client.connect((host, 80))  # 阻塞不会消耗 CPU
#     client.send("GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\n\r\n".format(path, host).encode("utf8"))
#     data = b""
#     while True:
#         d = client.recv(1024)
#         if d:
#             data += d
#         else:
#             break
#     data = data.decode("utf8")
#     html_data = data.split("\r\n\r\n")[1]
#     print(html_data)
#     client.close()
#


async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.request('get', url) as resp:
            return await resp.read()
    # async with requests.get(url, cookies=cookies) as resp:
    #     return await resp.text()


async def main():
    # url = "http://193.112.143.129/blt/pipeflow"
    url = "http://httpbin.org/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        'Cookie': 'sidebar_collapsed=false; _gitlab_session=7ae12a4207628addfcf7af235f5ff895'
    }
    cookies = "sidebar_collapsed=false; _gitlab_session=7ae12a4207628addfcf7af235f5ff895"
    html = await fetch(url)
    print(html)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())