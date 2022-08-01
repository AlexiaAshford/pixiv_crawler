import requests
from tools.instance import *
import functools


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


def request(
        api_url: str,
        method: str = "GET",
        headers: dict = None,
        params: dict = None,
        max_retry_count: int = 5,
) -> requests.request:
    for retry in range(max_retry_count):
        try:
            if method == "GET":
                return requests.request(method=method, url=api_url, params=params, headers=headers)
            else:
                return requests.request(method=method, url=api_url, data=params, headers=headers)
        except requests.exceptions.RequestException as error:
            print("there is an error:", error)
        except Exception as error:
            print("there is an error:", error)
    else:
        print("retry too many times, please check your network")
