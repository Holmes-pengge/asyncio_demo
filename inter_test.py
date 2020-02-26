import redis


class Person:
    def __init__(self, name):
        self.name = name

    def __len__(self):
        return len(self.name)


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

if __name__ == '__main__':
    # p = Person('Tom')
    # print(p.name)
    # print(len(p))
    # from pygeocoder import Geocoder
    #
    # results = Geocoder.geocode("Tian'anmen, Beijing")
    # print(results[0].coordinates)
    import requests

    PROXY_HOST = "lum-customer-onesiness-zone-ip:mmfzi3x924k1@zproxy.lum-superproxy.io"
    PROXY_PORT = "22225"

    '''代理IP地址（高匿）'''
    proxy = {
        "http": "http://" + PROXY_HOST + ":" + PROXY_PORT,
        "https": "http://" + PROXY_HOST + ":" + PROXY_PORT,
    }
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
    }
    proxy_pool = SelfProxy()
    p = proxy_pool.random_one

    base_url = 'https://maps.google.com/maps/api/geocode/json?'
    url = 'https://www.baidu.com'
    params = {
        'address': "Tian'anmen, Beijing",
        'sensor': False,
    }
    resp = requests.get(url, headers=header,proxies=p)
    print(resp.status_code)
    print(resp.text)
    print(resp.json())