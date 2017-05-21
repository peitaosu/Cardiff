import os, re

def make_path_exist(path):
    if path is not "":
        if not os.path.isdir(path):
            make_path_exist(os.path.dirname(path))
            os.mkdir(path)

def clean_path(path, pattern=None):
    for root, dirs, files in os.walk(path):
        for file_item in files:
            if pattern is not None:
                if not re.search(pattern, file_item):
                    continue
            os.remove(os.path.join(root, file_item))
            print os.path.join(root, file_item) + " deleted."
