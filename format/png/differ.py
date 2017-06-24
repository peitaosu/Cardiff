import sys, json
from PIL import Image
from parser.png_diff import PNG_DIFF
from format.util import *

def diff(file_before, file_after):
    """diff png file

    args:
        file_before (str)
        file_after (str)

    returns:
        png_diff (PNG_DIFF)
    """
    png_before = Image.open(file_before)
    png_after = Image.open(file_after)
    png_diff = PNG_DIFF()
    png_diff.diff(png_before, png_after)
    return png_diff

def make_diff(file_before, file_after, file_output_name):
    """diff png file and save as file

    args:
        file_before (str)
        file_after (str)
        file_output_name (str)

    returns:
        saved_files (list)
    """
    png_diff = diff(file_before, file_after)
    saved_diff_images = create_diff_image("RGBA", tuple(png_diff.size[0]), png_diff.pixel_diff, file_output_name)
    saved_diff_json = create_diff_json(png_diff, file_output_name)
    saved_files = saved_diff_images
    saved_files.append(saved_diff_json)
    return saved_files
