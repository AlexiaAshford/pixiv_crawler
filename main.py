import download
from instance import *
from rich.progress import track
import PixivAPI


def shell_download_author_works(author_id: str):
    for index, page in enumerate(range(20), start=1):
        image_id_list = PixivAPI.PixivApp.author_information(author_id, index)
        if isinstance(image_id_list, list) and len(image_id_list) != 0:
            Vars.images_info_list = [
                download.ImageInfo(PixivAPI.PixivApp.images_information(image_id))
                for image_id in track(image_id_list, description="作者插画集加载中...")
            ]
            download.threading_download()
        else:
            print("作者插画集下载完毕！")


@count_time
def shell_illustration(inputs):
    if len(inputs) >= 2:
        if isinstance(inputs, list) and len(inputs) == 3 and inputs[2] == "a":
            shell_download_author_works(inputs[1])  # 通过作者ID下载作者的作品集
        else:
            Vars.images_info = PixivAPI.PixivApp.images_information(PixivAPI.rec_id(inputs[1]))
            if isinstance(Vars.images_info, dict):
                Vars.images_info = download.ImageInfo(Vars.images_info)
                Vars.images_info.show_images_information()
                if Vars.images_info.page_count == 1:
                    Vars.images_info.save_image(Vars.images_info.original_url)
                else:
                    Vars.images_info.save_image(Vars.images_info.original_url_list)
            else:
                print("没有找到相应的作品！")
    else:
        print("你没有输入id或者链接")


@count_time
def shell_search(inputs: list):
    if len(inputs) >= 2:
        PixivAPI.PixivApp.search_information(inputs[1])
    else:
        print("没有输入搜索信息")


@count_time
def shell_download_follow_author():
    author_id_list = PixivAPI.PixivApp.follow_information()
    for author_id in author_id_list:
        shell_download_author_works(author_id)


@count_time
def shell_download_rank():
    try:
        print(PixivAPI.PixivApp.rank_information())
    except Exception as error:
        print(error)


@count_time
def shell_read_text_id(inputs):
    list_file_name = inputs[1] + '.txt' if len(inputs) >= 2 else 'list.txt'
    try:
        list_file_input = open(list_file_name, 'r', encoding='utf-8')
    except OSError:
        print(f"{list_file_name}文件不存在")
        return
    image_id_list = [
        re.sub("^\\s*([0-9]{1,8}).*$\\n?", "\\1", line)
        for line in list_file_input.readlines() if re.match("^\\s*([0-9]{1,7}).*$", line)
    ]
    PixivAPI.Download.threading_download(image_id_list)


def shell_pixiv_token():
    for retry in range(Vars.cfg.data("headers", "retry")):
        if Vars.cfg.data("user", "access_token") != "":
            return True
        else:
            print("检测到本地档案没有令牌，请登入网站获取code，也可以将token自行写入本地档案")
            code_verifier = PixivAPI.login_pixiv.open_browser()
            code = PixivAPI.input_('code:').strip()
            result = PixivAPI.login_pixiv.login(code_verifier, code)
            if result is None:
                return
            print("输入code无效，请重新尝试获取！")


def shell():
    if len(sys.argv) > 1 and isinstance(sys.argv, list):
        command_line = True
        inputs = sys.argv[1:]
    else:
        command_line = False
        print(Vars.cfg.data("user", "help"))
        inputs = re.split('\\s+', PixivAPI.input_('>').strip())
    while True:
        if inputs[0] == 'q' or inputs[0] == 'quit':
            sys.exit("已退出程序")
        elif inputs[0] == 'h' or inputs[0] == 'help':
            print(Vars.cfg.data("user", "help"))
        elif inputs[0] == 'l' or inputs[0] == 'login':
            shell_pixiv_token()
        elif inputs[0] == 'd' or inputs[0] == 'download':
            shell_illustration(inputs)
        elif inputs[0] == 's' or inputs[0] == 'stars':
            PixivAPI.PixivApp.start_information()
        elif inputs[0] == 'n' or inputs[0] == 'name':
            shell_search(inputs)
        elif inputs[0] == 't' or inputs[0] == 'recommend':
            PixivAPI.PixivApp.recommend_information()
        elif inputs[0] == 'u' or inputs[0] == 'update':
            shell_read_text_id(inputs)
        elif inputs[0] == 'r' or inputs[0] == 'rank':
            shell_download_rank()
        elif inputs[0] == 'f' or inputs[0] == 'follow':
            shell_download_follow_author()
        else:
            print(inputs[0], "为无效指令")
        if command_line is True:
            sys.exit(1)
        inputs = re.split('\\s+', PixivAPI.input_('>').strip())


if __name__ == '__main__':
    set_config()
    shell_pixiv_token()
    shell()
