import logging
import random
from src.PixivUtil import *
from src.pixiv_shell import *
from src.https import HttpUtil
from tenacity import *

common_params = {"filter": "for_android"}


def return_headers(headers: str = "app"):
    if headers == "app":
        return {
            'Host': 'app-api.pixiv.net ',
            'user-agent': 'PixivAndroidApp/6.46.0',
            'authorization': "Bearer " + Vars.cfg.data.get("access_token"),
            'app-version': '6.46.0 ',
        }
    if headers == "login":
        return {"User-Agent": "PixivAndroidApp/5.0.234 (Android 11; Pixel 5)"}
    if headers == "png":
        return {'Referer': 'https://www.pixiv.net/', 'User-Agent': random.choice(UrlConstant.USER_AGENT)}
    else:
        return {'User-Agent': random.choice(UrlConstant.USER_AGENT)}


@retry(stop=stop_after_attempt(5), wait=wait_fixed(0.5))
def get(api_url: str,
        method: str = "GET",
        params: [dict, str] = None,
        head: str = "app",
        return_type: str = "json",
        params_clear: bool = False
        ) -> [dict, bytes, str, None]:  # return json or bytes or str or None (if error)
    """
    :param api_url: url
    :param method: method of request
    :param params: params of request
    :param head: headers of request
    :param return_type: return type of response
    :param params_clear: clear params of request
    :return: json or bytes or str or None (if error)
    """
    if params_clear:
        params = params.clear()
    if head == "app":
        if params is not None:
            params.update(common_params)
        api_url = UrlConstant.PIXIV_HOST + api_url.replace(UrlConstant.PIXIV_HOST, '')
    try:
        headers = return_headers(head)
        if return_type == "json":
            return HttpUtil.request(method=method, api_url=api_url, params=params, headers=headers).json()
        elif return_type == "content":
            return HttpUtil.request(method=method, api_url=api_url, params=params, headers=headers).content
        elif return_type == "text":
            return HttpUtil.request(method=method, api_url=api_url, params=params, headers=headers).text
    except Exception as error:
        logging.error(error)
        Exception("get error: {}".format(error))
