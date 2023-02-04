import re
import sys
import src
from tools import *
from lib import start_parser


def shell_parser(command_line_args):
    shell_console = False  # if shell console is True, it will start shell console
    if command_line_args.recommend:
        src.shell_download_recommend()
        shell_console = True

    if command_line_args.ranking:
        src.shell_download_rank()
        shell_console = True

    if command_line_args.stars:
        src.shell_download_stars()
        shell_console = True

    if command_line_args.follow:
        src.shell_download_follow_author()
        shell_console = True

    if command_line_args.update:
        src.shell_read_text_id()
        shell_console = True

    if command_line_args.clear_cache:
        Vars.cfg.data.clear()
        Vars.cfg.save()
        shell_console = True  # if clear cache, it will close shell console

    if command_line_args.threading_max:
        Vars.cfg.data['max_thread'] = int(command_line_args.max)

    if command_line_args.name:
        src.shell_search(['name', command_line_args.name[0]])
        shell_console = True

    if command_line_args.download:
        src.shell_illustration(['download', command_line_args.download[0]])
        shell_console = True

    if command_line_args.author:
        src.shell_author_works(command_line_args.author[0])
        shell_console = True

    if command_line_args.login:
        src.shell_test_pixiv_token()
        shell_console = True

    if not shell_console:
        [print('[帮助]', info) for info in instance.Msg.msg_help]
        while True:  # start interactive mode for command line
            shell(re.split('\\s+', functions.input_str('>').strip()))


def shell(inputs: list):
    inputs_choice: str = inputs[0].lower()
    if inputs_choice == 'q' or inputs_choice == 'quit':
        sys.exit("已退出程序")
    elif inputs_choice == 'l' or inputs_choice == 'login':
        src.shell_test_pixiv_token()
    elif inputs_choice == 'd' or inputs_choice == 'download':
        src.shell_illustration(inputs)
    elif inputs_choice == 's' or inputs_choice == 'stars':
        src.shell_download_stars()
    elif inputs_choice == 'n' or inputs_choice == 'name':
        src.shell_search(inputs)
    elif inputs_choice == 'r' or inputs_choice == 'recommend':
        src.shell_download_recommend()
    elif inputs_choice == 'u' or inputs_choice == 'update':
        src.shell_read_text_id(inputs[1:])
    elif inputs_choice == 'k' or inputs_choice == 'rank':
        src.shell_download_rank()
    elif inputs_choice == 'f' or inputs_choice == 'follow':
        src.shell_download_follow_author()
    else:
        print(inputs_choice, "is not a valid command, please try again!")


def main():
    try:
        set_update_config()
        src.shell_test_pixiv_token()
        shell_parser(start_parser())
    except KeyboardInterrupt:
        print("已手动退出程序")


if __name__ == '__main__':
    main()
