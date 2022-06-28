import os
import re
import time
from rich import print
import yaml


class Msg:
    msg_help = [
        "输入首字母",
        "h | help\t\t\t\t\t\t--- 显示说明",
        "q | quit\t\t\t\t\t\t--- 退出正在运作的程序",
        "d | picture\t\t\t\t\t\t--- 输入id或url下载插画",
        "t | recommend\t\t\t\t\t--- 下载pixiv推荐插画",
        "s | start\t\t\t\t\t\t--- 下载账号收藏插画",
        "r | rank\t\t\t\t\t\t--- 下载排行榜作品",
        "n | tag name\t\t\t\t\t--- 输入插画名或者表情名",
        "u | read text pid\t\t\t\t\t--- 读取本地文本里的pid批量下载",
        "f | follow\t\t\t\t\t\t--- 下载关注的画师作品",
    ]


class YamlData:
    def __init__(self, file_path=None, file_dir=None):
        if file_dir is not None:
            self.file_dir = os.path.join(os.getcwd(), file_dir)
            if not os.path.exists(self.file_dir):
                try:
                    os.mkdir(self.file_dir)
                except (FileExistsError, OSError) as err:
                    print("file_dir：", err)

        if file_path is not None:
            self.file_path = os.path.join(os.getcwd(), file_path)
            print("file_path：", self.file_path)
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


class TextFile:
    @staticmethod
    def write(text_path: str = "", text_content: str = "", mode: str = "a") -> [str, None]:
        try:
            with open(text_path, mode, encoding="utf-8") as file:
                file.write(text_content)
        except Exception as error:
            print("[error] text_file.write:", error)

    @staticmethod
    def read(text_path: str = "", split_list: bool = False, allow_file_not_found: bool = False) -> [str, None]:
        if allow_file_not_found and not os.path.exists(text_path):
            return None
        try:
            with open(text_path, "r", encoding="utf-8") as file:
                if split_list:
                    return file.read().splitlines()
                return file.read()
        except Exception as error:
            print("[error] text_file.read:", error)

    @staticmethod
    def write_image(save_path: str, image_file: str, mode: str = "wb+") -> None:
        if image_file is not None:
            try:
                with open(save_path, mode) as file:  # wb+:二进制写入
                    file.write(image_file)  # write binary data to file
            except Exception as error:
                print("[error] text_file.write_image:", error)
        else:
            print("[error] text_file.write_image: image_file is None", image_file)


class Vars:
    cfg = YamlData(file_path='pixiv-config.yaml')
    images_info = None
    image_out_path = None
    complex_images_info = list()
    images_info_list = list()


def count_time(func: callable) -> callable:
    def wrapper(*arg, **kwargs):
        start_time = time.time()
        result = func(*arg, **kwargs)
        print(f"下载耗时:{time.time() - start_time:.2f}s")
        return result

    return wrapper


def remove_str(content: str):
    res_compile = re.compile(u'[\U00010000-\U0010ffff\\uD800-\\uDBFF\\uDC00-\\uDFFF]')
    return res_compile.sub("", re.sub('[/:*?"<>|x08]', '-', content))


def rec_id(book_id: str):
    book_id = book_id if 'http' not in book_id else re.findall(r'/(\d+)/?', book_id)[0]
    return str(book_id) if book_id.isdigit() else f'输入信息 {book_id} 不是数字或链接！'


def index_title(division_index: int, image_name: str):
    return str(division_index).rjust(4, "0") + '-' + str(image_name)


def input_str(prompt, default=None):
    while True:
        ret = input(prompt)
        if ret != '':
            return ret
        elif default is not None:
            return default


def input_int(prompt: str, max_number: int = None):
    while True:
        ret = input(prompt)
        if ret.isdigit():
            if max_number is None:
                return int(ret)
            if max_number is not None and int(ret) < max_number:
                return int(ret)
            else:
                print(f"输入数字 {ret} 需要小于索引 {max_number} ")
                continue
        else:
            if ret.strip() != '':
                print(f"输入的内容 {ret} 不是数字，请重新输入")
