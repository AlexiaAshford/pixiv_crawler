from instance import *
import scr


class ImageInfo:
    def __init__(self, result_info: dict):
        self.image_id = str(result_info["id"])
        self.author_id = str(result_info['user']["id"])
        self.author_name = remove_str(str(result_info['user']["name"]))
        self.page_count = result_info['page_count']
        self.image_name = remove_str(result_info['title'])
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
        YamlData(file_dir=Vars.image_out_path)  # create a new image file

    def save_image_to_local(self, file_name: str, image_url: str):
        save_image_dir: str = os.path.join(Vars.image_out_path, file_name)
        if not os.path.exists(save_image_dir):
            TextFile.write_image(
                save_path=save_image_dir,
                image_file=scr.get(api_url=image_url, head="png", types="content")
            )
        elif os.path.getsize(save_image_dir) == 0:
            print("{} is empty, retry download png file!".format(self.image_name))
            TextFile.write_image(
                save_path=save_image_dir,
                image_file=scr.get(api_url=image_url, head="png", types="content")
            )

    def out_put_download_image_file(self, image_url: str = None, image_url_list: list = None):
        if isinstance(image_url_list, list) and len(image_url_list) > 0:
            for index, url in enumerate(image_url_list, start=1):
                file_name = self.image_id + "-" + str(index).rjust(4, "0") + '-' + self.image_name
                self.save_image_to_local(file_name=file_name, image_url=url)

        elif isinstance(image_url, str) and image_url != "":
            self.save_image_to_local(file_name=self.image_id + "-" + self.image_name + ".png", image_url=image_url)
