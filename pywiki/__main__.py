from time import sleep

from . import cli
from .core import builder


if __name__ == "__main__":
    args = cli.get_args()
    if args.auto:
        while True:
            sleep(10)
            builder.build_wiki(args)
    else:
        builder.build_wiki(args)
