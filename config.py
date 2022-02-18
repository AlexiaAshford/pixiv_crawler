import re
import time
from setting import *
from rich import print


class Vars:
    cfg = Config('Pixiv-Config.json', os.getcwd())