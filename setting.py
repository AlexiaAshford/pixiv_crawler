# 封装配置文件
import configparser


class Config:

    def __init__(self, filename):
        self.filename = filename
        self.config = configparser.ConfigParser()

    def load(self):
        try:
            self.config.read(self.filename, encoding="utf-8")
        except configparser.ParsingError as error:
            print("ERROR:{}".format(error))
            with open(self.filename, 'w') as configfile:
                configfile.write("")

    def data(self, key, value):
        try:
            return self.config.get(key, value)
        except:
            print("No section or Option!", key, value)

    def save(self, config_key, save_key, save_data):
        if not self.config.has_section(config_key):
            # 增加section
            self.config.add_section(config_key)

        # 增加key-value
        self.config.set(config_key, save_key, save_data)
        # 将配置写入文件
        with open(self.filename, 'w') as configfile:
            self.config.write(configfile)


def set_config():
    conf = Config('config.ini')
    conf.load()
    # +++++++++++++++++++++headers=======================
    if type(conf.data("headers", "User-Agent")) is not str:
        conf.save(
            "headers", "User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1"
        )
    if type(conf.data("headers", "Cookie")) is not str:
        conf.save("headers", "Cookie`", "")
    if type(conf.data("headers", "retry")) is not str:
        conf.save("headers", "retry", "5")
    if type(conf.data("headers", "referer")) is not str:
        conf.save(
            "headers", "referer", "https://www.pixiv.net/ranking.php?mode=daily&content=illust"
        )
    # +++++++++++++++++++++headers=======================
    if type(conf.data("thread", "max_thread")) is not str:
        conf.save("thread", "max_thread", "5")
    if type(conf.data("File", "save_file")) is not str:
        conf.save("File", "save_file", "pixiv")
    if type(conf.data("File", "out_file")) is not str:
        conf.save("File", "out_file", "downloaded")
    return conf

