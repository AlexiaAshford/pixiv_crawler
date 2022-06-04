from PixivAPI import HttpUtil
from instance import *


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
