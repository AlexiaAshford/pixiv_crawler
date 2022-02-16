import os
import re
import sys
from rich import print
import PixivAPI


def new_file():
    PixivAPI.mkdir(PixivAPI.config.data("user", "save_file"))


def shell_collection():
    response = PixivAPI.PixivApp.start_information()
    if type(response) is list:
        for index, values in enumerate(response):
            author_name = values['user']['name']
            image_name = values["title"]
            update = values['create_date']
            tags_llist = [i['name'] for i in values['tags']]
            print("\n第{}幅插图 [{}]:".format(index, update))
            print("作者: {}\n插画: {}:".format(author_name, image_name))
            print("标签: {}".format(', '.join(tags_llist)))
            shell_illustration(values["id"])


def shell_illustration(illustration_id: int):
    response = PixivAPI.PixivApp.illustration_information(illustration_id)
    if response.get("message") is None:
        image_url = response.image_urls['large']
        image_name = PixivAPI.remove_str(response.title)
        file_path = PixivAPI.config.data("user", "save_file")
        if not os.path.exists(os.path.join(file_path, f'{image_name}.png')):
            PixivAPI.Download.download(image_url, image_name, file_path)


def shell_pixiv_token():
    for retry in range(int(PixivAPI.config.data("headers", "retry"))):
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
            shell_collection()
        else:
            print(inputs[0], "为无效指令")
        if command_line is True:
            sys.exit(1)
        inputs = re.split('\\s+', PixivAPI.input_('>').strip())


if __name__ == '__main__':
    shell_pixiv_token()
    new_file()
    shell()
