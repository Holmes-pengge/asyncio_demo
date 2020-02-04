import re
import time
import requests
import json

from demo.mtime_spider2.log import logger


class HTMLDownloader(object):
    """下载网页"""

    @staticmethod
    def downloader(url):
        """
        下载网页内容
        Parameters
        ----------
        url

        Returns
        -------

        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        }
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            resp.encoding = 'utf-8'
            return resp.text
        return None


class HTMLParser(object):
    """解析网页"""

    @staticmethod
    def parse_url(response):
        """
        提取当前正在上映的电影链接
        Parameters
        ----------
        response

        Returns
        -------

        """
        pattern = re.compile(r'(http://movie.mtime.com/(\d+)/)')
        urls = pattern.findall(response)
        if urls is not None:
            return list(set(urls))  # 对 URL 去重
        else:
            return None

    def parse_json(self, page_url, response):
        """
        提取响应内容, 并区分电影是否已上映
        Parameters
        ----------
        page_url
        response

        Returns
        -------

        """
        ''' 未上映
        var result_202022189586465 = {
            "value": {
                "isRelease": false,
                "movieRating": {
                    "MovieId": 254785,
                    "RatingFinal": -1,
                    "RDirectorFinal": 0,
                    "ROtherFinal": 0,
                    "RPictureFinal": 0,
                    "RShowFinal": 0,
                    "RStoryFinal": 0,
                    "RTotalFinal": 0,
                    "Usercount": 88,
                    "AttitudeCount": 3435,
                    "UserId": 0,
                    "EnterTime": 0,
                    "JustTotal": 0,
                    "RatingCount": 0,
                    "TitleCn": "",
                    "TitleEn": "",
                    "Year": "",
                    "IP": 0
                },
                "movieTitle": "唐人街探案3",
                "tweetId": 0,
                "userLastComment": "",
                "userLastCommentUrl": "",
                "releaseType": 0,
                "hotValue": {
                    "MovieId": 254785,
                    "Ranking": 1,
                    "Changing": 0,
                    "YesterdayRanking": 1
                }
            },
            "error": null
        };
        var movieOverviewRatingResult = result_202022189586465;
        '''

        '''  已上映
        var result_2020221815342671 = {
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
                    "Usercount": 3579,
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
                    "EndDate": "2020-02-02 15:06",
                    "FirstDayBoxOffice": "2510.69",
                    "FirstDayBoxOfficeUnit": "万"
                }
            },
            "error": null
        };
        var movieOverviewRatingResult = result_2020221815342671;
        '''
        # 提取 "=" 和 ";" 之间的内容 ,纯 json
        pattern = re.compile(r'=(.*?);')
        result = pattern.findall(response)[0]
        if result is not None:
            value_dct = json.loads(result)
            try:
                isRelease = value_dct.get('value').get('isRelease')
            except Exception as err:
                logger.error(err)
                return None
            if isRelease:
                if value_dct.get('value').get('hotValue') is None:
                    return self._parser_release(page_url, value_dct)
                else:
                    return self._parser_no_release(page_url, value_dct, isRelease=2)
            else:
                return self._parser_no_release(page_url, value_dct)

    @staticmethod
    def _parser_release(page_url, value):
        """
        解析已经上映的影片
        Parameters
        ----------
        page_url 影片 URL
        value

        Returns
        -------

        """
        try:
            isRelease = 1
            movieRating = value.get('value').get('movieRating')
            movieTitle = value.get('value').get('movieTitle')
            RatingFinal = movieRating.get('RatingFinal')
            return RatingFinal, movieTitle
        except Exception as err:
            logger.error(err, page_url, value)
            return None

    @staticmethod
    def _parser_no_release(page_url, value):
        """
        解析 未上映的影片
        Parameters
        ----------
        page_url
        value

        Returns
        -------

        """
        try:
            movieRating = value.get('value').get('movieRating')
            movieTitle = value.get('value').get('movieTitle')
            return movieRating, movieTitle
        except Exception as err:
            logger.error(err, page_url, value)
            return None


class Save(object):
    """保存结果"""
    pass


class SpiderMan(object):
    """爬虫调度器, 协调各模块，以及构造ajax请求的 动态URL"""

    def __init__(self):
        self.downloader = HTMLDownloader()
        self.parser = HTMLParser()

    def crawl(self, root_url):
        content = self.downloader.downloader(root_url)
        urls = self.parser.parse_url(content)
        for url in urls:
            try:
                t = time.strftime('%Y%m%d%H%M%S2323', time.localtime())
                rank_url = 'http://service.library.mtime.com/Movie.api' \
                           '?Ajax_CallBack=true' \
                           '&Ajax_CallBackType=Mtime.Library.Services' \
                           '&Ajax_CallBackMethod=GetMovieOverviewRating' \
                           '&Ajax_CrossDomain=1' \
                           '&Ajax_RequestUrl={0}' \
                           '&t={1}' \
                           '&Ajax_CallBackArgument0={2}'.format(url[0], t, url[1])
                rank_content = self.downloader.downloader(rank_url)
                data = self.parser.parse_json(rank_url, rank_content)
                print(data)
            except Exception as err:
                logger.error('crawl failed')
            time.sleep(0.5)
        logger.info("crawl finished")


if __name__ == '__main__':
    spider = SpiderMan()
    spider.crawl('http://theater.mtime.com/China_Beijing/')
