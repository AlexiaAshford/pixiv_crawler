import os
import re

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


def remove_str(content: str):
    file_name = re.sub('[/:*?"<>|]', '-', content)  # 去掉非法字符
    res_compile = re.compile(u'[\U00010000-\U0010ffff\\uD800-\\uDBFF\\uDC00-\\uDFFF]')
    return res_compile.sub("", file_name)


def input_(prompt, default=None):
    while True:
        ret = input(prompt)
        if ret != '':
            return ret
        elif default is not None:
            return default


def mkdir(file_path: str):
    if not os.path.exists(file_path):
        os.mkdir(file_path)


class Download:
    @staticmethod
    def download(png_url: str, png_name: str, file_path: str):
        with open(os.path.join(file_path, f'{png_name}.png'), 'wb+') as file:
            print(f"插图 {png_name} 下载成功")
            file.write(get(png_url).content)
            print('成功下载图片：{}.png'.format(png_name))


class PixivApp:
    @staticmethod
    def pixiv_app_api(max_retry=config.data("headers", "retry")):
        """构造API接口类"""
        app_pixiv = AppPixivAPI()
        for index, retry in enumerate(range(int(max_retry))):
            access_token = config.data("user", "access_token")
            refresh_token = config.data("user", "refresh_token")
            app_pixiv.set_auth(access_token=access_token, refresh_token=refresh_token)
            if app_pixiv.illust_recommended().error is not None:
                login_pixiv.refresh(refresh_token)
                print("令牌失效，尝试刷新令牌{}".format(index))
            return app_pixiv

    @staticmethod
    def start_information():
        """收藏插画 <class 'pixivpy3.utils.JsonDict'>"""
        response = PixivApp.pixiv_app_api().illust_recommended()
        if response.error is None:
            return response.illusts
        return response.error

    @staticmethod
    def illustration_information(works_id: int):
        """插画信息 <class 'pixivpy3.utils.JsonDict'>"""
        response = PixivApp.pixiv_app_api().illust_detail(works_id)
        if response.error is None:
            return response.illust
        return response.error
