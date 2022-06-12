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


def get_api(
        api_url: str,
        params: Union[dict, str] = None,
        headers: dict = "app",
        return_type: str = "json",
        **kwargs) -> Union[dict, bool, bytes, str]:
    try:
        if return_type == "json":
            return requests.get(api_url, headers=headers, params=params, **kwargs).json()
        if return_type == "content":
            return requests.get(api_url, headers=headers, params=params, **kwargs).content
        if return_type == "text":
            return requests.get(api_url, headers=headers, params=params, **kwargs).text
    except requests.exceptions.RequestException as error:
        print("HttpUtil.get error:", error)


def post_api(
        api_url: str,
        data: Union[dict, str] = None,
        headers: dict = "app",
        return_type: str = "json",
        **kwargs) -> Union[dict, bool, bytes, str, None]:
    try:
        if return_type == "json":
            return requests.post(api_url, headers=headers, data=data, **kwargs).json()
        if return_type == "content":
            return requests.post(api_url, headers=headers, data=data, **kwargs).content
        if return_type == "text":
            return requests.post(api_url, headers=headers, data=data, **kwargs).text
    except requests.exceptions.RequestException as error:
        print("HttpUtil.get error:", error)


def put_api(
        api_url: str,
        data: Union[dict, str] = None,
        headers: dict = "app",
        return_type: str = "json",
        **kwargs) -> Union[dict, bool, bytes, str, None]:
    try:
        if return_type == "json":
            return requests.put(api_url, headers=headers, data=data, **kwargs).json()
        if return_type == "content":
            return requests.put(api_url, headers=headers, data=data, **kwargs).content
        if return_type == "text":
            return requests.put(api_url, headers=headers, data=data, **kwargs).text
    except requests.exceptions.RequestException as error:
        print("HttpUtil.get error:", error)
