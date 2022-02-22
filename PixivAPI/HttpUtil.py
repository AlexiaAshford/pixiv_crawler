import requests
from instance import *
from fake_useragent import UserAgent


def headers():
    return {
        'Referer': 'https://www.pixiv.net/',
        'User-Agent': UserAgent(verify_ssl=False).random,
        'cookie': Vars.cfg.data("headers", "Cookie"),
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Microsoft Edge";v="98"',
    }


def get(url, params=None, max_retry=10, *args, **kwargs):
    for retry in range(max_retry):
        result = requests.get(url=url, headers=headers(), params=params)
        if result.status_code == 200:
            return result
        print("插图下载失败，重新第{}次请求：".format(retry))


def post(url, data=None, *args, **kwargs):
    for retry in range(int(Vars.cfg.data("headers", "retry"))):
        result = requests.post(url=url, headers=headers(), data=data)
        if result.status_code == 200:
            return result
        print("插图下载失败，重新第{}次请求：".format(retry))


def put(url, data=None, *args, **kwargs):
    for retry in range(int(Vars.cfg.data("headers", "retry"))):
        result = requests.put(url=url, headers=headers(), data=data)
        if result.status_code == 200:
            return result
        print("插图下载失败，重新第{}次请求：".format(retry))
