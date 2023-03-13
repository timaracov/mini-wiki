import markdown as md

from pywiki.config import Config

from .filesys import (
    get_filename_from_path,
    get_folders_files,
    get_folders_subdirs,
    get_folder_from_path
)


def add_page_file(md_file_path, out_file_path):
    with (
        open(md_file_path) as md,
        open(out_file_path, "w") as out
    ):
        page_html = md2html(md.read())
        page_header = get_filename_from_path(md_file_path)
        built_wiki_page = make_wiki_page(page_header, page_html)
        out.write(built_wiki_page)


def add_index_page(source_folder, out_folder, is_root=False):
    if not is_root:
        source_folder_name = get_folder_from_path(source_folder)
    else:
        source_folder_name = "wiki"

    out_index = out_folder / f"index_{source_folder_name}.html"
    with open(out_index, "w") as out:
        built_index_page = make_index_page(source_folder_name, out_folder)
        out.write(built_index_page)


def make_wiki_page(header: str, article_html: str):
    wiki_page_template = Config.env.get_template("wiki_page.html")
    css_path = Config.out_styles_path / "wiki.css"

    built_html_page = wiki_page_template.render(
        styles_path=f'"{css_path}"',
        page_header=header,
        article=article_html)

    return built_html_page


def make_index_page(topic_name: str, topic_folder_path: str): 
    articles_files = get_folders_files(topic_folder_path)
    subtopics_folders  = get_folders_subdirs(topic_folder_path)

    wiki_page_template = Config.env.get_template("index_page.html")
    css_path = Config.out_styles_path / "index.css"

    built_html_page = wiki_page_template.render(
        styles_path=f'"{css_path}"',
        index_page_header=topic_name,
        subtopics=subtopics_folders,
        articles=articles_files,
    )

    return built_html_page


def md2html(md_text: str) -> str:
    return md.markdown(md_text, extensions=['fenced_code', 'codehilite'])


def is_md_file(filename: str) -> bool:
    return filename.endswith(".md")


def md2html_extension(filename: str) -> str:
    ext_index = filename.find(".md")
    return f"{filename[:ext_index]}.html"

