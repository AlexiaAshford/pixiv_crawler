from concurrent.futures import ThreadPoolExecutor

import PixivAPI
from PixivAPI import HttpUtil
from instance import *
import threading


class ImageInfo:
    def __init__(self, result_info: dict):
        self.image_id = str(result_info["id"])
        self.author_id = str(result_info['user']["id"])
        self.author_name = remove_str(str(result_info['user']["name"]))
        self.page_count = result_info['page_count']
        self.image_name = remove_str(result_info['title'])
        self.create_date = result_info['create_date']
        self.tag_name = list_derivation(result_info['tags'], "name")
        self.original_url = result_info.get('meta_single_page', {}).get('original_image_url')
        self.original_url_list = [url['image_urls']["original"] for url in result_info.get('meta_pages')]

    def show_images_information(self):
        print("插画名称: {}:".format(self.image_name))
        print("插画序号: {}".format(self.image_id))
        print("作者名称: {}".format(self.author_name))
        print("作者序号: {}".format(self.author_id))
        print("插画标签: {}".format(self.tag_name))
        print("画集数量: {}".format(self.page_count))
        if self.page_count == 1:
            print("插画地址:{}".format(re.sub(r"pximg.net", "pixiv.cat", self.original_url)))
        else:
            for original_url in self.original_url_list:
                print("插画地址:{}".format(re.sub(r"pximg.net", "pixiv.cat", original_url)))
        print("发布时间: {}\n".format(self.create_date))

    def save_file(self, image_name: str, image_url: str):
        if Vars.cfg.data.get('save_type'):
            out_dir = os.path.join(Vars.cfg.data.get("save_file"), self.author_name, self.image_name)
        else:
            out_dir = os.path.join(Vars.cfg.data.get("save_file"), self.author_name)
        YamlData("", out_dir)
        if not os.path.exists(os.path.join(out_dir, f'{image_name}.png')):
            with open(os.path.join(out_dir, f'{image_name}.png'), 'wb+') as file:
                file.write(HttpUtil.get(image_url).content)

    def save_image(self, image_url_list):
        if isinstance(image_url_list, list):
            for index, url in enumerate(image_url_list):
                self.save_file(self.author_id + "-" + index_title(index, self.image_name), url)
        else:
            self.save_file(self.author_id + "-" + self.image_name, image_url_list)


class ThreadDownload:
    def __init__(self):
        self.threading_list = list()
        self.current_progress = 1
        self.threading_length = len(Vars.images_info_list)
        self.pool_sema = threading.BoundedSemaphore(8)

    def threading_downloader(self):
        if len(Vars.images_info_list) == 0:
            print('下载列表为空！')

        for index, images_info in enumerate(Vars.images_info_list):
            thread = threading.Thread(target=self.download_images, args=(images_info,))
            self.threading_list.append(thread)

        for thread in self.threading_list:
            thread.start()

        for thread in self.threading_list:
            thread.join()
        self.current_progress = 0

    def download_images(self, images_info):
        self.pool_sema.acquire()
        Vars.images_info = images_info
        if Vars.images_info is not None:
            if Vars.images_info.page_count == 1:
                Vars.images_info.save_image(Vars.images_info.original_url)
            else:
                Vars.images_info.save_image(Vars.images_info.original_url_list)
        print("{}/{} name:{}".format(
            self.current_progress, self.threading_length, Vars.images_info.image_name), end='\r')
        self.current_progress += 1
        self.pool_sema.release()


class ThreadGetImagesInfo:
    @staticmethod
    def threading_images_info(image_id):
        Vars.images_info = PixivAPI.PixivApp.images_information(image_id)
        if Vars.images_info is not None and isinstance(Vars.images_info, dict):
            Vars.images_info_list.append(ImageInfo(Vars.images_info))

    @staticmethod
    def get_images_info(images_id_list):
        with ThreadPoolExecutor(max_workers=5) as executor:
            for image_id in images_id_list:
                executor.submit(ThreadGetImagesInfo.threading_images_info, image_id)
