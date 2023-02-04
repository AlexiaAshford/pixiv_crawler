import re
import src
import base64
import database
import threading
from lib.tools import *
from rich import print
import pixiv_template
from concurrent.futures import ThreadPoolExecutor


class ImageInfo:
    def __init__(self, result_info):
        if isinstance(result_info, dict):
            # try:
            #     self.result_info = pixiv_template.Illusts(**result_info)
            # except Exception as e:
            #     print("result_info type error, it must be dict or Illusts:", result_info)
            #     print(e)
            # print(self.result_info)
            self.result_info = pixiv_template.Illusts(**result_info)
        elif isinstance(result_info, pixiv_template.Illusts):
            self.result_info = result_info
        else:
            raise Exception("result_info type error, it must be dict or Illusts:", type(result_info))

    @property
    def tag_name(self) -> str:  # get tag name
        return ' '.join([data.name for data in self.result_info.tags if data.name])

    @property
    def original_url_list(self) -> list:  # get original image url list
        return [url['image_urls']["original"] for url in self.result_info.meta_pages]

    @property
    def original_url(self) -> str:  # get original url
        return self.result_info.meta_single_page.original_image_url

    @property
    def image_name(self) -> str:  # get image name
        res_compile = re.compile(u'[\U00010000-\U0010ffff\\uD800-\\uDBFF\\uDC00-\\uDFFF]')
        return res_compile.sub("", re.sub('[/:*?"<>|x08]', '#', str(self.result_info.title)))

    @property
    def author_name(self) -> str:  # author name
        res_compile = re.compile(u'[\U00010000-\U0010ffff\\uD800-\\uDBFF\\uDC00-\\uDFFF]')
        return res_compile.sub("", re.sub('[/:*?"<>|x08]', '#', str(self.result_info.user.name)))

    @property
    def description(self) -> str:  # get description
        description_info = "插画名称: {}:\n插画序号: {}\n".format(self.image_name, self.result_info.id)
        description_info += "作者名称: {}\n作者序号: {}\n".format(self.author_name, self.result_info.user.id)
        description_info += "插画标签: {}\n画集数量: {}".format(self.tag_name, self.result_info.page_count)
        if self.result_info.page_count == 1:
            description_info += "\n插画地址:{}".format(re.sub(r"pximg.net", "pixiv.cat", self.original_url))
        else:
            for index, original_url in enumerate(self.original_url_list, start=1):
                description_info += "\n画集{}:{}".format(index, re.sub(r"pximg.net", "pixiv.cat", original_url))
        description_info += "\n发布时间: {}\n".format(self.result_info.create_date)
        return description_info

    def save_image_to_local(self, image_url: str):
        print("start download image: {}".format(self.result_info.title))
        image_id = image_url.split("/")[-1].replace(".jpg", "").replace(".png", "")
        try:
            database.session.add(database.ImageDB(
                id=image_id,
                image_title=self.result_info.title,
                image_caption=self.result_info.caption,
                image_author=self.result_info.user.name,
                image_author_id=self.result_info.user.id,
                image_tags=self.tag_name,
                image_url=image_url,
                image_page_count=self.result_info.page_count,
                image_create_date=self.result_info.create_date,
                cover=base64.b64encode(src.get(api_url=image_url, head_type="png", return_type="content")).decode()
            ))  # add data to database
        except Exception as e:
            print("Error: {}".format(e))
            self.save_image_to_local(image_url=image_url)


class Multithreading:
    def __init__(self):
        self.threading_list = []
        self.pool_length = 0
        self.threading_page = 0
        self.images_info_obj_list = []
        self.semaphore = threading.Semaphore(self.max_thread_number)

    @property
    def max_thread_number(self) -> int:
        max_thread_number = Vars.cfg.data["max_thread"]
        if max_thread_number == 0:
            max_thread_number = 16
        elif max_thread_number > 64:
            max_thread_number = 64
        return max_thread_number

    def add_image_info_obj(self, image_info_obj):
        self.images_info_obj_list.append(image_info_obj)  # add image_info_obj to threading pool
        self.pool_length += 1  # pool length + 1 if add image_info_obj to threading pool

    # def handling_threads(self):
    #     if len(self.images_info_obj_list) != 0:
    #         print("download {} images~ ".format(self.pool_length))
    #         self.threading_list = [
    #             threading.Thread(target=self.download_images, args=(image_info_obj,))
    #             for image_info_obj in self.images_info_obj_list
    #         ]
    #         for thread_ing in self.threading_list:  # start threading pool for download images
    #             thread_ing.start()  # start threading pool for download images
    #
    #         for thread_ing in self.threading_list:  # wait for all threading pool finish download
    #             thread_ing.join()  # wait for all threading pool finish download
    #         self.threading_list.clear()
    #     else:
    #         print("threading pool is empty, no need to start download threading pool.")
    #     self.images_info_obj_list.clear()  # clear threading pool and semaphore for next download

    # def progress_bar(self, total_length: int, images_name: str) -> None:  # progress bar
    #     percentage = int(100 * self.threading_page / total_length)
    #     print("progress: {}/{}\tpercentage: {}%\tname: {}".format(
    #         self.threading_page, total_length, percentage, images_name),
    #         end="\r")  # print progress bar for download images in threading pool

    # def download_images(self, images_info: ImageInfo):
    #     self.semaphore.acquire()  # acquire semaphore to limit threading pool
    #     self.threading_page += 1  # threading page count + 1
    #     images_info.show_images_information(thread_status=True)  # show images information
    #     if images_info.result_info.page_count == 1:
    #         images_info.out_put_download_image_file(image_url=images_info.original_url)
    #     else:
    #         images_info.out_put_download_image_file(image_url_list=images_info.original_url_list)
    #
    #     self.progress_bar(len(self.images_info_obj_list), images_info.image_name)
    #
    #     self.semaphore.release()  # release semaphore when threading pool is empty

    def executing_multithreading(self, image_info_list: list):
        download_list = []
        if len(image_info_list) == 0:
            return print("image_info_list is empty, no need to start download threading pool.")
        for illusts in image_info_list:
            illust_info = ImageInfo(illusts)
            if illust_info.result_info.page_count == 1:
                image_id = illust_info.original_url.split("/")[-1].replace(".jpg", "").replace(".png", "")
                # check image is exist in database
                if not database.session.query(database.ImageDB).filter(database.ImageDB.id == image_id).first():
                    download_list.append([illust_info, illust_info.original_url])
            else:
                for image_url in illust_info.original_url_list:
                    image_id = image_url.split("/")[-1].replace(".jpg", "").replace(".png", "")
                    # check image is exist in database
                    if not database.session.query(database.ImageDB).filter(database.ImageDB.id == image_id).first():
                        download_list.append([illust_info, image_url])

            self.add_image_info_obj(illust_info)

        print("download {} images~ ".format(len(download_list)))
        # start download threading pool for download images
        with ThreadPoolExecutor(max_workers=self.max_thread_number) as executor:
            for illusts, url in download_list:  # type: ImageInfo, str
                executor.submit(illusts.save_image_to_local, url)
        database.session.commit()  # commit database
        return True
        # self.handling_threads()  # start download threading pool for download images
