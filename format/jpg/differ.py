import sys, json
from PIL import Image
from parser.jpg_diff import JPG_DIFF

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
    diff_jpg_out = Image.new("RGB", diff_content["size"]["after"])
    diff_jpg_out_data = diff_jpg_out.load()
    width, height = diff_jpg_out.size
    pixel_index = 1
    for y in xrange(height):
        for x in xrange(width):
            if str(pixel_index) in diff_content["pixel"]:
                diff_jpg_out_data[x, y] = (0, 0, 0)
            else:
                diff_jpg_out_data[x, y] = (0, 0, 0)
            pixel_index += 1
    diff_jpg_out.save(file_output_name + ".diff.jpg", "JPG")
    return file_output_name + ".diff.jpg"

if __name__ == "__main__":
    file_before = sys.argv[1]
    file_after = sys.argv[2]
    file_output_name = sys.argv[3]
    make_diff(file_before, file_after, file_output_name)