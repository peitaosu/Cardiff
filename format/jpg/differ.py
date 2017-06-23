import sys, json
from PIL import Image
from parser.jpg_diff import JPG_DIFF
from format.differ import create_diff_image

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
        saved_file (str)
    """
    jpg_diff = diff(file_before, file_after)
    diff_content = {}
    for attr in jpg_diff.attributes:
        diff_content[attr] = {}
        diff_content[attr]["before"] = getattr(jpg_diff, attr)[0]
        diff_content[attr]["after"] = getattr(jpg_diff, attr)[1]
        if diff_content[attr]["before"] != diff_content[attr]["after"]:
            diff_content[attr]["diff"] = True
    diff_content["pixel"] = jpg_diff.pixel_diff
    with open(file_output_name + "diff.json", "w") as diff_file:
        json.dump(diff_content, diff_file, indent=4)
    return create_diff_image("RGB", diff_content["size"]["before"], diff_content["pixel"], file_output_name)
