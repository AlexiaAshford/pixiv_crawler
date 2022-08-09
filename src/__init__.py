import json
import random
from src.pixiv import *
from src.pixiv_shell import *
from src.https import HttpUtil
from tenacity import *

common_params = {"filter": "for_android"}


def header(headers: str = "app"):
    if headers == "app":
        return {
            'Host': 'app-api.pixiv.net ',
            'user-agent': 'PixivAndroidApp/{} (Android 11; Pixel 5)'.format(Vars.cfg.data['app_version']),
            'authorization': "Bearer " + Vars.cfg.data.get("access_token"),
            'app-version': Vars.cfg.data['app_version'],
        }
    if headers == "login":
        return {"User-Agent": "PixivAndroidApp/{} (Android 11; Pixel 5)".format(Vars.cfg.data['app_version'])}
    if headers == "png" or headers == "jpg":
        # download from pixiv image need to add Referer:'https://www.pixiv.net/
        return {'Referer': 'https://www.pixiv.net/', 'User-Agent': random.choice(UrlConstant.USER_AGENT)}
    else:
        return {'User-Agent': random.choice(UrlConstant.USER_AGENT)}


@retry(stop=stop_after_attempt(5), wait=wait_fixed(0.5))
def get(api_url: str,
        method: str = "GET",
        params: [dict, str] = None,
        head_type: str = "app",
        dumps: bool = False,
        return_type: str = "json",
        params_clear: bool = False
        ) -> [dict, bytes, str, None]:  # return json or bytes or str or None (if error)
    """
    :param dumps: if False, return json.dumps(json_str)
    :param api_url: url
    :param method: method of request
    :param params: params of request
    :param head_type: headers of request
    :param return_type: return type of response
    :param params_clear: clear params of request
    :return: json or bytes or str or None (if error)
    """
    if method not in ["GET", "POST", "PUT", "DELETE"]:
        raise Exception("method is not in ['GET', 'POST', 'PUT', 'DELETE']")

    if params_clear:
        params = params.clear()

    if head_type == "app":
        params.update(common_params) if params is not None else common_params
        api_url = UrlConstant.PIXIV_HOST + api_url.replace(UrlConstant.PIXIV_HOST, '')

    if dumps and isinstance(params, dict):  # dump params to string json
        params = json.dumps(params)

    try:
        response = HttpUtil.request(method=method, api_url=api_url, params=params, headers=header(head_type))
        if return_type == "json" or return_type == "dict":
            return response.json()
        elif return_type == "content" or return_type == "png":
            return response.content
        elif return_type == "text" or return_type == "str":
            return response.text
    except Exception as error:  # if error, return None
        Exception("get error: {}".format(error))
