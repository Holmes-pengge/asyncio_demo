import requests
import redis
from random import choice

PROXY_HOST = "lum-customer-onesiness-zone-ip:mmfzi3x924k1@zproxy.lum-superproxy.io"
PROXY_PORT = "22225"

'''代理IP地址（高匿）'''
proxy = {
    "http": "http://" + PROXY_HOST + ":" + PROXY_PORT,
    "https": "http://" + PROXY_HOST + ":" + PROXY_PORT,
}


# proxy = {
#     "http": "http://bi273023:bi273023@134.73.209.228:7777",
#     "https": "https://bi273023:bi273023@134.73.209.228:7777"
# }

class PoolEmptyError(Exception):

    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return repr('代理池已经枯竭')


class SelfProxy2:
    # 自建代理
    def __init__(self):
        self._redis = redis.StrictRedis(
            host='127.0.0.1',
            port=6379,
            password=None,
            db=0,
        )

    @property
    def random_one(self):
        """
        随机获取有效代理，首先尝试获取最高分数代理，如果不存在，按照排名获取，否则异常
        :return: 随机代理
        """
        result = self._redis.zrangebyscore('proxies', 100, 100)
        if len(result):
            ip_port = choice(result).decode('utf-8')
            p = {
                "http": "http://" + ip_port,
                "https": "https://" + ip_port,
            }
            return p
        else:
            result = self._redis.zrevrange('proxies', 0, 100)
            if len(result):
                ip_port = choice(result).decode('utf-8')
                p = {
                    "http": "http://" + ip_port,
                    "https": "https://" + ip_port,
                }
                return p
            else:
                raise PoolEmptyError


class SelfProxy:
    # 自建代理
    def __init__(self):
        self._redis = redis.StrictRedis(
            host='45.34.33.156',
            port='12111',
            password='513f21fbc55d446186c7f1daa9dae626',
            db=10,
        )

    @property
    def random_one(self):
        ip_port = self._redis.srandmember('proxy_pool_us')
        p = {
            "http": "http://" + ip_port.decode('utf-8'),
            "https": "https://" + ip_port.decode('utf-8'),
        }
        print(p)
        return p


def fetch():
    # url = "http://icanhazip.com"
    # url = "http://httpbin.org/get"
    url = "https://detail.1688.com/offer/609640207222.html"

    with open(r'D:\work\code\private_code\asyncio_demo\cookies.txt', 'r') as fp:
        cookies = {}
        for line in fp.read().split(';'):
            k, v = line.strip().split('=', 1)
            cookies[k] = v

    with requests.Session() as s:
        # header = {
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        # }
        h = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1',
            "upgrade-insecure-requests": "1",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en,zh-CN;q=0.9,zh;q=0.8",
        }
        s.headers.update(h)
        timeout = 5
        cookies = cookies
        proxy_pool = SelfProxy()
        while True:
            try:
                # p = proxy_pool.random_one
                # print(p)

                # resp = s.get(url, cookies=cookies, proxies=p, timeout=timeout)
                resp = s.get(url, cookies=cookies, timeout=timeout)
                print(cookies)

                with open(url.split('/')[-1], 'w', encoding="utf-8") as fp:
                    fp.write(resp.text)
                if resp.status_code == 200:
                    print(resp.status_code)
                    print(resp.text)
                    break
            except requests.exceptions.ProxyError as exc:
                print("proxy error")
                continue
            except requests.exceptions.Timeout as exc:
                print("time out")
                continue
            except requests.exceptions.ConnectionError as exc:
                print("ConnectionError")
                continue


if __name__ == '__main__':
    fetch()

# resp = requests.get('http://icanhazip.com', headers=header, proxies=proxy, timeout=5)
# resp = requests.get('https://www.baidu.com', headers=head)
# resp = requests.get('https://www.baidu.com', headers=head, proxies=proxy)
# resp = requests.get('http://icanhazip.com', headers=head)
