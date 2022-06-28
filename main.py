import argparse
import sys
import Image
from instance import *
from rich.progress import track
import scr


def shell_author_works(author_id: str, next_url: str = ""):  # download author images save to local
    while True:
        if next_url is None:  # if next_url is None, it means that it is download complete
            return print("the end of author_works list")
        if next_url == "":  # if next_url is empty, it means it is the first time to download author works list
            image_info_list, next_url = scr.PixivApp.author_information(author_id=author_id)
        else:  # if next_url is not empty, it means it is the next time to download author works list
            image_info_list, next_url = scr.PixivApp.author_information(api_url=next_url)
        # # start download threading pool for download images from author works list
        Image.Multithreading().executing_multithreading(image_info_list)


@count_time
def shell_illustration(inputs):
    if len(inputs) >= 2:
        Vars.images_info = scr.PixivApp.images_information(scr.rec_id(inputs[1]))
        if isinstance(Vars.images_info, dict):
            Vars.images_info = Image.ImageInfo(Vars.images_info)
            Vars.images_info.show_images_information()
            if Vars.images_info.page_count == 1:
                Vars.images_info.out_put_download_image_file(image_url=Vars.images_info.original_url)
            else:
                Vars.images_info.out_put_download_image_file(image_url_list=Vars.images_info.original_url_list)
        else:
            print("没有找到相应的作品！")
    else:
        print("你没有输入id或者链接")


@count_time
def shell_search(inputs: list):
    if len(inputs) < 2:  # if there is no search keyword input
        return print("没有输入搜索信息")  # print error message
    # start download threading pool for download images from search list and save to local
    Image.Multithreading().executing_multithreading(scr.Tag.search_information(png_name=inputs[1]))


@count_time
def shell_download_follow_author(next_url: str = ""):
    while True:
        if next_url is None:  # if next_url is None, it means that it is download complete
            return print("the end of follow list")
        if next_url == "":  # if next_url is empty, it means it is the first time to download author works list
            follow_list, next_url = scr.PixivApp.follow_information()
        else:  # if next_url is not empty, it means it is the next time to download author works list
            follow_list, next_url = scr.PixivApp.follow_information(api_url=next_url)  # get next follow list
        for follow_info in follow_list:  # start download threading pool for download images from author works list
            print("start download author {} works".format(follow_info['user_name']))  # print author name
            shell_author_works(follow_info.get("user").get("id"))  # download author works list and save to local


@count_time
def shell_download_rank(next_url: str = ""):
    while True:
        if next_url is None:  # if next_url is None, it means that it is download complete
            return print("the end of follow list")
        if next_url == "":  # if next_url is empty, it means it is the first time to download author works list
            image_info_list, next_url = scr.PixivApp.get_ranking_info()
        else:  # if next_url is not empty, it means it is the next time to download author works list
            image_info_list, next_url = scr.PixivApp.get_ranking_info(api_url=next_url)  # get next follow list
        # start download threading pool for download images from author works list
        Image.Multithreading().executing_multithreading(image_info_list)


@count_time
def shell_read_text_id():
    default_file_name = "pixiv_id_list.txt"
    if not os.path.exists(default_file_name):
        open(default_file_name, 'w').close()
    image_id_list = []
    for line in open(default_file_name, 'r', encoding='utf-8', newline="").readlines():
        if line.startswith("#") or line.strip() == "":
            continue
        image_id = re.findall(r'^(\d{1,8})', line)
        if image_id and len(image_id) >= 5:
            image_id_list.append(image_id[0])
    if isinstance(image_id_list, list) and len(image_id_list) != 0:
        threading_image_pool = Image.Multithreading()
        for image_id in track(image_id_list, description="本地插画集加载中..."):
            Vars.images_info = scr.PixivApp.images_information(image_id)
            if isinstance(Vars.images_info, dict):
                threading_image_pool.add_image_info_obj(Image.ImageInfo(Vars.images_info))
            else:
                return print("无法进行下载,ERROR:", Vars.images_info)
        threading_image_pool.handling_threads()


def shell_test_pixiv_token():
    if Vars.cfg.data.get("refresh_token") == "":
        print("检测到本地档案没有令牌，请登入网站获取code来请求token，也可以将token自行写入本地档案")
        code_verifier, browser = scr.PixivLogin.open_browser()
        if scr.PixivLogin.login(code_verifier, scr.input_str('code:').strip()):
            print(f"code信息验证成功！，token信息已经保存在本地档案，请继续使用")
        else:
            print(f"输入code无效，请重新尝试获取code！")
            shell_test_pixiv_token()
    if not scr.PixivApp.get_user_info(show_start=True):
        scr.refresh_pixiv_token()


def shell_download_recommend(next_url: str = ""):  # download recommend images from pixiv api and save to local
    while True:
        if next_url is None:  # if next_url is None, it means that it is download complete
            return print("the end of recommend list")
        if next_url == "":  # if next_url is empty, it means it is the first time to download recommend list
            image_info_list, next_url = scr.PixivApp.recommend_images()
        else:  # if next_url is not empty, it means it is the next time to download recommend list
            image_info_list, next_url = scr.PixivApp.recommend_images(api_url=next_url)
        # start download threading pool for download images from recommend list and save to local
        Image.Multithreading().executing_multithreading(image_info_list)


