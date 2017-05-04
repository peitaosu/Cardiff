import sys, json
from parser.bmp import BMP
from parser.bmp_diff import BMP_DIFF

def diff(file_before, file_after):
    bmp_before = BMP()
    bmp_after = BMP()
    bmp_before.load_bmp_from_file(file_before)
    bmp_after.load_bmp_from_file(file_after)
    bmp_diff = BMP_DIFF()
    bmp_diff.diff(bmp_before, bmp_after)
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
    with open(file_output_name + ".diff.json", "w") as diff_file:
        json.dump(diff_content, diff_file, indent=4)
    # TODO: save *.diff.bmp file

if __name__ == "__main__":
    file_before = sys.argv[1]
    file_after = sys.argv[2]
    file_output_name = sys.argv[3]
    make_diff(file_before, file_after, file_output_name)