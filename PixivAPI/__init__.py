from setting import *
import threading
from PixivApp import *
from PixivAPI import login_pixiv, HttpUtil

config = set_config()


def remove_str(content: str):
    res_compile = re.compile(u'[\U00010000-\U0010ffff\\uD800-\\uDBFF\\uDC00-\\uDFFF]')
    return res_compile.sub("", re.sub('[/:*?"<>|]', '-', content))


def rec_id(book_id):
    book_id = book_id if 'http' not in book_id else re.findall(r'/([0-9]+)/?', book_id)[0]
    return int(book_id) if book_id.isdigit() else f'输入信息 {book_id} 不是数字或链接！'


def mkdir(file_path: str):
    if not os.path.exists(file_path):
        os.mkdir(file_path)


class Download:
    @staticmethod
    def save_image(image_id: int):
        response = PixivApp.illustration_information(image_id)
        if not response.get("message") and response.get("token") is None:
            image_name = remove_str(response.title)
            file_path = config.data("user", "save_file")
            if not os.path.exists(os.path.join(file_path, f'{image_name}.png')):
                time.sleep(random.random() * float(1.2))  # 随机延迟
                with open(os.path.join(file_path, f'{image_name}.png'), 'wb+') as file:
                    file.write(HttpUtil.get(response.image_urls['large']).content)
                    print('成功下载图片：{}\n'.format(image_name))
            else:
                print(f"{image_name} 已经下载过了\n")
        else:
            print(response.get("message"), "token invalid")

    @staticmethod
    def threading_download(image_id_list: list):
        image_id_len = len(image_id_list)
        lock_tasks_list = threading.Lock()
        print(f"开始下载，一共 {image_id_len} 张图片")

        # 生成下载队列.
        def downloader():
            """多线程下载函数"""
            nonlocal lock_tasks_list

            while image_id_list:
                lock_tasks_list.acquire()
                image_id = image_id_list.pop()
                print("正在下载第{}张".format(image_id_len - len(image_id_list)))
                lock_tasks_list.release()
                Download.save_image(image_id)

        threads_pool = []
        for _ in range(int(config.data("user", "max_thread"))):
            th = threading.Thread(target=downloader)
            threads_pool.append(th)
            th.start()

        # wait downloader
        for th in threads_pool:
            th.join()


class PixivToken:
    @staticmethod
    def instantiation_api(max_retry=config.data("headers", "retry")):
        instantiation = AppPixivAPI()
        for index, retry in enumerate(range(int(max_retry))):
            instantiation.set_auth(
                access_token=config.data("user", "access_token"),
                refresh_token=config.data("user", "refresh_token")
            )
            if instantiation.illust_recommended().error is None:
                return instantiation

            login_pixiv.refresh(config.data("user", "refresh_token"))
            print(f"token失效，尝试刷新refresh_token retry{index}")
            if retry >= int(max_retry) - 1:
                return 403




class PixivApp:

    @staticmethod
    def start_information():
        """收藏插画 <class 'PixivApp.utils.JsonDict'>"""
        response = PixivToken.instantiation_api().illust_recommended()
        if response.error is None:
            return response.illusts
        return response.error

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
            return list(set([data.id for data in response.illusts]))
        return response.error

    @staticmethod
    def author_information(author_id: str):
        """作者作品集 <class 'PixivApp.utils.JsonDict'>"""
        response = PixivToken.instantiation_api().user_illusts(author_id)
        if response.error is None:
            return list(set([data.id for data in response.illusts]))
        return response.error

    @staticmethod
    def search_information(png_name: str, search_target: str):
        """搜搜插画 <class 'PixivApp.utils.JsonDict'>"""
        response = PixivToken.instantiation_api().search_illust(
            word=png_name, search_target=search_target
        )
        if response.error is None:
            return list(set([data.id for data in response.illusts]))
        return response.error

    @staticmethod
    def illustration_information(works_id: int):
        """插画信息 <class 'PixivApp.utils.JsonDict'>"""

        pixiv_app_api = PixivToken.instantiation_api()
        if pixiv_app_api == 403:
            return {"token": 403}
        response = pixiv_app_api.illust_detail(works_id)
        if response.error is None:
            tags_llist = [i['name'] for i in response.illust['tags']]
            print("插画名称: {}:".format(response.illust.title))
            print("插画ID: {}".format(response.illust.id))
            print("作者名称: {}".format(response.illust.user['name']))
            print("插画标签: {}".format(', '.join(tags_llist)))
            print("发布时间: {}\n".format(response.illust.create_date))
            return response.illust
        return response.error
