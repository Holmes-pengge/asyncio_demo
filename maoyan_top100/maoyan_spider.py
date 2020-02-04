# !/usr/bin/python
# -*- coding: utf-8 -*-
import time

import requests
from lxml import etree


def fetch(offset):
    # top_url = 'https://maoyan.com/board/4?offset={}'.format(str(offset))
    top_url = 'https://maoyan.com/board/4'

    headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
        'Referer': 'https://maoyan.com/board/4',
    }

    r = requests.get(top_url, headers=headers)

    # with open('./maoyan_top100.html', 'w', encoding='utf-8') as fp:
    #     fp.write(r.text)

    # print(r.status_code)
    # print(r.text)
    html = etree.HTML(r.text)
    # name_list = html.xpath('//p[@class="name"]/a/text()')
    # for name in name_list:
    #     print(name)
    #
    # star_list = html.xpath('//p[@class="star"]/text()')
    # for star in star_list:
    #     print(star.strip())
    #
    # release_time_list = html.xpath('//p[@class="releasetime"]/text()')
    # for time in release_time_list:
    #     print(time.strip())

    # for node in html.xpath('//p[@class="score"]'):
    #     integer = node.xpath('./i[1]/text()')[0]
    #     fraction = node.xpath('./i[2]/text()')[0]
    #     # print(type(integer), integer)
    #     # print(type(fraction), fraction)
    #     score = integer + fraction
    #     print(score)

    result_list = []
    for node in html.xpath('//dl[@class="board-wrapper"]//dd'):
        movie_name = node.xpath('.//p[@class="name"]/a/text()')[0]
        print(movie_name)
        star = node.xpath('.//p[@class="star"]/text()')[0].strip()
        # print(star)
        # star = star.strip()
        release_time = node.xpath('.//p[@class="releasetime"]/text()')[0].strip()
        # release_time = release_time.strip()
        integer = node.xpath('.//p[@class="score"]/i[1]/text()')[0]
        fraction = node.xpath('.//p[@class="score"]/i[2]/text()')[0]
        score = integer + fraction
        # print(score)
        item = {
            'movie_name': movie_name,
            'star': star,
            'release_time': release_time,
            'score': score,
        }
        result_list.append(item)
    # print(result_list)
    return result_list

    # print(html.xpath('//dl[@class="board-wrapper"]//dd/a/img[2]/@src'))
    # print(html.xpath('//dl[@class="board-wrapper"]//dd/a//@src'))
    # print(html.xpath('//dl[@class="board-wrapper"]//dd/a/img[@class="board-img"]/@src'))
    # for img in html.xpath('//dl[@class="board-wrapper"]//dd/a//@src'):
    #     print(img)


def main():
    data = []

    for i in range(10):
        result_list = fetch(offset=i * 10)
        data.extend(result_list)
        time.sleep(1)
    print(data)


if __name__ == '__main__':
    # main()
    rst = fetch(1)
    print(rst)