from format.util import *

def visualize(file_before, file_diff_before, file_diff_after, file_after, file_output_name = None):
    """visualize the jpg diff, open with Tk window or save as file

    args:
        file_before (str)
        file_diff_before (str)
        file_diff_after (str)
        file_after (str)
        file_output_name (str)
    """
    if file_output_name == None:
        visualize_image_as_window([file_before, file_diff_before, file_diff_after, file_after])
    else:
        visualize_image_as_png(file_diff_before, file_diff_after, file_output_name)

