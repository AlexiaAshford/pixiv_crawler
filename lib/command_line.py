import argparse


def start_parser() -> argparse.Namespace:  # start parser for command line arguments and start download process
    parser = argparse.ArgumentParser()  # create parser object for command line arguments
    parser.add_argument(
        "-l", "--login",
        default=False, action="store_true", help="login to pixiv account and save token to config file"
    )  # add login argument to parser object for command line arguments
    parser.add_argument(
        "-d", "--download",
        nargs=1, default=None, help="input image id to download it"
    )  # add download argument to parser object for command line arguments for download image
    parser.add_argument(
        "-m", "--max",
        dest="threading_max", default=None, help="change max threading number"
    )  # add max argument to parser object for command line arguments for change threading max
    parser.add_argument(
        "-n", "--name",
        nargs=1, default=None, help="input search name or tag name"
    )  # add name argument to parser object for command line arguments for search
    parser.add_argument(
        "-u", "--update",
        default=False, action="store_true", help="download update local image id"
    )  # add update argument to parser object for command line arguments for download local file
    parser.add_argument(
        "-s", "--stars",
        default=False, action="store_true", help="download stars list and download all the images in the list"
    )  # add stars argument to parser object for command line arguments for download stars
    parser.add_argument(
        "-r", "--recommend",
        default=False, action="store_true", help="download pixiv recommend images"
    )  # add recommend argument to parser object for command line arguments for download recommend
    parser.add_argument(
        "-k", "--ranking",
        default=False, action="store_true", help="download ranking images"
    )  # add ranking argument to parser object for command line arguments for download ranking
    parser.add_argument(
        "-f", "--follow",
        default=False, action="store_true", help="download follow author images"
    )
    parser.add_argument(
        "-c", "--clear_cache",
        default=False, action="store_true"
    )  # add clear_cache argument to parser object for command line arguments for clear cache
    parser.add_argument(
        "-a", "--author",
        nargs=1, default=None, help="enter author id"
    )  # add author argument to parser object for command line arguments for download author
    return parser.parse_args()  # return parser object for command line arguments and return it as a tuple
