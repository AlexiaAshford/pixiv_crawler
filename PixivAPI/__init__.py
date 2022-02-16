from PixivAPI import login_pixiv
from fake_useragent import UserAgent
import setting
import requests
from pixivpy3 import *
from rich import print

config = setting.set_config()


def headers():
    return {
        'User-Agent': UserAgent(verify_ssl=False).random,
        'Referer': 'https://www.pixiv.net/',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Microsoft Edge";v="98"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'cookie': config.data("headers", "Cookie")
    }


def get(url, params=None, max_retry=config.data("headers", "retry")):
    for retry in range(int(max_retry)):
        result = requests.get(url=url, headers=headers(), params=params)
        if result.status_code == 200:
            return result
        print("插图下载失败，重新第{}次请求：".format(retry))


def input_(prompt, default=None):
    while True:
        ret = input(prompt)
        if ret != '':
            return ret
        elif default is not None:
            return default


class Download:
    @staticmethod
    def download_png(png_url: str) -> bytes:
        url = 'https://embed.pixiv.net/decorate.php?illust_id={}&mode=sns-automator'
        return get(url.format(png_url)).content


class PixivApp:
    @staticmethod
    def pixiv_app_api(max_retry=config.data("headers", "retry")):
        """构造API接口类"""
        app_pixiv = AppPixivAPI()
        for retry in range(int(max_retry)):
            access_token = config.data("user", "access_token")
            refresh_token = config.data("user", "refresh_token")
            app_pixiv.set_auth(access_token=access_token, refresh_token=refresh_token)
            if app_pixiv.illust_recommended().error is not None:
                login_pixiv.refresh(refresh_token)
                print("令牌失效，尝试刷新令牌{}：".format(retry))
            return app_pixiv

    @staticmethod
    def start_information():
        """收藏插画 <class 'pixivpy3.utils.JsonDict'>"""
        response = PixivApp.pixiv_app_api().illust_recommended()
        if response.error is None:
            return response.illust
        return ""

    @staticmethod
    def illustration_information(works_id: int):
        """插画信息 <class 'pixivpy3.utils.JsonDict'>"""
        response = PixivApp.pixiv_app_api().illust_detail(works_id)
        if response.error is None:
            return response.illust
        print(response.error["message"])
        return ""
