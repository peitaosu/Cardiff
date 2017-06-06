import os, sys, importlib, time

def merge_file(file_before, file_after, file_output_name = None):
    """merge files and save as file

    args:
        file_before (str)
        file_after (str)
        file_output_name (str)
    
    returns:
        saved_file (str)
    """
    file_name = os.path.basename(file_before)
    file_ext = file_name.split(".")[-1]
    file_merger = importlib.import_module("format." + file_ext + ".merger")
    if file_output_name == None:
        file_output_name = str(time.time())
    saved_file = file_merger.make_merged(file_before, file_after, file_output_name)
    return saved_file

def merge(file_before, file_after):
    """merge files and return the file merged dict

    args:
        file_before (str)
        file_after (str)
    
    returns:
        file_merged (dict)
    """
    file_name = os.path.basename(file_before)
    file_ext = file_name.split(".")[-1]
    file_merger = importlib.import_module("format." + file_ext + ".merger")
    return file_merger.merge(file_before, file_after)
