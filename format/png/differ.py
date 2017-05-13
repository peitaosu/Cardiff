import sys, json
from PIL import Image
from parser.png_diff import PNG_DIFF

def diff(file_before, file_after):
    png_before = Image.open(file_before)
    png_after = Image.open(file_after)
    png_diff = PNG_DIFF()
    png_diff.diff(png_before, png_after)
    return png_diff

def make_diff(file_before, file_after, file_output_name):
    png_diff = diff(file_before, file_after)
    diff_content = {}
    for attr in png_diff.attributes:
        diff_content[attr] = {}
        diff_content[attr]["before"] = getattr(png_diff, attr)[0]
        diff_content[attr]["after"] = getattr(png_diff, attr)[1]
        if diff_content[attr]["before"] != diff_content[attr]["after"]:
            diff_content[attr]["diff"] = True
    diff_content["pixel"] = png_diff.pixel_diff
    with open(file_output_name + "diff.json", "w") as diff_file:
        json.dump(diff_content, diff_file, indent=4)
    return file_output_name + ".diff.json"

if __name__ == "__main__":
    file_before = sys.argv[1]
    file_after = sys.argv[2]
    diff(file_before, file_after)
