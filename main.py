import re
import sys

from rich import print
import PixivAPI


def shell_Collection():
    for illusts in PixivAPI.PixivApp.start_information()["illusts"]:
        id = illusts["id"]
        title = illusts["title"]
        # image_urls = illusts["image_urls"]
        print(title, f"\t{id}")


def shell_illustration(illustration_id: int):
    response = PixivAPI.PixivApp.illustration_information(illustration_id)
    if response != "":
        print("插画名称：", response.title)
        print("插画链接：", response.image_urls['large'])


def shell_pixiv_token():
    if PixivAPI.config.data("user", "access_token") == "":
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
        else:
            print(inputs[0], "为无效指令")
        if command_line is True:
            sys.exit(1)
        inputs = re.split('\\s+', PixivAPI.input_('>').strip())


if __name__ == '__main__':
    shell_pixiv_token()
    shell()
