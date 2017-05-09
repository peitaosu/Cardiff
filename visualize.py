import os, sys, importlib, time

def visualize_diff(file_diff, file_after, file_ext, file_output_name = None):
    file_visualizer = importlib.import_module("format." + file_ext + ".visualizer")
    if file_output_name == None:
        file_output_name = str(time.time())
    saved_file = file_visualizer.visualize(file_diff, file_after, file_output_name)
    return saved_file
