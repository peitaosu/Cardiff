import os, sys, importlib, time

def diff_file(file_before, file_after, file_output_name = None):
    """diff file and save as file

    args:
        file_before (str)
        file_after (str)
        file_output_name (str)
    
    returns:
        saved_file (str)
    """
    file_name = os.path.basename(file_before)
    file_ext = file_name.split(".")[-1]
    file_differ = importlib.import_module("format." + file_ext + ".differ")
    if file_output_name == None:
        file_output_name = str(time.time())
    saved_file = file_differ.make_diff(file_before, file_after, file_output_name)
    return saved_file

def diff(file_before, file_after):
    """diff file and return the diff object

    args:
        file_before (str)
        file_after (str)

    returns:
        file_diff (object)
    """
    file_name = os.path.basename(file_before)
    file_ext = file_name.split(".")[-1]
    file_differ = importlib.import_module("format." + file_ext + ".differ")
    return file_differ.diff(file_before, file_after)
