import os
import yaml


class YamlData:
    def __init__(self, file_path=None, file_dir=None):
        if file_dir is not None:
            self.file_dir = os.path.join(os.getcwd(), file_dir)
            if not os.path.exists(self.file_dir):
                try:
                    os.mkdir(self.file_dir)
                except (FileExistsError, OSError) as err:
                    print("Yaml Data Error: {}".format(err))

        if file_path is not None:
            self.file_path = os.path.join(os.getcwd(), file_path)
            self.data = {}

    def load(self):
        try:
            with open(file=self.file_path, mode="r", encoding='utf-8') as f:
                self.data = yaml.load(f, Loader=yaml.FullLoader)
                if self.data is None:
                    self.data = {}
        except FileNotFoundError:
            with open(self.file_path, 'w', encoding='utf-8'):
                self.data = {}

    def save(self):
        with open(file=self.file_path, mode="w", encoding='utf-8') as f:
            yaml.safe_dump(self.data, f, default_flow_style=False, allow_unicode=True)
