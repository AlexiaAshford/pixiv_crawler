from rich import print
import PixivAPI


def shell_Collection():
    print()
    for illusts in PixivAPI.PixivApp.start_information()["illusts"]:
        id = illusts["id"]
        title = illusts["title"]
        # image_urls = illusts["image_urls"]
        print(title, f"\t{id}")


def shell_illustration(illustration_id: int):
    response = PixivAPI.PixivApp.illustration_information(illustration_id)
    print("插画名称：", response.illust.title)
    print("插画链接：", response.illust.image_urls['large'])


if __name__ == '__main__':
    shell_illustration(72686840)
