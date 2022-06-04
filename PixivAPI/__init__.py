import json
import threading
from instance import *
from PixivApp import *
from PixivAPI import login_pixiv, HttpUtil, UrlConstant


def get(url: str) -> dict:
    return HttpUtil.get(url).json()


def image(url: str) -> bytes:
    return HttpUtil.get(url).content


class PixivToken:
    @staticmethod
    def instantiation_api():
        instantiation = AppPixivAPI()
        for index, retry in enumerate(range(Vars.cfg.data.get("max_retry"))):
            instantiation.set_auth(
                access_token=Vars.cfg.data.get("access_token"),
                refresh_token=Vars.cfg.data.get("refresh_token")
            )
            if instantiation.illust_recommended().error is None:
                return instantiation

            login_pixiv.refresh(Vars.cfg.data.get("refresh_token"))
            print(f"token失效，尝试刷新refresh_token retry{index}")
            if retry >= Vars.cfg.data.get("max_retry") - 1:
                return 403


class PixivApp:

    @staticmethod
    def images_information(works_id):
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
                PixivToken.instantiation_api()

    @staticmethod
    def follow_information(user_id: [int, str] = None, restrict: str = "public", max_retry: int = 5) -> list:
        """获取指定 user_id 关注的所有画师信息"""
        if user_id is None:
            user_id = Vars.cfg.data['user_info']['id']
        params = {"filter": "for_android", "user_id": user_id, "restrict": restrict}

        for retry in range(1, max_retry):
            response = HttpUtil.get_api(api_url=UrlConstant.FOLLOWING_INFORMATION, params=params)
            if response.get('user_previews') is not None:
                return response["user_previews"]
            else:
                print("Retry:{} follow_infor error:{}".format(retry, response.get("error").get("message")))

    @staticmethod
    def author_information(author_id: str, page: int):
        """作者作品集 <class 'PixivApp.utils.JsonDict'>"""
        response = get(UrlConstant.AUTHOR_INFORMATION.format(author_id, page))
        if response.get("illusts") and response.get("error") is None:
            return [data.get("id") for data in response.get("illusts")]

    @staticmethod
    def search_information(png_name: str, page: int):
        """搜索插画 <class 'PixivApp.utils.JsonDict'>"""
        response = get(UrlConstant.SEARCH_INFORMATION(png_name, page))
        if response.get("illusts") and response.get("error") is None:
            return [data.get("id") for data in response.get("illusts")]

    @staticmethod
    def rank_information():
        """作品排行 <class 'PixivApp.utils.JsonDict'>"""
        pixiv_app_api = PixivToken.instantiation_api()
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
