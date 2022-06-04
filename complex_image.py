import threading
from instance import *


class Complex:
    def __init__(self):
        self.images_info_obj_list = []
        self.threading_list = []
        self.threading_page = 0
        self.max_thread = Vars.cfg.data.get("max_thread")
        self.semaphore = threading.Semaphore(self.max_thread)

    def add_image_info_obj(self, image_info_obj):
        self.images_info_obj_list.append(image_info_obj)

    def start_download_threading(self):
        print("插画列表加载完毕...")
        if len(self.images_info_obj_list) != 0:
            print("开始下载, 一共:", len(self.images_info_obj_list), "幅插画\n\n")
            self.threading_list = [threading.Thread(target=self.thread_download_images, args=(images_info,))
                                   for images_info in self.images_info_obj_list]
            for thread_ing in self.threading_list:
                thread_ing.start()

            for thread_ing in self.threading_list:
                thread_ing.join()
            self.threading_list.clear()
        else:
            print("线程队列为空，没有可下载的插画！")
        self.images_info_obj_list.clear()

    def thread_download_images(self, images_info):
        self.semaphore.acquire()
        self.threading_page += 1
        images_info.show_images_information(thread_status=True)
        if images_info.page_count == 1:
            images_info.save_image(images_info.original_url)
        else:
            images_info.save_image(images_info.original_url_list)
        # print(images_info.image_name, "的作品下载完毕")
        print("下载进度:{}/{}".format(self.threading_page, len(self.images_info_obj_list)), end="\r")
        self.semaphore.release()
