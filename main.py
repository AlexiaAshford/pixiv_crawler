import re
import sys

from rich import print
import PixivAPI


def shell_Collection():
    for illusts in PixivAPI.PixivApp.start_information()["illusts"]:
        shell_illustration(illusts["id"])


def shell_illustration(illustration_id: int):
    response = PixivAPI.PixivApp.illustration_information(illustration_id)
    if response != "":
        print("插画名称：", response.title, "开始下载")
        PixivAPI.Download.download_png(response.image_urls['large'])


def shell_pixiv_token():
    for retry in range(PixivAPI.config.data("headers", "retry")):
        if PixivAPI.config.data("user", "access_token") != "":
            return True
        print("本地配置文件没有令牌，请登入网站获取code")
        PixivAPI.login_pixiv.login()


def shell():
    if len(sys.argv) > 1 and type(sys.argv) is list:
        command_line = True
        inputs = sys.argv[1:]
    else:
        command_line = False
        inputs = re.split('\\s+', PixivAPI.input_('>').strip())
    while True:
        if inputs[0] == 'q' or inputs[0] == 'quit':
            sys.exit("已退出程序")
        elif inputs[0] == 'h' or inputs[0] == 'help':
            print("help")
        elif inputs[0] == 'd' or inputs[0] == 'download':
            shell_illustration(inputs[0])
        elif inputs[0] == 's' or inputs[0] == 'stars':
            shell_Collection()
        else:
            print(inputs[0], "为无效指令")
        if command_line is True:
            sys.exit(1)
        inputs = re.split('\\s+', PixivAPI.input_('>').strip())


if __name__ == '__main__':
    shell_pixiv_token()
    shell()
