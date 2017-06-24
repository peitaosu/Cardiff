import sys
import json
from parser.bmp import BMP
from parser.bmp_diff import BMP_DIFF
from format.util import *

def diff(file_before, file_after):
    """diff bmp file

    args:
        file_before (str)
        file_after (str)

    returns:
        bmp_diff (BMP_DIFF)
    """
    bmp_before = BMP()
    bmp_after = BMP()
    bmp_before.load_bmp_from_file(file_before)
    bmp_after.load_bmp_from_file(file_after)
    bmp_diff = BMP_DIFF()
    bmp_diff.diff(bmp_before, bmp_after)
    bmp_diff.diff_pixel(bmp_before, bmp_after)
    return bmp_diff

def make_diff(file_before, file_after, file_output_name):
    """diff bmp file and save as file

    args:
        file_before (str)
        file_after (str)
        file_output_name (str)

    returns:
        saved_files (list)
    """
    bmp_diff = diff(file_before, file_after)
    saved_diff_images = create_diff_image("RGB", (bmp_diff.biWidth[0], bmp_diff.biHeight[0]), bmp_diff.pixel_diff, file_output_name, "y")
    saved_diff_json = create_diff_json(bmp_diff, file_output_name)
    saved_files = saved_diff_images
    saved_files.append(saved_diff_json)
    return saved_files
