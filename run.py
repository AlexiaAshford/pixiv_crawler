import os
import setting
import random
import time
from rich import print
import PixivAPI


def download_pic(illust_id):
    save_path = config.data("File", "save_file")
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    with open(os.path.join(save_path, f'{illust_id}.png'), 'wb+') as file:
        file.write(PixivAPI.Download.download(illust_id))
        print('成功下载图片：{}.png'.format(illust_id))


if __name__ == '__main__':
    config = setting.Config('config.ini')
    config.load()
    for index, page in enumerate(range(1, 6)):
        response = PixivAPI.Ranking.ranking_id(page)
        if response is not None and response.get('contents'):
            for contents in response['contents']:
                png_id = contents["illust_id"]
                time.sleep(random.random() * float(1))
                download_pic(png_id)
