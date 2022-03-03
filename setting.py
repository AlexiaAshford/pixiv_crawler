# 封装配置文件
import os
import random
import re
import sys
import time
import configparser
from rich import print


class Config:

    def __init__(self, filename: str, main_path: str):
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
