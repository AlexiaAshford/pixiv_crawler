import sys
import argparse
from tools.instance import *
import src
from src import __main__

if __name__ == '__main__':
    try:
        __main__.set_update_config()
        src.shell_test_pixiv_token()
        __main__.shell_parser(__main__.start_parser())
    except KeyboardInterrupt:
        print("已手动退出程序")
    except Exception as error:
        print("there is an error:", error)