def shell_download_stars(next_url: str = ""):  # get stars list and download all the images in the list
    while True:
        if next_url is None:
            return print("the end of stars list")  # if next_url is None, it means that it is download complete
        if next_url == "":  # if next_url is empty, it means it is the first time to download stars list
            image_info_list, next_url = scr.PixivApp.start_images()
        else:  # if next_url is not empty, it means it is the next time to download stars list
            image_info_list, next_url = scr.PixivApp.start_images(api_url=next_url)
        # start download threading pool for download images from stars list and save to local
        Image.Multithreading().executing_multithreading(image_info_list)


def start_parser() -> argparse.Namespace:  # start parser for command line arguments and start download process
    parser = argparse.ArgumentParser()  # create parser object for command line arguments
    parser.add_argument(
        "-l",
        "--login",
        dest="login",
        default=False,
        action="store_true",
        help="登录账号"
    )  # add login argument to parser object for command line arguments
    parser.add_argument(
        "-d",
        "--download",
        dest="downloadbook",
        nargs=1,
        default=None,
        help="输入image-id"
    )  # add download argument to parser object for command line arguments for download image
    parser.add_argument(
        "-m", "--max",
        dest="threading_max",
        default=None,
        help="更改线程"
    )  # add max argument to parser object for command line arguments for change threading max
    parser.add_argument(
        "-n", "--name",
        dest="name",
        nargs=1,
        default=None,
        help="输入搜搜信息"
    )  # add name argument to parser object for command line arguments for search
    parser.add_argument(
        "-u",
        "--update",
        dest="update",
        default=False,
        action="store_true",
        help="下载本地档案"
    )  # add update argument to parser object for command line arguments for download local file
    parser.add_argument(
        "-s", "--stars",
        dest="stars",
        default=False,
        action="store_true",
        help="download stars list and download all the images in the list"
    )  # add stars argument to parser object for command line arguments for download stars
    parser.add_argument(
        "-r", "--recommend",
        dest="recommend",
        default=False,
        action="store_true",
        help="download pixiv recommend images"
    )  # add recommend argument to parser object for command line arguments for download recommend
    parser.add_argument(
        "-k", "--ranking",
        dest="ranking",
        default=False,
        action="store_true",
        help="download ranking images"
    )  # add ranking argument to parser object for command line arguments for download ranking
    parser.add_argument(
        "-f",
        "--follow",
        dest="follow",
        default=False,
        action="store_true",
        help="download follow author images"
    )
    parser.add_argument(
        "-c",
        "--clear_cache",
        dest="clear_cache",
        default=False,
        action="store_true"
    )  # add clear_cache argument to parser object for command line arguments for clear cache
    parser.add_argument(
        "-a",
        "--author",
        dest="author",
        nargs=1,
        default=None,
        help="enter author id"
    )  # add author argument to parser object for command line arguments for download author
    return parser.parse_args()  # return parser object for command line arguments and return it as a tuple


def shell_parser():
    args, shell_console = start_parser(), False
    if args.recommend:
        shell_download_recommend()
        shell_console = True

    if args.ranking:
        shell_download_rank()
        shell_console = True

    if args.stars:
        shell_download_stars()
        shell_console = True

    if args.follow:
        shell_download_follow_author()
        shell_console = True

    if args.update:
        shell_read_text_id()
        shell_console = True

    if args.clear_cache:
        Vars.cfg.data.clear(), set_config()
        Vars.cfg.save()
        sys.exit(3)  # exit with code 3  to clear cache

    if args.threading_max:
        Vars.cfg.data['max_thread'] = int(args.max)

    if args.name:
        shell_search(['n'] + args.name)
        shell_console = True

    if args.downloadbook:
        shell_illustration(['d'] + args.downloadbook)
        shell_console = True

    if args.author:
        shell_author_works(args.author[0])
        shell_console = True

    if args.login:
        shell_test_pixiv_token()
        shell_console = True

    if not shell_console:
        for info in Msg.msg_help:
            print_lang('[帮助]', info)
        while True:
            shell(re.split('\\s+', scr.input_str('>').strip()))


def shell(inputs: list):
    if inputs[0] == 'q' or inputs[0] == 'quit':
        sys.exit("已退出程序")
    elif inputs[0] == 'l' or inputs[0] == 'login':
        shell_test_pixiv_token()
    elif inputs[0] == 'd' or inputs[0] == 'download':
        shell_illustration(inputs)
    elif inputs[0] == 's' or inputs[0] == 'stars':
        shell_download_stars()
    elif inputs[0] == 'n' or inputs[0] == 'name':
        shell_search(inputs)
    elif inputs[0] == 'r' or inputs[0] == 'recommend':
        shell_download_recommend()
    elif inputs[0] == 'u' or inputs[0] == 'update':
        shell_read_text_id(inputs)
    elif inputs[0] == 'k' or inputs[0] == 'rank':
        shell_download_rank()
    elif inputs[0] == 'f' or inputs[0] == 'follow':
        shell_download_follow_author()
    else:
        print(inputs[0], "为无效指令")


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
        print(msg)


if __name__ == '__main__':
    # update()
    try:
        set_config()
        shell_test_pixiv_token()
        shell_parser()
    except KeyboardInterrupt:
        quit("已手动退出程序")
    except Exception as error:
        print("程序意外退出，ERROR:", error)
