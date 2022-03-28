import threading
from instance import *
from PixivApp import *
from PixivAPI import login_pixiv, HttpUtil, UrlConstant


def get(url: str) -> dict:
    return HttpUtil.get(url).json()


# def obf_api(url: str):
#     def decorator(func):
#         @functools.wraps(func)
#         def wrapper(*args, **kwargs):
#             web_site = "https://api.obfs.dev/api/pixiv/"
#             api_url = web_site + url.replace(web_site, '')
#             # response = get(api_url)
#             return func(*args, **kwargs)
#         return wrapper
#     return decorator


def image(url: str) -> bytes:
    return HttpUtil.get(url).content


class Download:

    @staticmethod
    def save_file(file_path: str, image_name: str, image_url: str):
        if not os.path.exists(os.path.join(file_path, f'{image_name}.png')):
            time.sleep(random.random() * float(1.2))  # 随机延迟
            with open(os.path.join(file_path, f'{image_name}.png'), 'wb+') as file:
                file.write(image(image_url))
        else:
            print(f"{image_name} 已经下载过了\n")

    @staticmethod
    def save_image(image_id: str):
        file_path = Vars.cfg.data.get("save_file")
        if "http" in image_id and len(image_id) > 20:
            image_name = image_id.split("/")[-1].replace(".jpg", "")
            Download.save_file(file_path, image_name, image_id)
            return False
        info_list = PixivApp.illustration_information(image_id)
        if isinstance(info_list, list) and not isinstance(info_list, bool):
            image_url, image_name, author_id = info_list
            out_image_path = os.path.join(Vars.cfg.data.get("save_file"), author_id, image_name)
            makedirs(out_image_path)
            if type(image_url) is str:
                Download.save_file(out_image_path, image_name, image_url)
                return
            for index, url in enumerate(image_url):
                image_page_name = index_title(index, image_name)
                Download.save_file(out_image_path, image_page_name, url)

    @staticmethod
    def threading_download(image_id_list: list):
        lock_tasks_list = threading.Lock()

        def downloader():  # 多线程闭包下载函数
            nonlocal lock_tasks_list
            while image_id_list:
                if not image_id_list and len(image_id_list) == 0:
                    break
                else:
                    lock_tasks_list.acquire()
                    image_id = image_id_list.pop(0) if image_id_list else False
                    lock_tasks_list.release()
                    Download.save_image(str(image_id)) if type(image_id) is not bool else ""

        threads_pool = []
        for _ in range(Vars.cfg.data.get("max_thread")):
            th = threading.Thread(target=downloader)
            threads_pool.append(th)
            th.start()

        # wait downloader
        for th in threads_pool:
            th.join()


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
        if response.get('error') is not None:
            print("image: {}\tmsg:{}".format(works_id, response.get('error').get("user_message")))
            return False
        return response["illust"]

    @staticmethod
    def illustration_information(works_id: int):
        """插画信息 <class 'PixivApp.utils.JsonDict'>"""
        response = get(UrlConstant.IMAGE_INFORMATION.format(works_id))
        if response.get('error') is not None:
            print("image: {}\tmsg:{}".format(works_id, response.get('error').get("user_message")))
            return False
        else:
            information = response["illust"]
            image_name = remove_str(information['title'])
            page_count = information['page_count']
            author_id = str(information['user']["id"])

            print("插画名称: {}:".format(image_name))
            print("插画ID: {}".format(information["id"]))
            print("作者ID: {}".format(author_id))
            print("作者名称: {}".format(information['user']["name"]))
            print("插画标签: {}".format(list_derivation(information['tags'], "translated_name")))
            print("画集数量: {}".format(page_count))
            print("发布时间: {}\n".format(information["create_date"]))
            if page_count == 1:
                return [information['meta_single_page']['original_image_url'], image_name, author_id]
            img_url_list = [url['image_urls'].get("original") for url in information['meta_pages']]
            return [img_url_list, image_name, author_id]

    @staticmethod
    def start_information():
        """收藏插画 <class 'PixivApp.utils.JsonDict'>"""
        response = PixivToken.instantiation_api().illust_recommended()
        if response.error is None:
            image_id_list = list(set([data.id for data in response.illusts]))
            if type(image_id_list) is list and len(image_id_list) != 0:
                Download.threading_download(image_id_list)
        else:
            print(response.error)

    @staticmethod
    def recommend_information():
        """推荐插画 <class 'PixivApp.utils.JsonDict'>"""
        pixiv_app_api = PixivToken.instantiation_api()
        response = pixiv_app_api.illust_recommended()
        next_qs = pixiv_app_api.parse_qs(response.next_url)
        while next_qs is not None:
            if pixiv_app_api == 403:
                return "token invalid"
            response = pixiv_app_api.illust_recommended(**next_qs)
            if response.error is not None:
                return response.error
            image_id_list = list(set([data.id for data in response.illusts]))
            if type(image_id_list) is list and len(image_id_list) != 0:
                Download.threading_download(image_id_list)
            else:
                print("Pixiv推荐插图下载完毕")

    @staticmethod
    def follow_information():
        """关注用户信息 <class 'PixivApp.utils.JsonDict'>"""
        response = PixivToken.instantiation_api().illust_follow()
        if response.error is None:
            return list(set([illusts.user['id'] for illusts in response.illusts]))
        else:
            print(response.error)
            return response.error

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
                print(image_id_list)
                next_page = pixiv_app_api.parse_qs(response.next_url)
            else:
                return "Pixiv排行榜插图下载完毕"
