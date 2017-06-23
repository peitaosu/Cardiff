import sys, json
from PIL import Image
from parser.gif_diff import GIF_DIFF
from format.differ import create_diff_image

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
        saved_file (str)
    """
    gif_diff = diff(file_before, file_after)
    diff_content = {}
    for attr in gif_diff.attributes:
        diff_content[attr] = {}
        diff_content[attr]["before"] = getattr(gif_diff, attr)[0]
        diff_content[attr]["after"] = getattr(gif_diff, attr)[1]
        if diff_content[attr]["before"] != diff_content[attr]["after"]:
            diff_content[attr]["diff"] = True
    diff_content["pixel"] = gif_diff.pixel_diff
    with open(file_output_name + "diff.json", "w") as diff_file:
        json.dump(diff_content, diff_file, indent=4)
    return create_diff_image("RGBA", diff_content["size"]["before"], diff_content["pixel"], file_output_name)
