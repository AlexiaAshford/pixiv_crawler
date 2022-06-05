from fake_useragent import UserAgent
from instance import *
from PixivAPI import login_pixiv, HttpUtil, UrlConstant

common_params = {"filter": "for_android"}


def return_headers(headers: str = "app"):
    if headers == "app":
        return {
            'Host': 'app-api.pixiv.net ',
            'user-agent': 'PixivAndroidApp/6.46.0',
            'authorization': "Bearer " + Vars.cfg.data.get("access_token"),
            'app-version': '6.46.0 ',
        }
    if headers == "png":
        return {'Referer': 'https://www.pixiv.net/', 'User-Agent': UserAgent(verify_ssl=False).random}
    else:
        return {'User-Agent': UserAgent(verify_ssl=False).random}


def get(
        api_url: str,
        params: [dict, str] = None,
        head: str = "app",
        types: str = "json",
        request_mode: str = "GET") -> [dict, bytes, str, None]:
    if head == "app":
        params.update(common_params)
        api_url = UrlConstant.PIXIV_HOST + api_url.replace(UrlConstant.PIXIV_HOST, '')
    try:
        if request_mode == "GET":
            return HttpUtil.get_api(api_url, params=params, return_type=types, headers=return_headers(head))
        elif request_mode == "POST":
            return HttpUtil.post_api(api_url, params=params, return_type=types, headers=return_headers(head))
        elif request_mode == "PUT":
            return HttpUtil.put_api(api_url, params=params, return_type=types, headers=return_headers(head))
    except Exception as error:
        print("post error:", error)


def refresh_pixiv_token():
    login_pixiv.refresh(Vars.cfg.data.get("refresh_token"))
    print("token失效，尝试刷新refresh_token ")


class PixivApp:

    @staticmethod
    def get_user_info(show_start: bool = False) -> bool:
        params = {"user_id": Vars.cfg.data['user_info']['id']}
        response = get(api_url=UrlConstant.ACCOUNT_INFORMATION, params=params).get('user')
        if response is not None:
            if show_start is True:
                print(f"用户名：{response.get('name')}\t\t用户id：{response.get('id')}")
            return True

    @staticmethod
    def images_information(works_id: str) -> dict:
        response = get(UrlConstant.IMAGE_INFORMATION, params={'id': works_id}, head="web")
        if isinstance(response, dict) and response.get('illust') is not None:
            return response["illust"]
        else:
            print(response)

    @staticmethod
    def start_information(user_id: [int, str] = None, restrict: str = "public", max_retry: int = 5) -> list:
        """收藏插画 """
        if user_id is None:
            user_id = Vars.cfg.data['user_info']['id']
        params = {"user_id": user_id, "restrict": restrict}

        for retry in range(1, max_retry):
            response = get(api_url=UrlConstant.BOOKMARK_INFORMATION, params=params)
            if response.get('illusts') is not None:
                return response["illusts"]
            else:
                print("Retry:{} start error:{}".format(retry, response.get("error").get("message")))
                refresh_pixiv_token()

    @staticmethod
    def recommend_information() -> list:  # 推荐插画
        params = {"include_ranking_illusts": "true", "include_privacy_policy": "true"}
        response = get(api_url=UrlConstant.RECOMMENDED_INFORMATION, params=params)
        if response.get('illusts') is not None:
            return response["illusts"]
        else:
            print("recommend error:{}".format(response.get("error").get("message")))
            refresh_pixiv_token()
            PixivApp.recommend_information()

    @staticmethod
    def follow_information(user_id: [int, str] = None, restrict: str = "public", max_retry: int = 5) -> list:
        """获取指定 user_id 关注的所有画师信息"""
        if user_id is None:
            user_id = Vars.cfg.data['user_info']['id']
        for retry in range(1, max_retry):
            params = {"user_id": user_id, "restrict": restrict}
            response = get(api_url=UrlConstant.FOLLOWING_INFORMATION, params=params)
            if response.get('user_previews') is not None:
                return response["user_previews"]
            else:
                print("Retry:{} follow_infor error:{}".format(retry, response.get("error").get("message")))
                refresh_pixiv_token()

    @staticmethod
    def author_information(author_id: str, offset: int = 30, max_retry: int = 5) -> list:  # 作者作品集
        for retry in range(1, max_retry):
            params = {"user_id": author_id, "type": "illust", "offset": offset}
            response = get(api_url=UrlConstant.AUTHOR_INFORMATION, params=params)
            if response.get('illusts') is not None:
                return response["illusts"]
            else:
                print("Retry:{} author error:{}".format(retry, response.get("error").get("message")))
                refresh_pixiv_token()

    @staticmethod
    def rank_information(max_page: int = 100, max_retry: int = 5) -> list:  # 作品排行信息
        mode_list = ["day", "week", "month", "day_male", "day_female", "week_original", "week_rookie", "day_manga",
                     "day_r18", "day_male_r18", "day_female_r18", "week_r18", "week_r18g"]
        for index, mode in enumerate(mode_list):
            print("index:", index, "\t\tmode_name:", mode)
        mode_type = mode_list[input_int(">", len(mode_list))]
        for index, page in enumerate(range(max_page), start=1):
            params = {"offset": index * 30, "mode": mode_type, "data": time.strftime("%Y-%m-%d", time.localtime())}
            for retry in range(1, max_retry):
                response = get(api_url=UrlConstant.RANKING_INFORMATION, params=params)
                if response.get('illusts') is not None:
                    return response["illusts"]
                else:
                    print("rank_information error:{}".format(retry, response.get("error").get("message")))
                    refresh_pixiv_token()


class Tag:
    """
    search_target
    partial_match_for_tags	exact_match_for_tags    title_and_caption
    标签部分一致                  标签完全一致              标题说明文

    sort
    date_desc	    date_asc    popular_desc
    按日期倒序        按日期正序    受欢迎降序(Premium功能)

    search_duration
    "within_last_day" "within_last_week" "within_last_month"
    """

    @staticmethod
    def search_tag_information(png_name: str, sort: str = "popular_desc", max_retry: int = 5) -> list:
        params = {
            "include_translated_tag_results": "true",
            "merge_plain_keyword_results": "true",
            "word": png_name,
            "sort": sort,
            "search_target": "exact_match_for_tags",
        }
        for retry in range(1, max_retry):
            response = get(api_url=UrlConstant.SEARCH_INFORMATION, params=params)
            if response.get('illusts') is not None:
                return response["illusts"]
            else:
                print("Retry:{} search error:{}".format(retry, response.get("error").get("message")))
                refresh_pixiv_token()

    @staticmethod
    def search_information(png_name: str, sort: str = "date_desc", max_retry: int = 5) -> list:
        params = {
            "include_translated_tag_results": "true",
            "merge_plain_keyword_results": "true",
            "word": png_name,
            "sort": sort,
            "search_target": "partial_match_for_tags",
        }
        for retry in range(1, max_retry):
            response = get(api_url=UrlConstant.SEARCH_INFORMATION, params=params)
            if response.get('illusts') is not None:
                return response["illusts"]
            else:
                print("Retry:{} search error:{}".format(retry, response.get("error").get("message")))
                refresh_pixiv_token()
