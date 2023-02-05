import time
import requests
from lib.tools import *
from functools import wraps, partial


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


# def refresh_pixiv_token(error_info: str = "") -> None:
#     if error_info != "" and error_info is not None:
#         print("[error]:", error_info)
#     if PixivLogin.refresh(Vars.cfg.data.get("refresh_token")):
#         print("refresh token success, new token:", Vars.cfg.data.get("access_token"))
#     else:
#         print("refresh token failed, please login again")


class MessageError:

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            response = func(*args, **kwargs)
            if response.get("errors") is not None:
                print("errors:", response['errors'])
            else:
                return response

        return wrapper


class Request:
    def __init__(self, method: str, app: str, path: str):
        self.api_url = None
        self.path = path
        self.app = app
        self.method = method
        self.common_params = {"filter": "for_android"}
        if app == "app":
            self.headers = {
                'Host': 'app-api.pixiv.net ',
                'user-agent': 'PixivAndroidApp/{} (Android 11; Pixel 5)'.format(Vars.cfg.data['app_version']),
                'authorization': "Bearer " + Vars.cfg.data.get("access_token", ""),
                'app-version': Vars.cfg.data['app_version'],
            }
        elif app == "png" or app == "jpg" or app == "web":
            self.headers = {
                'Referer': 'https://www.pixiv.net/',
                'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/41.0.2227.1 Safari/537.36"
            }

    def __call__(self, func):
        @wraps(func)
        def wrapper(params=None, host=None):
            if params is None:
                params = {}
            if self.app == "app":
                params.update(self.common_params)
                self.api_url = (host if host else "https://app-api.pixiv.net/v1/") + self.path
            else:
                self.api_url = self.path
            if self.method == "GET":
                response = requests.request(method=self.method, url=self.api_url, params=params, headers=self.headers)
            else:
                response = requests.request(method=self.method, url=self.api_url, data=params, headers=self.headers)
            return func(response)

        return wrapper


GET = partial(Request, method="GET", app="app")

GET_WEB = partial(Request, method="GET", app="web")
