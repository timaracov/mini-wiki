import os
from pathlib import Path

from pywiki.config import Config

from .md_html import (
    is_md_file,
    add_page_file,
    md2html_extension,
    add_index_page
)
from .filesys import get_folders_files, get_folders_subdirs


def build_wiki(args):
    config = _update_config(Config, args)

    _drop_output_folders(config)
    _create_output_folders(config)
    _copy_styles_by_theme(config)
    _build_html_files_tree(Config.source_path, Config.out_pages_path)


def _update_config(config, args):
    config.name = args.name
    config.theme = args.theme
    config.source_path = Path(args.folder).absolute()
    config.out_path = Path(args.output).absolute()
    config.out_pages_path = Config.out_path / args.name / "pages"
    config.out_styles_path = Config.out_path / args.name / "styles"

    return config


def _create_output_folders(config):
    os.makedirs(config.out_pages_path)
    os.makedirs(config.out_styles_path)


def _drop_output_folders(config):
    from shutil import rmtree
    try:
        rmtree(config.out_path)
    except:
        pass


def _copy_styles_by_theme(config):
    from distutils.dir_util import copy_tree

    available_themes = __get_available_themes(config)
    if config.theme in available_themes:
        copy_tree(
            str(__get_theme_folder(config.theme, config)),
            str(config.out_styles_path))


def _build_html_files_tree(source_folder: Path, out_folder: Path, root=1):
    subdirs = get_folders_subdirs(source_folder)
    files = get_folders_files(source_folder)

    for file in files:
        if is_md_file(file):
            add_page_file(
                source_folder / file,
                out_folder / md2html_extension(file))

    for subdir in subdirs:
        new_out_folder = out_folder / subdir
        new_source_folder = source_folder / subdir

        os.makedirs(new_out_folder)
        _build_html_files_tree(new_source_folder, new_out_folder, root=0)

    add_index_page(source_folder, out_folder, bool(root))



def __get_available_themes(config):
    return os.listdir(config.project_root / "templates/themes")


def __get_theme_folder(theme: str, config):
    return config.project_root / "templates/themes" / theme
