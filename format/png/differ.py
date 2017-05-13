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
    diff_png_out = Image.new("RGBA", diff_content["size"]["after"])
    diff_png_out_data = diff_png_out.load()
    width, height = diff_png_out.size
    pixel_index = 1
    for y in xrange(height):
        for x in xrange(width):
            if str(pixel_index) in diff_content["pixel"]:
                diff_png_out_data[x, y] = (0, 0, 0, 255)
            else:
                diff_png_out_data[x, y] = (0, 0, 0, 0)
            pixel_index += 1
    diff_png_out.save(file_output_name + ".diff.png", "PNG")
    return file_output_name + ".diff.png"

if __name__ == "__main__":
    file_before = sys.argv[1]
    file_after = sys.argv[2]
    file_output_name = sys.argv[3]
    make_diff(file_before, file_after, file_output_name)