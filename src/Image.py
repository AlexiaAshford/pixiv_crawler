import os
import re
import threading
from tools import *
import src


class ImageInfo:
    def __init__(self, result_info: dict):
        self.result_info = result_info
        self.image_id = str(result_info["id"])
        self.author_id = str(result_info['user']["id"])
        self.author_name = functions.remove_str(str(result_info['user']["name"]))
        self.page_count = result_info['page_count']
        self.image_name = functions.remove_str(result_info['title'])
        self.create_date = result_info['create_date']
        self.tag_name = ' '.join([data["name"] for data in result_info['tags'] if data["name"]])
        self.original_url = result_info.get('meta_single_page', {}).get('original_image_url')
        self.original_url_list = [url['image_urls']["original"] for url in result_info.get('meta_pages')]

    def show_images_information(self, thread_status: bool = False):
        if not thread_status:
            print("插画名称: {}:".format(self.image_name))
            print("插画序号: {}".format(self.image_id))
            print("作者名称: {}".format(self.author_name))
            print("作者序号: {}".format(self.author_id))
            print("插画标签: {}".format(self.tag_name))
            print("画集数量: {}".format(self.page_count))
            if self.page_count == 1:
                print("插画地址:{}".format(re.sub(r"pximg.net", "pixiv.cat", self.original_url)))
            else:
                for index, original_url in enumerate(self.original_url_list, start=1):
                    print("画集{}:{}".format(index, re.sub(r"pximg.net", "pixiv.cat", original_url)))
            print("发布时间: {}\n".format(self.create_date))

        Vars.image_out_path = os.path.join(Vars.cfg.data['save_file'], self.author_name)
        yaml_config.YamlData(file_dir=Vars.image_out_path)  # create a new image file

    def save_image_to_local(self, file_name: str, image_url: str):
        save_image_dir: str = os.path.join(Vars.image_out_path, file_name)  # save image file
        if not os.path.exists(save_image_dir):
            instance.TextFile.write_image(
                save_path=save_image_dir,
                image_file=src.get(api_url=image_url, head="png", return_type="content")
            )
        elif os.path.getsize(save_image_dir) == 0:
            print("{} is empty, retry download png file!".format(self.image_name))
            instance.TextFile.write_image(
                save_path=save_image_dir,
                image_file=src.get(api_url=image_url, head="png", return_type="content")
            )

    def out_put_download_image_file(self, image_url: str = None, image_url_list: list = None):
        if isinstance(image_url_list, list) and len(image_url_list) > 0:
            for index, url in enumerate(image_url_list, start=1):
                file_name = self.image_id + "-" + str(index).rjust(4, "0") + '-' + self.image_name
                self.save_image_to_local(file_name=file_name + Vars.cfg.data['picture_format'], image_url=url)

        elif isinstance(image_url, str) and image_url != "":
            file_name = self.image_id + "-" + self.image_name + Vars.cfg.data['picture_format']
            self.save_image_to_local(file_name=file_name, image_url=image_url)


class Multithreading:
    def __init__(self):
        self.threading_list = []
        self.threading_page = 0
        self.images_info_obj_list = []
        self.pool_length = 0
        self.max_thread = Vars.cfg.data.get("max_thread")
        self.semaphore = threading.Semaphore(self.max_thread)

    def add_image_info_obj(self, image_info_obj):
        self.images_info_obj_list.append(image_info_obj)  # add image_info_obj to threading pool
        self.pool_length += 1  # pool length + 1 if add image_info_obj to threading pool

    def handling_threads(self):
        if len(self.images_info_obj_list) != 0:
            print("download {} images~ ".format(self.pool_length))
            self.threading_list = [
                threading.Thread(target=self.download_images, args=(image_info_obj,))
                for image_info_obj in self.images_info_obj_list
            ]
            for thread_ing in self.threading_list:  # start threading pool for download images
                thread_ing.start()  # start threading pool for download images

            for thread_ing in self.threading_list:  # wait for all threading pool finish download
                thread_ing.join()  # wait for all threading pool finish download
            self.threading_list.clear()
        else:
            print("threading pool is empty, no need to start download threading pool.")
        self.images_info_obj_list.clear()  # clear threading pool and semaphore for next download

    def progress_bar(self, total_length: int, images_name: str) -> None:  # progress bar
        percentage = int(100 * self.threading_page / total_length)
        print("progress: {}/{}\tpercentage: {}%\tname: {}".format(
            self.threading_page, total_length, percentage, images_name),
            end="\r")  # print progress bar for download images in threading pool

    def download_images(self, images_info):
        self.semaphore.acquire()  # acquire semaphore to limit threading pool
        self.threading_page += 1  # threading page count + 1
        images_info.show_images_information(thread_status=True)  # show images information
        if images_info.page_count == 1:
            images_info.out_put_download_image_file(image_url=images_info.original_url)
        else:
            images_info.out_put_download_image_file(image_url_list=images_info.original_url_list)

        self.progress_bar(len(self.images_info_obj_list), images_info.image_name)

        self.semaphore.release()  # release semaphore when threading pool is empty

    def executing_multithreading(self, image_info_list: list):
        if isinstance(image_info_list, list) and len(image_info_list) != 0:  # if image_info_list is not empty list
            for illusts in image_info_list:  # add illusts to threading pool for download
                self.add_image_info_obj(ImageInfo(illusts))
            self.handling_threads()  # start download threading pool for download images
        else:
            return print("get works list error:", image_info_list)
