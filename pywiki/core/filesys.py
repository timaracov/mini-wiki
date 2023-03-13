import os
from pathlib import Path


def get_folders_files(folder):
    return [
        name
        for name in os.listdir(folder)
        if not os.path.isdir(os.path.join(folder, name))
    ]


def get_folders_subdirs(folder):
    return [
        name for name in os.listdir(folder) if os.path.isdir(os.path.join(folder, name))
    ]


def get_filename_from_path(path_to_file: str):
    _, filename_with_extension = os.path.split(path_to_file)
    md_index = filename_with_extension.find(".md")
    return filename_with_extension[:md_index]


def get_folder_from_path(path: Path):
    return os.path.basename(path)
