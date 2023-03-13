import os
import time
import datetime as dt


WIKI_TREE = {".": {}}
WIKI_TAGS = {}

HOME = os.getenv("HOME") or "/home/timaracov"
DEFAULT_PATH = os.path.join(HOME, "main_files/reading/wiki/topics")

EXCLUDE_FOLDERS = ["html", "graph", "mini_wiki"]


def update_wiki():
    if is_wiki_tree_updated():
        make_tags()
        print(f":: updated wiki | {dt.datetime.now().strftime('%H:%M:%S %d/%m/%Y')}")


def is_wiki_tree_updated() -> bool:
    global WIKI_TREE

    if (new_wiki := make_wiki_tree()) == WIKI_TREE:
        return False
    else:
        WIKI_TREE = new_wiki.copy()
        return True


def make_wiki_tree(current_dir: str = DEFAULT_PATH, wiki_keys: list[str] =[DEFAULT_PATH], wiki={}):
    to_eval = make_dict_eval_string("wiki", wiki_keys)
    eval(to_eval)

    for path in os.listdir(current_dir):
        new_current_path = os.path.join(current_dir, path)
        new_keys = wiki_keys + [path]

        if not os.path.isdir(new_current_path):
            continue

        if any(is_dir(new_current_path, path) for path in os.listdir(new_current_path)):
            make_wiki_tree(new_current_path, new_keys, wiki)
        else:
            to_eval = make_dict_eval_string("wiki", new_keys)
            eval(to_eval)

    return wiki


def make_dict_eval_string(wiki_name: str, keys):
    if len(keys) == 1:
        return f"{wiki_name}.update({{'{keys[0]}': {{}}}})"

    string = f"{wiki_name}"
    for ind, key in enumerate(keys):
        if ind == len(keys)-1:
            string += f".update({{'{key}': {{}}}})"
        else:
            string += f"['{key}']"

    return string


def make_tags(current_dir: str = DEFAULT_PATH, tag: str = '0', tag_count: int = 0):
    write_tag(current_dir, tag)

    for path in os.listdir(current_dir):
        new_current_path = os.path.join(current_dir, path)

        if not os.path.isdir(new_current_path):
            continue

        if any(is_dir(new_current_path, path) for path in os.listdir(new_current_path)):
            make_tags(new_current_path, f"{tag}.{tag_count}", tag_count+1)
        else:
            write_tag(new_current_path, f"{tag}.{tag_count}")

        tag_count += 1


def is_dir(path, sub_path):
    return os.path.isdir(os.path.join(path, sub_path))


def write_tag(path, tag):
    global WIKI_TAGS

    if any(exl in path for exl in EXCLUDE_FOLDERS):
        return
    
    WIKI_TAGS.update({tag: f"{path}/tag.md"})

    with open(f"{path}/tag.md", "w") as f:
        f.write(tag)


def write_stats():
    with open("wiki.stats", "w") as f:
        f.write(wiki_dict_to_yaml(WIKI_TREE))
        f.write("\n\n")
        f.write(tag_dict_to_yaml(WIKI_TAGS))


def wiki_dict_to_yaml(tag_dict: dict, _indet="", _yaml_string=""):
    for k, v in tag_dict.items():
        if v == {}:
            _yaml_string += f"\n{_indet}-{k}"
        else:
            _yaml_string += f"\n{_indet}| {k}:"
            _yaml_string = wiki_dict_to_yaml(v, _indet+"  ", _yaml_string)

    return _yaml_string


def tag_dict_to_yaml(tags):
    yaml_string = ""
    max_line_length = len(max(tags.keys(), key=len))
    separator = "  -  "
    for k, v in tags.items():
        yaml_string += f"{k:{max_line_length}}{separator}{v}\n"
    return yaml_string


#if __name__ == "__main__":
#    while 1:
#        update_wiki()
#        write_stats()
#        time.sleep(1)
