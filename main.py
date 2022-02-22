from instance import *
import PixivAPI


def new_file():
    PixivAPI.mkdir(Vars.cfg.data("user", "save_file"))


def shell_download_author_works(author_id: str):
    start = time.time()



    image_id_list = PixivAPI.PixivApp.author_information(author_id)
    if type(image_id_list) is list and len(image_id_list) != 0:
        PixivAPI.Download.threading_download(image_id_list)
        print(f'下载耗时:{round(time.time() - start, 2)} 秒')
    else:
        print("没有找到相关的信息，可能是输入的ID不正确")


def shell_illustration(inputs):
    if len(inputs) >= 2:
        if type(inputs) is list and len(inputs) == 3 and inputs[2] == "a":
            shell_download_author_works(inputs[1])  # 通过作者ID下载作者的作品集
        else:
            start = time.time()  # 通过作品ID下载原图
            image_id = PixivAPI.rec_id(inputs[1])
            if image_id != "":
                PixivAPI.Download.save_image(image_id)
            print(f'下载耗时:{round(time.time() - start, 2)} 秒')
    else:
        print("你没有输入id或者链接")


def shell_search(inputs: list, target=None):
    if target is None:
        target = 'partial_match_for_tags'
    if len(inputs) >= 2:
        PixivAPI.PixivApp.search_information(inputs[1], target)


def shell_pixiv_token():
    for retry in range(int(Vars.cfg.data("headers", "retry"))):
        if Vars.cfg.data("user", "access_token") != "":
            return True
        print("本地配置文件没有令牌，请登入网站获取code")
        PixivAPI.login_pixiv.login()


def shell():
    if len(sys.argv) > 1 and type(sys.argv) is list:
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
        elif inputs[0] == 'd' or inputs[0] == 'download':
            shell_illustration(inputs)
        elif inputs[0] == 's' or inputs[0] == 'stars':
            PixivAPI.PixivApp.start_information()
        elif inputs[0] == 'n' or inputs[0] == 'name':
            shell_search(inputs[1])
        elif inputs[0] == 't' or inputs[0] == 'recommend':
            PixivAPI.PixivApp.recommend_information()
        elif inputs[0] == 'f' or inputs[0] == 'follow':
            response = PixivAPI.PixivApp.follow_information()
            print(response)
        else:
            print(inputs[0], "为无效指令")
        if command_line is True:
            sys.exit(1)
        inputs = re.split('\\s+', PixivAPI.input_('>').strip())


if __name__ == '__main__':
    set_config()
    shell_pixiv_token()
    new_file()
    shell()
