import re
import threading
from tools import *
import src


class ImageInfo:
    def __init__(self, result_info: src.Illusts):
        self.result_info = result_info
        # self.image_id = str(result_info["id"])
        # self.author_id = str(result_info['user']["id"])
        # self.page_count = result_info['page_count']
        # self.create_date = result_info['create_date']

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

    def show_images_information(self, thread_status: bool = False):
        if not thread_status:
            print(self.description)
        Vars.images_out_path = os.path.join(Vars.cfg.data['save_file'], self.author_name)
        yaml_config.YamlData(file_dir=Vars.images_out_path)  # create a new image file

    def save_image_to_local(self, file_name: str, image_url: str):
        save_image_dir: str = os.path.join(Vars.images_out_path, file_name)  # save image file
        if not os.path.exists(save_image_dir):
            instance.TextFile.write_image(
                save_path=save_image_dir,
                image_file=src.get(api_url=image_url, head_type="png", return_type="content")
            )
        elif os.path.getsize(save_image_dir) == 0:
            print("{} is empty, retry download png file!".format(self.image_name))
            instance.TextFile.write_image(
                save_path=save_image_dir,
                image_file=src.get(api_url=image_url, head_type="png", return_type="content")
            )

    def out_put_download_image_file(self, image_url: str = None, image_url_list: list = None):
        if isinstance(image_url_list, list) and len(image_url_list) > 0:
            for index, url in enumerate(image_url_list, start=1):
                file_name = str(self.result_info.id) + "-" + str(index).rjust(4, "0") + '-' + self.image_name
                self.save_image_to_local(file_name=file_name + Vars.cfg.data['picture_format'], image_url=url)

        elif isinstance(image_url, str) and image_url != "":
            file_name = str(self.result_info.id) + "-" + self.image_name + Vars.cfg.data['picture_format']
            self.save_image_to_local(file_name=file_name, image_url=image_url)


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

    def download_images(self, images_info:ImageInfo):
        self.semaphore.acquire()  # acquire semaphore to limit threading pool
        self.threading_page += 1  # threading page count + 1
        images_info.show_images_information(thread_status=True)  # show images information
        if images_info.result_info.page_count == 1:
            images_info.out_put_download_image_file(image_url=images_info.original_url)
        else:
            images_info.out_put_download_image_file(image_url_list=images_info.original_url_list)

        self.progress_bar(len(self.images_info_obj_list), images_info.image_name)

        self.semaphore.release()  # release semaphore when threading pool is empty

    def executing_multithreading(self, image_info_list: list[src.Illusts]):
        if isinstance(image_info_list, list):  # if image_info_list is not empty list
            if len(image_info_list) != 0:
                for illusts in image_info_list:  # type: src.Illusts
                    self.add_image_info_obj(ImageInfo(illusts))
                self.handling_threads()  # start download threading pool for download images
            else:
                print("image_info_list is empty, no need to start download threading pool.")
        else:
            print("image_info_list is not list, no need to start download threading pool.")
            print("image_info_list: {}".format(image_info_list))
