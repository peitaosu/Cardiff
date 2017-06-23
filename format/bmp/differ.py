import sys
import json
from parser.bmp import BMP
from parser.bmp_diff import BMP_DIFF
from format.util import create_diff_image

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
        saved_file (str)
    """
    bmp_diff = diff(file_before, file_after)
    diff_content = {}
    for attr in bmp_diff.attributes:
        diff_content[attr] = {}
        diff_content[attr]["before"] = getattr(bmp_diff, attr)[0]
        diff_content[attr]["after"] = getattr(bmp_diff, attr)[1]
        if diff_content[attr]["before"] != diff_content[attr]["after"]:
            diff_content[attr]["diff"] = True
    diff_content["pixel"] = bmp_diff.pixel_diff
    with open(file_output_name + ".diff.json", "w") as diff_file:
        json.dump(diff_content, diff_file, indent=4)
    return create_diff_image("RGB", (int(diff_content["biWidth"]["before"]), int(diff_content["biHeight"]["before"])), diff_content["pixel"], file_output_name)

