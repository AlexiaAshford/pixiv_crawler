from setting import *
from rich import print


class Vars:
    def __init__(self):
        pass

    cfg = Config('Pixiv-Config.conf', os.getcwd())


def remove_str(content: str):
    res_compile = re.compile(u'[\U00010000-\U0010ffff\\uD800-\\uDBFF\\uDC00-\\uDFFF]')
    return res_compile.sub("", re.sub('[/:*?"<>|]', '-', content))


def rec_id(book_id):
    book_id = book_id if 'http' not in book_id else re.findall(r'/([0-9]+)/?', book_id)[0]
    return int(book_id) if book_id.isdigit() else f'输入信息 {book_id} 不是数字或链接！'


def mkdir(file_path: str):
    if not os.path.exists(file_path):
        os.mkdir(file_path)


def input_(prompt, default=None):
    while True:
        ret = input(prompt)
        if ret != '':
            return ret
        elif default is not None:
            return default


def set_config():
    Vars.cfg.load()
    # +++++++++++++++++++++headers=======================
    if type(Vars.cfg.data("headers", "User-Agent")) is not str:
        Vars.cfg.save(
            "headers", "User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1"
        )
    if type(Vars.cfg.data("headers", "Cookie")) is not str:
        Vars.cfg.save("headers", "Cookie", "")
    if type(Vars.cfg.data("headers", "retry")) is not str:
        Vars.cfg.save("headers", "retry", "5")
    if type(Vars.cfg.data("headers", "referer")) is not str:
        Vars.cfg.save(
            "headers", "referer", "https://www.pixiv.net/ranking.php?mode=daily&content=illust"
        )
    # +++++++++++++++++++++user=======================
    if type(Vars.cfg.data("user", "max_thread")) is not str:
        Vars.cfg.save("user", "max_thread", "5")
    if type(Vars.cfg.data("user", "save_file")) is not str:
        Vars.cfg.save("user", "save_file", "pixiv")
    if type(Vars.cfg.data("user", "out_file")) is not str:
        Vars.cfg.save("user", "out_file", "downloaded")
    if type(Vars.cfg.data("user", "access_token")) is not str:
        Vars.cfg.save("user", "access_token", "")
    if type(Vars.cfg.data("user", "refresh_token")) is not str:
        Vars.cfg.save("user", "refresh_token", "")
    if type(Vars.cfg.data("user", "help")) is not str:
        Vars.cfg.save("user", "help",
                      "输入首字母\nh | help\t\t\t\t\t\t--- 显示说明\n"
                      "q | quit\t\t\t\t\t\t--- 退出正在运作的程序\n"
                      "d | picture\t\t\t\t\t\t--- 输入id或url下载插画\n"
                      "t | recommend\t\t\t\t\t\t--- 下载pixiv推荐插画\n"
                      "s | start\t\t\t\t\t\t--- 下载账号收藏插画\n"
                      "n | tag name\t\t\t\t\t\t--- 输入插画名或者表情名"
                      )
