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
    return False if PixivAPI.config.data("user", "access_token") == "" else True


if __name__ == '__main__':
    if not shell_pixiv_token():
        print()
        access_token, refresh_token = PixivAPI.login_pixiv.login()
        PixivAPI.config.save("user", "access_token", access_token)
        PixivAPI.config.save("user", "refresh_token", refresh_token)
    else:
        shell_illustration(72686840)
