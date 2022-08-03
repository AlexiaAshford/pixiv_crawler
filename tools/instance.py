import os
from rich import print



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
            print("[error] text_file.write_image:", image_file)
