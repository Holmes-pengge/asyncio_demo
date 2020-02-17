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


class PingDomain:
    def __init__(self, file_path, save_path):
        self.file_path = file_path
        self.save_path = save_path
        self.result_ls = []

    @staticmethod
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
        except TimeoutError:
            item = {
                "url": host,
                "isalvie": 0,
                "finalurl": "",
            }

        except Exception as exc:
            item = {
                "url": host,
                "isalvie": 0,
                "finalurl": "",
            }
        return item

    async def handle_file(self):
        # 读取域名文件

        with open(self.file_path, 'r', encoding='gb18030', errors='ignore') as fp:
            for line in fp.readlines():
                host = line.strip()
                item = await self.executor(host)
                self.result_ls.append(item)

        with open(self.save_path, 'w') as f:
            f.write(json.dumps(self.result_ls))
        # ping_domain('www.baidrrrru.com')
        # ping_domain('www.baidu.com')
        # ping_domain('www.sina123456.com')


def main():
    filename = r'D:\tmp\unclass_test'
    save_path = 'domain_v3.json'
    # filename = r'D:\tmp\unclass'
    ping_domain = PingDomain(filename, save_path)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(ping_domain.handle_file())
    print(ping_domain.result_ls)


if __name__ == '__main__':
    start_time = time.time()
    main()
    print(time.time() - start_time)
