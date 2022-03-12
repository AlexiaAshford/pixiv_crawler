from PixivAPI import HttpUtil
from instance import *
import threading


class ImageInfo:
    def __init__(self, result_info: dict):
        self.image_id = str(result_info["id"])
        self.author_id = str(result_info['user']["id"])
        self.author_name = str(result_info['user']["name"])
        self.page_count = result_info['page_count']
        self.image_name = remove_str(result_info['title'])
        self.create_date = result_info['create_date']
        self.tag_name = list_derivation(result_info['tags'], "translated_name")
        self.original_url = result_info.get('meta_single_page', {}).get('original_image_url')
        self.original_url_list = [url['image_urls']["original"] for url in result_info.get('meta_pages')]

    def show_images_information(self):
        print("插画名称: {}:".format(self.image_name))
        print("插画ID: {}".format(self.image_id))
        print("作者ID: {}".format(self.author_id))
        print("作者名称: {}".format(self.author_name))
        print("插画标签: {}".format(self.tag_name))
        print("画集数量: {}".format(self.page_count))
        print("发布时间: {}\n".format(self.create_date))

    def save_file(self, image_name: str, image_url: str):
        out_dir = os.path.join(Vars.cfg.data("user", "save_file"), self.author_id, self.image_name)
        makedirs(out_dir)
        if not os.path.exists(os.path.join(out_dir, f'{image_name}.png')):
            time.sleep(random.random() * float(1.2))  # 随机延迟
            with open(os.path.join(out_dir, f'{image_name}.png'), 'wb+') as file:
                file.write(HttpUtil.get(image_url).content)
                return True
        else:
            return False

    def save_image(self, image_url_list):
        if isinstance(image_url_list, list):
            for index, url in enumerate(image_url_list):
                image_page_name = index_title(index, self.image_name)
                if self.save_file(image_page_name, url):
                    print("\n<{}>\t下载成功\n".format(self.image_name))
                else:
                    print(f"\n<{self.image_name}>\t已经下载过了\n")
        else:
            if self.save_file(self.image_name, image_url_list):
                print(f"\n<{self.image_name}>\t下载成功\n")
            else:
                print(f"\n<{self.image_name}>\t已经下载过了\n")


def threading_download():
    lock_tasks_list, show_tasks = threading.Lock(), threading.Lock()

    def downloader():  # 多线程闭包下载函数
        nonlocal lock_tasks_list, show_tasks
        while Vars.images_info_list:
            lock_tasks_list.acquire()
            Vars.images_info = Vars.images_info_list.pop(0) if Vars.images_info_list else None
            lock_tasks_list.release()

            if Vars.images_info is not None:
                show_tasks.acquire()
                Vars.images_info.show_images_information()
                if Vars.images_info.page_count == 1:
                    Vars.images_info.save_image(Vars.images_info.original_url)
                else:
                    Vars.images_info.save_image(Vars.images_info.original_url_list)
                show_tasks.release()

    threads_pool = []
    for _ in range(int(Vars.cfg.data("user", "max_thread"))):
        th = threading.Thread(target=downloader)
        threads_pool.append(th)
        th.start()

    # wait downloader
    for th in threads_pool:
        th.join()

# def get_image_info(works_id: int):
#     Vars.images_info = PixivAPI.PixivApp.images_information(works_id)
#     if isinstance(Vars.images_info, dict):
#         Vars.images_info = ImageInfo(Vars.images_info)
#         show_images_information()
#         if Vars.images_info.page_count == 1:
#             Vars.images_info.save_image(Vars.images_info.original_url)
#         Vars.images_info.save_image(Vars.images_info.original_url_list)


# get_image_info("91042462")
