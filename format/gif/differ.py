import sys, json
from PIL import Image
from parser.gif_diff import GIF_DIFF
from format.util import *

def diff(file_before, file_after):
    """diff gif file

    args:
        file_before (str)
        file_after (str)

    returns:
        gif_diff (GIF_DIFF)
    """
    gif_before = Image.open(file_before)
    gif_after = Image.open(file_after)
    gif_diff = GIF_DIFF()
    gif_diff.diff(gif_before, gif_after)
    return gif_diff

def make_diff(file_before, file_after, file_output_name):
    """diff gif file and save as file

    args:
        file_before (str)
        file_after (str)
        file_output_name (str)

    returns:
        saved_files (list)
    """
    gif_diff = diff(file_before, file_after)
    saved_diff_images = create_diff_image("RGBA", tuple(gif_diff.size[0]), gif_diff.pixel_diff, file_output_name)
    saved_diff_json = create_diff_json(gif_diff, file_output_name)
    saved_files = saved_diff_images
    saved_files.append(saved_diff_json)
    return saved_files
