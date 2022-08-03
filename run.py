from tools.instance import *
from src import main, shell_test_pixiv_token

if __name__ == '__main__':
    try:
        main.set_update_config()
        shell_test_pixiv_token()
        main.shell_parser(main.start_parser())
    except KeyboardInterrupt:
        print("已手动退出程序")
