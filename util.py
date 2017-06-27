import os, re, time

def make_path_exist(path):
    """check the path if any folder not exists then create it

    args:
        path (str)
    """
    if path is not "":
        if not os.path.isdir(path):
            make_path_exist(os.path.dirname(path))
            os.mkdir(path)

def clean_path(path, pattern=None):
    """check the files in the path with pattern, if match then delete the file

    args:
        path (str)
        pattern (str)
    """
    for root, dirs, files in os.walk(path):
        for file_item in files:
            if pattern is not None:
                if not re.search(pattern, file_item):
                    continue
            os.remove(os.path.join(root, file_item))
            print os.path.join(root, file_item) + " deleted."

def vprint(verbose_log):
    """print verbose log while environment variable VERBOSE_LOG set

    args:
        verbose_log (str)
    """
    if "VERBOSE_MODE" in os.environ:
        if os.getenv("VERBOSE_MODE") == "1":
            print "[VERBOSE LOG]: {} - {}".format(time.strftime("%m-%d-%Y %H:%M:%S", time.localtime()), verbose_log)
