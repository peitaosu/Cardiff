import sys, json
from PIL import Image
from parser.png_diff import PNG_DIFF
from format.util import create_diff_image

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
        saved_file (str)
    """
    png_diff = diff(file_before, file_after)
    diff_content = {}
    for attr in png_diff.attributes:
        diff_content[attr] = {}
        diff_content[attr]["before"] = getattr(png_diff, attr)[0]
        diff_content[attr]["after"] = getattr(png_diff, attr)[1]
        if diff_content[attr]["before"] != diff_content[attr]["after"]:
            diff_content[attr]["diff"] = True
    diff_content["pixel"] = png_diff.pixel_diff
    with open(file_output_name + ".diff.json", "w") as diff_file:
        json.dump(diff_content, diff_file, indent=4)
    return create_diff_image("RGBA", diff_content["size"]["before"], diff_content["pixel"], file_output_name)
