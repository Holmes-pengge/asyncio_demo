import json
import re

import requests

from lxml import etree

url = 'https://www.jianshu.com/p/f712a5a46e95'


def downloader():
    """"下载网页"""
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
    }

    resp = requests.get(url=url, headers=headers)
    if resp.status_code == 200:
        with open(url.split('/')[-1] + '.html', 'w', encoding='utf-8') as fp:
            fp.write(resp.text)
        return resp
    else:
        return None


def parser():
    """解析 HTML"""
    resp = downloader()

    if resp:
        # html = etree.HTML(resp.text)
        # name = html.xpath('//div[@class="_3U4Smb"]/span/a/text()')
        # print(name)
        pattern = re.compile('<script>(.*?)</script>')
        result = pattern.findall(resp.text)[0]
        print(result)
        # result_dct = json.loads(result)
        # print(result_dct)
    else:
        print('response 为空')


if __name__ == '__main__':
    parser()
