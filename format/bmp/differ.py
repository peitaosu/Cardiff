import sys
import json
from parser.bmp import BMP
from parser.bmp_diff import BMP_DIFF

def diff(file_before, file_after):
    bmp_before = BMP()
    bmp_after = BMP()
    bmp_before.load_bmp_from_file(file_before)
    bmp_after.load_bmp_from_file(file_after)
    bmp_diff = BMP_DIFF()
    bmp_diff.diff(bmp_before, bmp_after)
    bmp_diff.diff_pixel(bmp_before, bmp_after)
    return bmp_diff

def make_diff(file_before, file_after, file_output_name):
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
    diff_bmp_out = BMP()
    diff_bmp_out.load_bmp_from_file(file_before)
    diff_bmp_out.get_bmp_pixel_data()
    pixel_start = diff_bmp_out.FORMAT_PIXEL_DATA[0]
    pixel_length = diff_bmp_out.FORMAT_PIXEL_DATA[1]
    diff_bmp_out_data = diff_bmp_out.bmp_data[:pixel_start]
    for i in range(pixel_length / 3):
        if str(i + 1) in bmp_diff.pixel_diff:
            diff_bmp_out_data = diff_bmp_out_data + \
                chr(255) + chr(255) + chr(255)
        else:
            diff_bmp_out_data = diff_bmp_out_data + chr(0) + chr(0) + chr(0)
    with open(file_output_name + ".diff.bmp", "wb") as diff_file:
        diff_file.write(diff_bmp_out_data)
    return file_output_name + ".diff.bmp"


if __name__ == "__main__":
    file_before = sys.argv[1]
    file_after = sys.argv[2]
    file_output_name = sys.argv[3]
    make_diff(file_before, file_after, file_output_name)