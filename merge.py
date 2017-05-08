import os, sys, importlib, time

def merge_file(file_before, file_after, file_output_name = None):
    file_name = os.path.basename(file_before)
    file_ext = file_name.split(".")[-1]
    file_merger = importlib.import_module("format." + file_ext + ".merger")
    if file_output_name == None:
        file_output_name = str(time.time())
    saved_file = file_merger.make_merged(file_before, file_after, file_output_name)
    return saved_file

def merge(file_before, file_after):
    file_name = os.path.basename(file_before)
    file_ext = file_name.split(".")[-1]
    file_merger = importlib.import_module("format." + file_ext + ".merger")
    return file_merger.merge(file_before, file_after)

if __name__ == "__main__":
    file_before = sys.argv[1]
    file_after = sys.argv[2]
    try:
        file_output_name = sys.argv[3]
        saved_file = merge_file(file_before, file_after, file_output_name)
    except:
        saved_file = merge_file(file_before, file_after)
    print "File Saved: " + saved_file
