# 封装配置文件
import os
import random
import re
import time
import configparser
from rich import print


def input_(prompt, default=None):
    while True:
        ret = input(prompt)
        if ret != '':
            return ret
        elif default is not None:
            return default


class Config:

    def __init__(self, filename):
        self.filename = filename
        self.config = configparser.ConfigParser()

    def load(self):
        try:
            self.config.read(self.filename, encoding="utf-8-sig")
        except configparser.ParsingError as error:
            print("ERROR:{}".format(error))
            with open(self.filename, 'w') as configfile:
                configfile.write("")

    def data(self, key, value):
        try:
            return self.config.get(key, value)
        except:
            print("No section or Option!", key, value)

    def save(self, config_key, save_key, save_data):
        if not self.config.has_section(config_key):
            # 增加section
            self.config.add_section(config_key)

        # 增加key-value
        self.config.set(config_key, save_key, save_data)
        # 将配置写入文件
        with open(self.filename, 'w', encoding="utf-8") as configfile:
            self.config.write(configfile)


def set_config():
    conf = Config(os.path.join(os.getcwd(), 'config.ini'))
    conf.load()
    # +++++++++++++++++++++headers=======================
    if type(conf.data("headers", "User-Agent")) is not str:
        conf.save(
            "headers", "User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1"
        )
    if type(conf.data("headers", "Cookie")) is not str:
        conf.save("headers", "Cookie", "")
    if type(conf.data("headers", "retry")) is not str:
        conf.save("headers", "retry", "5")
    if type(conf.data("headers", "referer")) is not str:
        conf.save(
            "headers", "referer", "https://www.pixiv.net/ranking.php?mode=daily&content=illust"
        )
    # +++++++++++++++++++++user=======================
    if type(conf.data("user", "max_thread")) is not str:
        conf.save("user", "max_thread", "5")
    if type(conf.data("user", "save_file")) is not str:
        conf.save("user", "save_file", "pixiv")
    if type(conf.data("user", "out_file")) is not str:
        conf.save("user", "out_file", "downloaded")
    if type(conf.data("user", "access_token")) is not str:
        conf.save("user", "access_token", "")
    if type(conf.data("user", "refresh_token")) is not str:
        conf.save("user", "refresh_token", "")
    if type(conf.data("user", "help")) is not str:
        conf.save("user", "help",
                  "输入首字母\nh | help\t\t\t\t\t\t--- 显示说明\n"
                  "q | quit\t\t\t\t\t\t--- 退出正在运作的程序\n"
                  "d | picture\t\t\t\t\t\t--- 输入id或url下载插画\n"
                  "t | recommend\t\t\t\t\t\t--- 下载pixiv推荐插画\n"
                  "s | start\t\t\t\t\t\t--- 下载账号收藏插画\n"
                  "n | tag name\t\t\t\t\t\t--- 输入插画名或者表情名"
                  )

    return conf
