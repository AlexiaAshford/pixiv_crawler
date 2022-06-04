import json
from instance import *
from PixivApp import *
from PixivAPI import login_pixiv, HttpUtil, UrlConstant


def get(url: str) -> dict:
    return HttpUtil.get(url).json()


def image(url: str) -> bytes:
    return HttpUtil.get(url).content


def refresh_pixiv_token():
    login_pixiv.refresh(Vars.cfg.data.get("refresh_token"))
    print(f"token失效，尝试刷新refresh_token ")


class PixivApp:

    @staticmethod
    def get_user_info(show_start: bool = False) -> bool:
        params = {"filter": "for_android", "user_id": Vars.cfg.data['user_info']['id']}
        response = HttpUtil.get_api(api_url=UrlConstant.ACCOUNT_INFORMATION, params=params).get('user')
        if response is not None:
            if show_start is True:
                print(f"用户名：{response.get('name')}\t\t用户id：{response.get('id')}")
            return True

        return False

    @staticmethod
    def images_information(works_id: str) -> dict:
        response = get(UrlConstant.IMAGE_INFORMATION.format(works_id))
        if response.get('error') is None:
            return response["illust"]

    @staticmethod
    def illustration_information(works_id: int):
        """插画信息 <class 'PixivApp.utils.JsonDict'>"""
        response = get(UrlConstant.IMAGE_INFORMATION.format(works_id))
        if response.get('error') is None:
            information = response["illust"]
            image_name = remove_str(information['title'])
            page_count = information['page_count']
            author_id = str(information['user']["id"])
            print("插画名称: {}:".format(image_name))
            print("插画ID: {}".format(information["id"]))
            print("作者ID: {}".format(author_id))
            print("作者名称: {}".format(information['user']["name"]))
            print("插画标签: {}".format(i for i in information['tags']))
            print("画集数量: {}".format(page_count))
            print("发布时间: {}\n".format(information["create_date"]))
            if page_count == 1:
                return [information['meta_single_page']['original_image_url'], image_name, author_id]
            img_url_list = [url['image_urls'].get("original") for url in information['meta_pages']]
            return [img_url_list, image_name, author_id]

    @staticmethod
    def start_information(user_id: [int, str] = None, restrict: str = "public", max_retry: int = 5) -> list:
        """收藏插画 """
        if user_id is None:
            user_id = Vars.cfg.data['user_info']['id']
        params = {"filter": "for_android", "user_id": user_id, "restrict": restrict}

        for retry in range(1, max_retry):
            response = HttpUtil.get_api(api_url=UrlConstant.BOOKMARK_INFORMATION, params=params)
            if response.get('illusts') is not None:
                return response["illusts"]
            else:
                print("Retry:{} start error:{}".format(retry, response.get("error").get("message")))
                refresh_pixiv_token()

    @staticmethod
    def recommend_information(ranking: bool = True, policy: bool = True, max_retry: int = 5) -> list:
        """推荐插画 """
        params = json.dumps({
            "filter": "for_android",
            "include_ranking_illusts": ranking,
            "include_privacy_policy": policy
        })
        for retry in range(1, max_retry):
            response = HttpUtil.get_api(api_url=UrlConstant.RECOMMENDED_INFORMATION, params=params)
            if response.get('illusts') is not None:
                return response["illusts"]
            else:
                print("Retry:{} recommend error:{}".format(retry, response.get("error").get("message")))
                refresh_pixiv_token()

    @staticmethod
    def follow_information(user_id: [int, str] = None, restrict: str = "public", max_retry: int = 5) -> list:
        """获取指定 user_id 关注的所有画师信息"""
        if user_id is None:
            user_id = Vars.cfg.data['user_info']['id']
        for retry in range(1, max_retry):
            params = {"filter": "for_android", "user_id": user_id, "restrict": restrict}
            response = HttpUtil.get_api(api_url=UrlConstant.FOLLOWING_INFORMATION, params=params)
            if response.get('user_previews') is not None:
                return response["user_previews"]
            else:
                print("Retry:{} follow_infor error:{}".format(retry, response.get("error").get("message")))

    @staticmethod
    def author_information(author_id: str, offset: int = 30, max_retry: int = 5) -> list:
        """作者作品集 """
        for retry in range(1, max_retry):
            params = {"filter": "for_android", "user_id": author_id, "type": "illust", "offset": offset}
            response = HttpUtil.get_api(api_url=UrlConstant.AUTHOR_INFORMATION, params=params)
            if response.get('illusts') is not None:
                return response["illusts"]
            else:
                print("Retry:{} author error:{}".format(retry, response.get("error").get("message")))

    @staticmethod
    def search_information(png_name: str, page: int):
        """搜索插画 <class 'PixivApp.utils.JsonDict'>"""
        response = get(UrlConstant.SEARCH_INFORMATION(png_name, page))
        if response.get("illusts") and response.get("error") is None:
            return [data.get("id") for data in response.get("illusts")]

    @staticmethod
    def rank_information():
        """作品排行 <class 'PixivApp.utils.JsonDict'>"""
        pixiv_app_api = refresh_pixiv_token()
        # mode: [day, week, month, day_male, day_female, week_original, week_rookie, day_manga]
        # date: '2016-08-01'
        # mode (Past): [day, week, month, day_male, day_female, week_original, week_rookie,
        #               day_r18, day_male_r18, day_female_r18, week_r18, week_r18g]
        next_page = {"mode": "day"}
        while next_page:
            response = pixiv_app_api.illust_ranking(**next_page)
            if response.error is not None:
                return response.error
            image_id_list = list(set([data.id for data in response.illusts]))
            if type(image_id_list) is list and len(image_id_list) != 0:
                next_page = pixiv_app_api.parse_qs(response.next_url)
            else:
                return "Pixiv排行榜插图下载完毕"
