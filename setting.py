# 封装配置文件
import os
import random
import re
import sys
import time
from rich import print

import os
import yaml


class YamlData:
    def __init__(self, file):
        self.file_path = os.path.join(os.getcwd(), file)
        self.data = {}

    def load(self):
        try:
            with open(file=self.file_path, mode="r", encoding='utf-8') as f:
                self.data = yaml.load(f, Loader=yaml.FullLoader)
                if self.data is None:
                    self.data = {}
        except FileNotFoundError:
            with open(self.file_path, 'w', encoding='utf-8'):
                self.data = {}

    def save(self):
        with open(file=self.file_path, mode="w", encoding='utf-8') as f:
            yaml.safe_dump(self.data, f, default_flow_style=False, allow_unicode=True)


def mkdir(path: str):
    if not os.path.exists(path):
        os.mkdir(path)


def write_file(file_dir: str, m: str, content: str = ""):
    if m == "r":
        return open(file_dir, "r", encoding='utf-8').read()
    with open(file_dir, m, encoding='utf-8', newline="") as f:
        f.write(content)
