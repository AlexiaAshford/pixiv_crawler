from src import Image
from tools.instance import *
from rich.progress import track
import src


def shell_author_works(author_id: str, next_url: str = ""):  # download author images save to local
    while True:
        if next_url is None:  # if next_url is None, it means that it is download complete
            return print("the end of author_works list")
        if next_url == "":  # if next_url is empty, it means it is the first time to download author works list
            image_info_list, next_url = src.PixivApp.author_information(author_id=author_id)
        else:  # if next_url is not empty, it means it is the next time to download author works list
            image_info_list, next_url = src.PixivApp.author_information(api_url=next_url)
        # # start download threading pool for download images from author works list
        Image.Multithreading().executing_multithreading(image_info_list)


@count_time
def shell_illustration(inputs):
    if len(inputs) >= 2:
        Vars.images_info = src.PixivApp.images_information(src.rec_id(inputs[1]))
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
    Image.Multithreading().executing_multithreading(src.Tag.search_information(png_name=inputs[1]))


@count_time
def shell_download_follow_author(next_url: str = ""):
    while True:
        if next_url is None:  # if next_url is None, it means that it is download complete
            return print("the end of follow list")
        if next_url == "":  # if next_url is empty, it means it is the first time to download author works list
            follow_list, next_url = src.PixivApp.follow_information()
        else:  # if next_url is not empty, it means it is the next time to download author works list
            follow_list, next_url = src.PixivApp.follow_information(api_url=next_url)  # get next follow list
        for follow_info in follow_list:  # start download threading pool for download images from author works list
            print("start download author {} works".format(follow_info['user_name']))  # print author name
            shell_author_works(follow_info.get("user").get("id"))  # download author works list and save to local


@count_time
def shell_download_rank(next_url: str = ""):
    while True:
        if next_url is None:  # if next_url is None, it means that it is download complete
            return print("the end of follow list")
        if next_url == "":  # if next_url is empty, it means it is the first time to download author works list
            image_info_list, next_url = src.PixivApp.get_ranking_info()
        else:  # if next_url is not empty, it means it is the next time to download author works list
            image_info_list, next_url = src.PixivApp.get_ranking_info(api_url=next_url)  # get next follow list
        # start download threading pool for download images from author works list
        Image.Multithreading().executing_multithreading(image_info_list)


@count_time
def shell_read_text_id():
    default_file_name = "../pixiv_id_list.txt"
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
            Vars.images_info = src.PixivApp.images_information(image_id)
            if isinstance(Vars.images_info, dict):
                threading_image_pool.add_image_info_obj(Image.ImageInfo(Vars.images_info))
            else:
                return print("无法进行下载,ERROR:", Vars.images_info)
        threading_image_pool.handling_threads()


def shell_test_pixiv_token():
    if Vars.cfg.data.get("refresh_token") == "":
        print("检测到本地档案没有令牌，请登入网站获取code来请求token，也可以将token自行写入本地档案")
        code_verifier, browser = src.PixivLogin.open_browser()
        if src.PixivLogin.login(code_verifier, src.input_str('code:').strip()):
            print(f"code信息验证成功！，token信息已经保存在本地档案，请继续使用")
        else:
            print(f"输入code无效，请重新尝试获取code！")
            shell_test_pixiv_token()
    if Vars.cfg.data.get("user_info", {}).get("id") is None:
        print("test pixiv account info is impossible, refresh token is needed")
        src.refresh_pixiv_token()
    if not src.PixivApp.get_user_info(show_start=True):
        src.refresh_pixiv_token()


def shell_download_recommend(next_url: str = ""):  # download recommend images from pixiv api and save to local
    while True:
        if next_url is None:  # if next_url is None, it means that it is download complete
            return print("the end of recommend list")
        if next_url == "":  # if next_url is empty, it means it is the first time to download recommend list
            image_info_list, next_url = src.PixivApp.recommend_images()
        else:  # if next_url is not empty, it means it is the next time to download recommend list
            image_info_list, next_url = src.PixivApp.recommend_images(api_url=next_url)
        # start download threading pool for download images from recommend list and save to local
        Image.Multithreading().executing_multithreading(image_info_list)


def shell_download_stars(next_url: str = ""):  # get stars list and download all the images in the list
    while True:
        if next_url is None:
            return print("the end of stars list")  # if next_url is None, it means that it is download complete
        if next_url == "":  # if next_url is empty, it means it is the first time to download stars list
            image_info_list, next_url = src.PixivApp.start_images()
        else:  # if next_url is not empty, it means it is the next time to download stars list
            image_info_list, next_url = src.PixivApp.start_images(api_url=next_url)
        # start download threading pool for download images from stars list and save to local
        Image.Multithreading().executing_multithreading(image_info_list)
