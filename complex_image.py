import threading
import Image
from instance import *


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
            print("download length:{}".format(self.pool_length))
            self.threading_list = [
                threading.Thread(target=self.download_images, args=(images_info,))
                for images_info in self.images_info_obj_list
            ]
            for thread_ing in self.threading_list:  # start threading pool for download images
                thread_ing.start()  # start threading pool for download images

            for thread_ing in self.threading_list:  # wait for all threading pool finish download
                thread_ing.join()  # wait for all threading pool finish download
            self.threading_list.clear()
        else:
            print("threading pool is empty, no need to start download threading pool.")
        self.images_info_obj_list.clear()  # clear threading pool and semaphore for next download

    def download_images(self, images_info):
        self.semaphore.acquire()  # acquire semaphore to limit threading pool
        self.threading_page += 1  # threading page count + 1
        images_info.show_images_information(thread_status=True)
        if images_info.page_count == 1:
            images_info.out_put_download_image_file(images_info.original_url)
        else:
            images_info.out_put_download_image_file(images_info.original_url_list)
        # print(images_info.image_name, "的作品下载完毕")
        print("下载进度:{}/{}".format(self.threading_page, len(self.images_info_obj_list)), end="\r")
        self.semaphore.release()  # release semaphore when threading pool is empty

    def executing_multithreading(self, image_info_list: list):
        if isinstance(image_info_list, list) and len(image_info_list) != 0:  # if image_info_list is not empty list
            for illusts in image_info_list:  # add illusts to threading pool for download
                self.add_image_info_obj(Image.ImageInfo(illusts))
            self.handling_threads()  # start download threading pool for download images
        else:
            return print("get works list error:", image_info_list)
