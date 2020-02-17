import requests

PROXY_HOST = "lum-customer-onesiness-zone-ip:mmfzi3x924k1@zproxy.lum-superproxy.io"
PROXY_PORT = 22225

proxy = {
    "http": "http://" + PROXY_HOST + ":22225",
    "https": "https://" + PROXY_HOST + ":22225",
}

headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
}
#
resp = requests.get('http://icanhazip.com', headers=headers, proxies=proxy, timeout=2)
# resp = requests.get('http://icanhazip.com', headers=headers, proxies={"http": "http://121.31.154.12:8123"}, timeout=2)
print(resp.status_code)
print(resp.text)
