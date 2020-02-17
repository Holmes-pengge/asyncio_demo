import requests

PROXY_HOST = "lum-customer-onesiness-zone-ip:mmfzi3x924k1@zproxy.lum-superproxy.io"

check_api = "http://ip.taobao.com/service/getIpInfo2.php?ip="
ip = PROXY_HOST
api = check_api + ip
headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
    }
try:
    response = requests.get(url=api, headers=headers, timeout=2)
    print("ip：%s 可用" % ip)
except Exception as e:
    print("此ip %s 已失效：%s" % (ip, e))
