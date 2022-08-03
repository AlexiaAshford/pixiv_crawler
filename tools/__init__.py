from tools import instance, functions, yaml_config


class Vars:
    cfg = yaml_config.YamlData(file_path='pixiv-config.yaml')
    images_info = None
    image_out_path = None
    complex_images_info = list()
    images_info_list = list()
