import time

import requests
from lxml import etree


def fetch(offset):
    # top_url = 'https://maoyan.com/board/4'
    top_url = 'https://maoyan.com/board/4?offset={}'.format(offset)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'Referer': 'https://maoyan.com/board/4',
    }

    resp = requests.get(top_url, headers=headers)
    html = etree.HTML(resp.text)
    data_list = []
    for dd in html.xpath('//div[@id="app"]//dl[@class="board-wrapper"]//dd'):
        movie_name = dd.xpath('.//p[@class="name"]//text()')[0]
        # print(movie_name)
        star = dd.xpath('.//p[@class="star"]//text()')[0].strip()
        # print(star)
        release_time = dd.xpath('.//p[@class="releasetime"]//text()')[0]
        integer = dd.xpath('.//p[@class="score"]/i[1]/text()')[0]
        fraction = dd.xpath('.//p[@class="score"]/i[2]/text()')[0]
        score = str(integer) + str(fraction)
        # print(score)
        img = dd.xpath('./a/img[2]/@src')
        # print(img)
        item = {
            'movie_name': movie_name,
            'star': star,
            'release_time': release_time,
            'score': score,
            'img': img,
        }
        # print(item)
        data_list.append(item)
    return data_list


def main():
    result_list = []
    for i in range(10):
        data_list = fetch(offset=i * 10)
        result_list.extend(data_list)
        time.sleep(1)
    # print(result_list)
    return result_list


if __name__ == '__main__':
    # main()
    print(fetch(20))