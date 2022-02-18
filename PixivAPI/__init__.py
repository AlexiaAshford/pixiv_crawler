import os
import re
import time

from PixivAPI import login_pixiv
from fake_useragent import UserAgent
import setting
import requests
from PixivApp import *
from rich import print
import threading

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


def rec_id(book_id):
    book_id = book_id if 'http' not in book_id else re.findall(r'/([0-9]+)/?', book_id)[0]
    return int(book_id) if book_id.isdigit() else f'输入信息 {book_id} 不是数字或链接！'


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
    def save_image(image_id: int):
        response = PixivApp.illustration_information(image_id)
        if response.get("message") is None:
            image_name = remove_str(response.title)
            file_path = config.data("user", "save_file")
            if not os.path.exists(os.path.join(file_path, f'{image_name}.png')):
                with open(os.path.join(file_path, f'{image_name}.png'), 'wb+') as file:
                    file.write(get(response.image_urls['large']).content)
                    print('成功下载图片：{}\n'.format(image_name))
            else:
                print(f"{image_name} 已经下载过了\n")
        else:
            print(response.get("message"))

    @staticmethod
    def threading_download(image_id_list: list):
        image_id_len = len(image_id_list)
        lock_tasks_list = threading.Lock()
        print(f"开始下载，一共 {image_id_len} 张图片")

        # 生成下载队列.
        def downloader():
            """多线程下载函数"""
            nonlocal lock_tasks_list

            while image_id_list:
                lock_tasks_list.acquire()
                image_id = image_id_list.pop()
                print("正在下载第{}张".format(image_id_len - len(image_id_list)))
                lock_tasks_list.release()
                Download.save_image(image_id)

        threads_pool = []
        for _ in range(int(config.data("user", "max_thread"))):
            th = threading.Thread(target=downloader)
            threads_pool.append(th)
            th.start()

        # wait downloader
        for th in threads_pool:
            th.join()


class PixivApp:
    @staticmethod
    def pixiv_app_api(max_retry=config.data("headers", "retry")):
        """构造API接口类"""
        for index, retry in enumerate(range(int(max_retry))):
            app_pixiv = AppPixivAPI()
            access_token = config.data("user", "access_token")
            refresh_token = config.data("user", "refresh_token")
            app_pixiv.set_auth(access_token=access_token, refresh_token=refresh_token)
            if app_pixiv.illust_recommended().error is not None:
                login_pixiv.refresh(refresh_token)
                print("令牌失效，尝试刷新令牌:retry {}".format(index))
            return app_pixiv

    @staticmethod
    def start_information():
        """收藏插画 <class 'PixivApp.utils.JsonDict'>"""
        response = PixivApp.pixiv_app_api().illust_recommended()
        if response.error is None:

            return response.illusts
        return response.error

    @staticmethod
    def recommend_information():
        """推荐插画 <class 'PixivApp.utils.JsonDict'>"""
        response = PixivApp.pixiv_app_api().illust_recommended()
        next_qs = PixivApp.pixiv_app_api().parse_qs(response.next_url)
        while next_qs is not None:
            response = PixivApp.pixiv_app_api().illust_recommended(**next_qs)
            if response.error is not None:
                return response.error
            image_id_list = list(set([data.id for data in response.illusts]))
            if type(image_id_list) is list and len(image_id_list) != 0:
                Download.threading_download(image_id_list)
            else:
                print("Pixiv推荐插图下载完毕")


    @staticmethod
    def follow_information():
        """关注用户信息 <class 'PixivApp.utils.JsonDict'>"""
        response = PixivApp.pixiv_app_api().illust_follow()
        if response.error is None:
            return list(set([data.id for data in response.illusts]))
        return response.error

    @staticmethod
    def author_information(author_id: str):
        """作者作品集 <class 'PixivApp.utils.JsonDict'>"""
        response = PixivApp.pixiv_app_api().user_illusts(author_id)
        if response.error is None:
            return list(set([data.id for data in response.illusts]))
        return response.error

    @staticmethod
    def search_information(png_name: str, search_target: str):
        """搜搜插画 <class 'PixivApp.utils.JsonDict'>"""
        response = PixivApp.pixiv_app_api().search_illust(
            word=png_name, search_target=search_target
        )
        if response.error is None:
            return list(set([data.id for data in response.illusts]))
        return response.error

    @staticmethod
    def illustration_information(works_id: int):
        """插画信息 <class 'PixivApp.utils.JsonDict'>"""
        response = PixivApp.pixiv_app_api().illust_detail(works_id)
        if response.error is None:
            tags_llist = [i['name'] for i in response.illust['tags']]
            print("插画名称: {}:".format(response.illust.title))
            print("插画ID: {}".format(response.illust.id))
            print("作者名称: {}".format(response.illust.user['name']))
            print("插画标签: {}".format(', '.join(tags_llist)))
            print("发布时间: {}\n".format(response.illust.create_date))
            return response.illust
        return response.error
