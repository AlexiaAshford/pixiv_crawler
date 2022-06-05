from typing import Union
import requests
from instance import *
import functools


def max_retry(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        for retry in range(5):
            response = func(*args, **kwargs)
            if not isinstance(response, bool):
                return response
            else:
                time.sleep(retry * 0.5)

    return wrapper


# def headers():
#     return {
#         'Referer': 'https://www.pixiv.net/',
#         'User-Agent': UserAgent(verify_ssl=False).random,
#         'sec-ch-ua-mobile': '?0',
#         'sec-ch-ua-platform': '"Windows"',
#         'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Microsoft Edge";v="98"',
#     }


# def android_app():
#     return {
#         'Host': 'app-api.pixiv.net ',
#         'user-agent': 'PixivAndroidApp/6.46.0',
#         'authorization': "Bearer " + Vars.cfg.data.get("access_token"),
#         'app-version': '6.46.0 ',
#     }


# @MaxRetry
# def get(api_url: str, params=None, **kwargs):
#     try:
#         response = requests.get(api_url, headers=headers(), params=params, **kwargs)
#         if response.status_code == 200:
#             return response
#         else:
#             return False
#     except requests.exceptions.RequestException as error:
#         print("\nGet url:{} Error:{}".format(api_url, error))
#         return False


def get_api(
        api_url: str,
        params: Union[dict, str] = None,
        headers: dict = "app",
        return_type: str = "json",
        **kwargs
        ) -> Union[dict, bool, bytes, str]:

    try:
        if return_type == "json":
            return requests.get(api_url, headers=headers, params=params, **kwargs).json()
        if return_type == "content":
            return requests.get(api_url, headers=headers, params=params, **kwargs).content
        if return_type == "text":
            return requests.get(api_url, headers=headers, params=params, **kwargs).text
    except requests.exceptions.RequestException as error:
        print("HttpUtil.get error:", error)


# @MaxRetry
# def post(api_url: str, data=None, **kwargs):
#     try:
#         response = requests.post(api_url, headers=headers(), params=data, **kwargs)
#         if response.status_code == 200:
#             return response
#         else:
#             return False
#     except requests.exceptions.RequestException as error:
#         print("\nGet url:{} Error:{}".format(api_url, error))
#         return False
#
#
# @MaxRetry
# def put(api_url: str, data=None, **kwargs):
#     try:
#         response = requests.put(api_url, headers=headers(), params=data, **kwargs)
#         if response.status_code == 200:
#             return response
#         else:
#             return False
#     except requests.exceptions.RequestException as error:
#         print("\nGet url:{} Error:{}".format(api_url, error))
#         return False
