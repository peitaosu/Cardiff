import sys
from PIL import Image
from parser.jpg_diff import JPG_DIFF


def merge(file_before, file_after):
    """merge jpg diff

    args:
        file_before (str)
        file_after (str)

    returns:
        pixel_merged (dict)
    """
    jpg_before = Image.open(file_before)
    jpg_after = Image.open(file_after)
    jpg_diff = JPG_DIFF()
    jpg_diff.diff(jpg_before, jpg_after)
    for attr in jpg_diff.attributes:
        if getattr(jpg_diff, attr)[0] != getattr(jpg_diff, attr)[1]:
            print "Parameter - " + attr + " not the same: " + getattr(jpg_diff, attr)[2]
            print "Cannot be merged."
            return -1
    option = raw_input("Choose your merge option: 1-All, 2-Pixel By Pixel: ")
    pixel_merged = {}
    if option == "2":
        for pixel_index, pixel_info in jpg_diff.pixel_diff.iteritems():
            pixel_merged[pixel_index] = {}
            print "Pixel: " + pixel_index
            print "Before: " + ", ".join([str(p) for p in pixel_info["before"]])
            print "After: " + ", ".join([str(p) for p in pixel_info["after"]])
            accept = raw_input(
                "Choose your merge option: 1-Accept After, 2-Accept Before: ")
            if accept == "1":
                pixel_merged[pixel_index] = pixel_info["after"]
            elif accept == "2":
                pixel_merged[pixel_index] = pixel_info["before"]
    elif option == "1":
        accept = raw_input(
            "Choose your merge option: 1-Accept After, 2-Accept Before: ")
        if accept == "1":
            for pixel_index, pixel_info in jpg_diff.pixel_diff.iteritems():
                pixel_merged[pixel_index] = pixel_info["after"]
        elif accept == "2":
            for pixel_index, pixel_info in jpg_diff.pixel_diff.iteritems():
                pixel_merged[pixel_index] = pixel_info["before"]
    return pixel_merged


def make_merged(file_before, file_after, file_output_name):
    """merge jpg diff and save as file

    args:
        file_before (str)
        file_after (str)
        file_output_name (str)
    """
    merged_jpg_out = Image.open(file_after)
    merged_jpg_out_data = merged_jpg_out.load()
    pixel_merged = merge(file_before, file_after)
    width, height = merged_jpg_out.size
    pixel_index = 1
    for y in xrange(height):
        for x in xrange(width):
            if str(pixel_index) in pixel_merged:
                print pixel_merged[str(pixel_index)]
                merged_jpg_out_data[x, y] = tuple(pixel_merged[str(pixel_index)])
            pixel_index += 1
    merged_jpg_out.save(file_output_name + ".merged.jpg", "JPEG")
    return file_output_name + ".merged.jpg"


if __name__ == "__main__":
    file_before = sys.argv[1]
    file_after = sys.argv[2]
    file_output_name = sys.argv[3]
    make_merged(file_before, file_after, file_output_name)
