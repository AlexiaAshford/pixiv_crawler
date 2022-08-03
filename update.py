import json
import os
import sys
import src
from tools import *


def update():
    download_test = False
    response = src.get("https://raw.githubusercontent.com/VeronicaAlexia/pixiv_crawler/main/update.json")
    if not os.path.exists('update.json'):
        json.dump(response, open('update.json', 'w'))
        download_test = True
    data = json.loads(open('update.json', 'r').read())
    if data['version'] < response['version']:
        print("检测到有新版本", response['version'], "是否进行更新？[yes/no]")
        choice = functions.input_str('>').strip()
        if choice == "yes":
            download_test = True
            print("开始更新", response['version'], "版本")
        else:
            download_test = False

    if download_test:
        with open(data['name'] + ".exe", 'wb') as file:
            print(response['download_url'].format(response['version']))
            file.write(src.get(response['download_url'].format(response['version']), return_type="content"))
        print(data['name'] + ".exe", "下载完毕")
        json.dump(response, open('update.json', 'w'))
        print("三秒后自动退出脚本...")
        sys.exit()
