from format.util import *

def visualize(file_before, file_diffs, file_after, file_output_name = None):
    """visualize the jpg diff, open with Tk window or save as file

    args:
        file_before (str)
        file_diffs (list)
        file_after (str)
        file_output_name (str)
    """
    if file_output_name == None:
        visualize_image_as_window([file_before, file_diffs[0], file_diffs[1], file_after])
    else:
        visualize_image_as_png(file_diffs[0], file_diffs[1], file_output_name)

