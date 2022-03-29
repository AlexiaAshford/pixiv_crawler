import requests
from instance import *
import functools
from fake_useragent import UserAgent


def MaxRetry(func, max_retry=5):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        for retry in range(max_retry):
            response = func(*args, **kwargs)
            if not isinstance(response, bool):
                return response
            else:
                time.sleep(retry * 0.5)
    return wrapper


def headers():
    return {
        'Referer': 'https://www.pixiv.net/',
        'User-Agent': UserAgent(verify_ssl=False).random,
        'cookie': Vars.cfg.data.get("Cookie"),
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Microsoft Edge";v="98"',
    }


@MaxRetry
def get(api_url: str, params=None, **kwargs):
    try:
        response = requests.get(api_url, headers=headers(), params=params, **kwargs)
        if response.status_code == 200:
            return response
        else:
            return False
    except requests.exceptions.RequestException as error:
        return False


@MaxRetry
def post(api_url: str, data=None, **kwargs):
    try:
        response = requests.post(api_url, headers=headers(), params=data, **kwargs)
        if response.status_code == 200:
            return response
        else:
            return False
    except requests.exceptions.RequestException as error:
        print("\nGet url:{} Error:{}".format(api_url, error))
        return False


@MaxRetry
def put(api_url: str, data=None, **kwargs):
    try:
        response = requests.put(api_url, headers=headers(), params=data, **kwargs)
        if response.status_code == 200:
            return response
        else:
            return False
    except requests.exceptions.RequestException as error:
        print("\nGet url:{} Error:{}".format(api_url, error))
        return False
