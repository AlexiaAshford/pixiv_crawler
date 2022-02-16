import json
from fake_useragent import UserAgent
import setting

import requests

config = setting.set_config()


def headers():
    return {
        'authority': 'www.pixiv.net',
        'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'user-agent': UserAgent(verify_ssl=False).random,
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.pixiv.net/ranking.php?mode=daily&content=illust',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': config.data("headers", "Cookie")
    }


def get(url, params=None, max_retry=config.data("headers", "retry")):
    for retry in range(int(max_retry)):
        result = requests.get(url=url, headers=headers(), params=params)
        if result.status_code == 200:
            return result
        print("重新请求：", retry)


class Ranking:
    @staticmethod
    def ranking_id(page) -> dict:
        params = (('mode', 'rookie'), ('content', 'illust'), ('p', page), ('format', 'json'),)
        return json.loads(get('https://www.pixiv.net/ranking.php', params).text)


class Download:
    @staticmethod
    def download(png_id) -> dict:
        url = 'https://embed.pixiv.net/decorate.php?illust_id={}&mode=sns-automator'
        return get(url.format(png_id)).content
