import argparse
import sys
from tools.instance import *
import src


def set_update_config():
    Vars.cfg.load()
    config_change = False
    if type(Vars.cfg.data.get('max_thread')) is not int:
        Vars.cfg.data['max_thread'] = 5
        config_change = True

    if Vars.cfg.data.get('save_file') is not str:
        Vars.cfg.data['save_file'] = 'image_file'
        config_change = True

    if type(Vars.cfg.data.get('access_token')) is not str:
        Vars.cfg.data['access_token'] = ""
        config_change = True

    if type(Vars.cfg.data.get('refresh_token')) is not str:
        Vars.cfg.data['refresh_token'] = ""
        config_change = True

    if type(Vars.cfg.data.get('picture_format')) is not int:
        Vars.cfg.data['picture_format'] = ".jpg"
        config_change = True

    if not isinstance(Vars.cfg.data.get('user_info'), dict):
        Vars.cfg.data['user_info'] = {}  # save user info to config file
        config_change = True

    if config_change:  # if config change, save it to file and reload.
        Vars.cfg.save()

    if not os.path.exists(Vars.cfg.data.get('save_file')):
        os.mkdir(Vars.cfg.data.get('save_file'))


def start_parser() -> argparse.Namespace:  # start parser for command line arguments and start download process
    parser = argparse.ArgumentParser()  # create parser object for command line arguments
    parser.add_argument(
        "-l", "--login",
        default=False, action="store_true", help="login to pixiv account and save token to config file"
    )  # add login argument to parser object for command line arguments
    parser.add_argument(
        "-d", "--download",
        nargs=1, default=None, help="input image id to download it"
    )  # add download argument to parser object for command line arguments for download image
    parser.add_argument(
        "-m", "--max",
        dest="threading_max", default=None, help="change max threading number"
    )  # add max argument to parser object for command line arguments for change threading max
    parser.add_argument(
        "-n", "--name",
        nargs=1, default=None, help="input search name or tag name"
    )  # add name argument to parser object for command line arguments for search
    parser.add_argument(
        "-u", "--update",
        default=False, action="store_true", help="download update local image id"
    )  # add update argument to parser object for command line arguments for download local file
    parser.add_argument(
        "-s", "--stars",
        default=False, action="store_true", help="download stars list and download all the images in the list"
    )  # add stars argument to parser object for command line arguments for download stars
    parser.add_argument(
        "-r", "--recommend",
        default=False, action="store_true", help="download pixiv recommend images"
    )  # add recommend argument to parser object for command line arguments for download recommend
    parser.add_argument(
        "-k", "--ranking",
        default=False, action="store_true", help="download ranking images"
    )  # add ranking argument to parser object for command line arguments for download ranking
    parser.add_argument(
        "-f", "--follow",
        default=False, action="store_true", help="download follow author images"
    )
    parser.add_argument(
        "-c", "--clear_cache",
        default=False, action="store_true"
    )  # add clear_cache argument to parser object for command line arguments for clear cache
    parser.add_argument(
        "-a", "--author",
        nargs=1, default=None, help="enter author id"
    )  # add author argument to parser object for command line arguments for download author
    return parser.parse_args()  # return parser object for command line arguments and return it as a tuple


def shell_parser(command_line_args: argparse.Namespace):
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
        src.shell_search(['n'] + command_line_args.name)
        shell_console = True

    if command_line_args.download:
        src.shell_illustration(['d'] + command_line_args.download)
        shell_console = True

    if command_line_args.author:
        src.shell_author_works(command_line_args.author[0])
        shell_console = True

    if command_line_args.login:
        src.shell_test_pixiv_token()
        shell_console = True

    if not shell_console:
        for info in Msg.msg_help:
            print_lang('[帮助]', info)
        while True:  # start interactive mode for command line
            shell(re.split('\\s+', src.input_str('>').strip()))


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
        print(inputs_choice, "为无效指令")


def print_lang(*args) -> None:  # print message in language set in config file
    from zhconv import convert  # import zhconv module for chinese conversion
    msg = ""  # create empty string for message to be printed
    if len(args) >= 1:  # if there is message to be printed
        for arg in args:  # for each message in args
            msg += str(arg)  # add message to string for printing
    else:  # if there is no message to be printed
        msg += args[0] if len(args) == 1 else msg  # if there is only one message to be printed, print it directly
    if Vars.cfg.data.get("lang") is None:  # if language is not set in config file
        print(convert(str(msg), 'zh-hant'))  # print message in chinese
    else:  # if language is set in config file
        print(msg)  # print message in language set in config file


def main():
    try:
        set_update_config()
        src.shell_test_pixiv_token()
        shell_parser(start_parser())
    except KeyboardInterrupt:
        print("已手动退出程序")
    except Exception as error:
        print("there is an error:", error)


if __name__ == '__main__':
    main()
