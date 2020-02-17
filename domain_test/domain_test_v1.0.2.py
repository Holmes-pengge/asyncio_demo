import json
import socket
import asyncio
from pythonping import ping
import time

"""  
{
        "domains": [{
                "url": "www.baidu.com",
                "isalvie": 0,
                "finalurl": ""

        }, {
                "url": "www.sina.com",
                "isalvie": 1,
                "finalurl": "https://www.sina.com"
        }]
}
"""


# def ping_domain(domain):
#     resp = ping(domain, count=4, size=10)
#     print(resp)
#     if 'Round Trip Times min/avg/max is' in resp:
async def executor(host):
    item = {}
    try:
        ip = socket.gethostbyname(host)
        resp = ping(ip, timeout=2, count=4, size=10, df=False)
        if resp.success():
            print(host)
            item = {
                "url": host,
                "isalvie": 1,
                "finalurl": "https://{}".format(host),
            }
    except Exception as exc:
        item = {
            "url": host,
            "isalvie": 0,
            "finalurl": "",
        }
    return item


async def handle_file(filename):
    # 读取域名文件

    result_ls = []
    with open(filename, 'r', encoding='gb18030', errors='ignore') as fp:
        for line in fp.readlines():
            host = line.strip()
            item = await executor(host)
            result_ls.append(item)

    print(result_ls)
    with open('domain_v2.json', 'w') as f:
        f.write(json.dumps(result_ls))
    # ping_domain('www.baidrrrru.com')
    # ping_domain('www.baidu.com')
    # ping_domain('www.sina123456.com')


def main():
    # filename = r'D:\tmp\unclass_test'
    filename = r'D:\tmp\unclass'
    loop = asyncio.get_event_loop()
    loop.run_until_complete(handle_file(filename))


if __name__ == '__main__':
    start_time = time.time()
    main()
    print(time.time() - start_time)
