import sys, json
from PIL import Image
from parser.jpg_diff import JPG_DIFF
from format.util import *

def diff(file_before, file_after):
    """diff jpg file

    args:
        file_before (str)
        file_after (str)

    returns:
        jpg_diff (JPG_DIFF)
    """
    jpg_before = Image.open(file_before)
    jpg_after = Image.open(file_after)
    jpg_diff = JPG_DIFF()
    jpg_diff.diff(jpg_before, jpg_after)
    return jpg_diff

def make_diff(file_before, file_after, file_output_name):
    """diff jpg file and save as file

    args:
        file_before (str)
        file_after (str)
        file_output_name (str)

    returns:
        saved_files (list)
    """
    jpg_diff = diff(file_before, file_after)
    saved_diff_images = create_diff_image("RGB", tuple(jpg_diff.size[0]), jpg_diff.pixel_diff, file_output_name)
    saved_diff_json = create_diff_json(jpg_diff, file_output_name)
    saved_files = saved_diff_images
    saved_files.append(saved_diff_json)
    return saved_files
