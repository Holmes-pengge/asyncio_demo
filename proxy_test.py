import requests
import redis

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
        return p


def fetch():
    url = "http://icanhazip.com"
    with requests.Session() as s:
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        }
        s.headers.update(header)
        timeout = 5
        # proxy_pool = SelfProxy()
        while True:
            try:
                # p = proxy_pool.random_one
                resp = s.get(url, proxies=proxy, timeout=timeout)
                print(resp.status_code)
                print(resp.text)
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



