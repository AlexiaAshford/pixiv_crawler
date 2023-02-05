
import time
import requests

from functools import wraps, partial
from lib.tools import Vars


def max_retry(func: callable) -> callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        for retry in range(5):
            response = func(*args, **kwargs)
            if not isinstance(response, bool):
                return response
            else:
                time.sleep(retry * 0.5)

    return wrapper


def request(api_url: str, method: str = "GET", headers: dict = None, params: dict = None) -> requests.request:
    try:
        if method == "GET":
            return requests.request(method=method, url=api_url, params=params, headers=headers)
        else:
            return requests.request(method=method, url=api_url, data=params, headers=headers)
    except requests.exceptions.RequestException as error:
        print("request error: {}".format(error))
    except Exception as error:
        print("request exception error: {}".format(error))


class Request:
    def __init__(self, method: str, app: str = None):
        self.api_url = None
        self.method = method
        self.params = {}
        self.common_params = {"filter": "for_android"}
        if app == "app":
            self.params = self.common_params
            self.headers = {
                'Host': 'app-api.pixiv.net ',
                'user-agent': 'PixivAndroidApp/{} (Android 11; Pixel 5)'.format("6.46.0"),
                'authorization': "Bearer " + "Cf1beejLfplEpi5061L0f4i1UyiogU8QBnIFGShcV_A",
                'app-version': "6.46.0",
            }
        elif app == "png" or app == "jpg":
            self.headers = {
                'Referer': 'https://www.pixiv.net/',
                'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/41.0.2227.1 Safari/537.36"
            }

    def __call__(self, func):
        @wraps(func)
        def wrapper(params, host=None, path=None):
            self.params.update(params if params else {})
            self.api_url = host if host else "https://app-api.pixiv.net/v1/"
            self.api_url = self.api_url + path if path else self.api_url
            print(self.api_url, self.params, self.headers)
            if self.method == "GET":
                response = requests.request(method=self.method, url=self.api_url, params=params, headers=self.headers)
            else:
                response = requests.request(method=self.method, url=self.api_url, data=params, headers=self.headers)
            return func(response)

        return wrapper


GET = partial(Request, method="GET", app="app")


# @GET()
# def get_(response):
#     print(response.text)
#
#
# if __name__ == '__main__':
#     get_(params={"include_ranking_illusts": "true", "include_privacy_policy": "true"}, path="illust/recommended")
