from tools.instance import *
from src import __main__, shell_test_pixiv_token

if __name__ == '__main__':
    try:
        __main__.set_update_config()
        shell_test_pixiv_token()
        __main__.shell_parser(__main__.start_parser())
    except KeyboardInterrupt:
        print("已手动退出程序")
