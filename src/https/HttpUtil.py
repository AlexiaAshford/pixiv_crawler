import functools
import time

import requests
from tools.instance import *


def max_retry(func: callable) -> callable:
    @functools.wraps(func)
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
