import os

def make_path_exist(path):
    if path is not "":
        if not os.path.isdir(path):
            make_path_exist(os.path.dirname(path))
            os.mkdir(path)
