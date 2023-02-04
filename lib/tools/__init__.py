import os
from lib.tools import  functions, yaml_config
# from src import Image


class Vars:
    cfg = yaml_config.YamlData(file_path='pixiv-config.yaml')
    images_info = None
    images_out_path = None
    images_info_list = list()


def set_update_config():
    Vars.cfg.load()
    config_change = False
    if not isinstance(Vars.cfg.data.get('max_thread'), int):
        Vars.cfg.data['max_thread'] = 10
        config_change = True

    if not isinstance(Vars.cfg.data.get('app_version'), int):
        Vars.cfg.data['app_version'] = "6.46.0"
        config_change = True

    if not isinstance(Vars.cfg.data.get('save_file'), str):
        Vars.cfg.data['save_file'] = 'image_file'
        config_change = True

    if not isinstance(Vars.cfg.data.get('access_token'), str):
        Vars.cfg.data['access_token'] = ""
        config_change = True

    if not isinstance(Vars.cfg.data.get('refresh_token'), str):
        Vars.cfg.data['refresh_token'] = ""
        config_change = True
    if not isinstance(Vars.cfg.data.get('picture_format'), str):
        Vars.cfg.data['picture_format'] = ".png"
        config_change = True

    if not isinstance(Vars.cfg.data.get('user_id'), str):
        Vars.cfg.data['user_id'] = ""  # user id
        config_change = True

    if not isinstance(Vars.cfg.data.get('account'), str):
        Vars.cfg.data['account'] = ""  # user id
        config_change = True

    if config_change:  # if config change, save it to file and reload.
        Vars.cfg.save()

    if not os.path.exists(Vars.cfg.data.get('save_file')):
        os.mkdir(Vars.cfg.data.get('save_file'))
