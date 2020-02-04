# !/usr/bin/python
# -*- coding: utf-8 -*-
import json
import time

import requests
from lxml import etree
import re

from demo.mtime_spider.log import logger


class HTMLDownloader(object):
    """HTML 下载器"""

    @staticmethod
    def download(url):
        if url is None:
            return None

        headers = {
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
        }

        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            resp.encoding = 'utf-8'
            return resp.text
        return None


class HTMLParser(object):
    """HTML 解析器"""

    @staticmethod
    def parse_url(page_url, response):
        """提取当前正在上映的电影链接 """
        pattern = re.compile(r'(http://movie.mtime.com/(\d+)/)')
        urls = pattern.findall(response)
        if urls is not None:
            return list(set(urls))  # 对 URL 进行去重
        else:
            return None

    def parse_json(self, page_url, response):
        """解析响应"""
        '''
            var result_2020211945063034 = {
            "value": {
                "isRelease": true,
                "movieRating": {
                    "MovieId": 258541,
                    "RatingFinal": 8.2,
                    "RDirectorFinal": 8,
                    "ROtherFinal": 8.1,
                    "RPictureFinal": 7.9,
                    "RShowFinal": 0,
                    "RStoryFinal": 8.2,
                    "RTotalFinal": 0,
                    "Usercount": 3574,
                    "AttitudeCount": 1330,
                    "UserId": 0,
                    "EnterTime": 0,
                    "JustTotal": 0,
                    "RatingCount": 0,
                    "TitleCn": "",
                    "TitleEn": "",
                    "Year": "",
                    "IP": 0
                },
                "movieTitle": "绿皮书",
                "tweetId": 0,
                "userLastComment": "",
                "userLastCommentUrl": "",
                "releaseType": 3,
                "boxOffice": {
                    "Rank": 0,
                    "TotalBoxOffice": "4.78",
                    "TotalBoxOfficeUnit": "亿",
                    "TodayBoxOffice": "0.0",
                    "TodayBoxOfficeUnit": "万",
                    "ShowDays": 0,
                    "EndDate": "2020-02-01 15:06",
                    "FirstDayBoxOffice": "2510.69",
                    "FirstDayBoxOfficeUnit": "万"
                }
            },
            "error": null
        };
        var movieOverviewRatingResult = result_2020211945063034; 
               
        '''

        # 提取 "=" 和 ";" 之间的内容
        pattern = re.compile(r'=(.*?);')
        result = pattern.findall(response)[0]
        print(result)
        if result is not None:
            value_dct = json.loads(result)
            try:
                isRelease = value_dct.get('value').get('isRelease')
            except Exception as e:
                logger.error(e)
                return None
            if isRelease:
                if value_dct.get('value').get('hotValue') is None:  # 说明正在上映
                    return self._parse_release(page_url, value_dct)
                else:
                    return self._parse_no_release(page_url, value_dct, isRelease=2)
            else:
                return self._parse_no_release(page_url, value_dct)

    @staticmethod
    def _parse_release(page_url, value):
        """
        解析已经上映的影片
        Parameters
        ----------
        page_url: 电影链接
        value: dict 类型

        Returns
        -------

        """
        try:
            isRelease = 1
            movieRating = value.get('value').get('movieRating')
            boxOffice = value.get('value').get('boxOffice')
            movieTitle = value.get('value').get('movieTitle')
            RPictureFinal = movieRating.get('RPictureFinal')
            RStoryFinal = movieRating.get('RStoryFinal')

            try:
                Rank = boxOffice.get('Rank')
            except Exception as e:
                Rank = 0
            return movieTitle, RPictureFinal, RStoryFinal, Rank
        except Exception as e:
            logger.error(e, page_url, value)
            return None

    @staticmethod
    def _parse_no_release(page_url, value, isRelease=0):
        """
        解析没有上映的电影信息
        Parameters
        ----------
        page_url: 电影链接
        value: dict 类型

        Returns
        -------

        """
        try:
            movieRating = value.get('value').get('movieRating')
            movieTitle = value.get('value').get('movieTitle')
            try:
                Rank = value.get('value').get('hotValue').get('Ranking')
            except Exception as e:
                Rank = 0
            return movieTitle, movieRating, Rank
        except Exception as e:
            logger.error(e, page_url, value)
            return None


class SpiderMan(object):
    """爬虫调度器，协调各个模块，并且负责构造 ajax 动态 URL"""

    def __init__(self):
        self.downloader = HTMLDownloader()
        self.parser = HTMLParser()

    def crawl(self, root_url):
        content = self.downloader.download(root_url)
        urls = self.parser.parse_url(root_url, content)
        # 构造一个获取 评分 和 票房信息的 URL
        if urls:
            for url in urls:
                logger.info(url)
                try:
                    t = time.strftime('%Y%m%d%H%M%S3333', time.localtime())
                    rank_url = 'http://service.library.mtime.com/Movie.api' \
                               '?Ajax_CallBack=true' \
                               '&Ajax_CallBackType=Mtime.Library.Services' \
                               '&Ajax_CallBackMethod=GetMovieOverviewRating' \
                               '&Ajax_CrossDomain=1' \
                               '&Ajax_RequestUrl={0}' \
                               '&t={1}' \
                               '&Ajax_CallBackArgument0={2}'.format(url[0], t, url[1])
                    rank_content = self.downloader.download(rank_url)
                    data = self.parser.parse_json(rank_url, rank_content)
                    print(data)
                except Exception as e:
                    logger.error(e)


if __name__ == '__main__':
    spider = SpiderMan()
    spider.crawl('http://theater.mtime.com/China_Beijing/')
