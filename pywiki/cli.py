import argparse


def get_args():
    parser = _get_parser()
    args = parser.parse_args()

    return args


def _get_parser():
    _parser = argparse.ArgumentParser(
        prog="pywiki",
        usage="pywiki [OPTIONS] folder",
        description="Build local wiki from markdown files",
    )

    _parser.add_argument(
        "folder",
        help="source folder of markdown files")
    _parser.add_argument(
        "--theme",
        default="default_dark",
        help="wiki pages theme, default opptions: default_dark")
    _parser.add_argument(
        "--name",
        default="wiki",
        help="name of the output wiki folder")
    _parser.add_argument(
        "--output",
        default="./out",
        help="path to the folder where the wiki will be stored",
    )
    _parser.add_argument(
        "--auto",
        default=False,
        help="automatically rebuild wiki",
    )

    return _parser
