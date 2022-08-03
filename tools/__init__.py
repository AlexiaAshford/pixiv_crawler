from tools import instance, functions, yaml_config


class Vars:
    cfg = yaml_config.YamlData(file_path='pixiv-config.yaml')
    images_info = None
    images_out_path = None
    images_info_list = list()
