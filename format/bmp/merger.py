import sys
from parser.bmp import BMP
from parser.bmp_diff import BMP_DIFF


def merge(file_before, file_after):
    bmp_before = BMP()
    bmp_after = BMP()
    bmp_before.load_bmp_from_file(file_before)
    bmp_after.load_bmp_from_file(file_after)
    bmp_diff = BMP_DIFF()
    bmp_diff.diff(bmp_before, bmp_after)
    for attr in bmp_diff.attributes:
        if getattr(bmp_diff, attr)[0] != getattr(bmp_diff, attr)[1]:
            print "Parameter - " + attr + " not the same: " + getattr(bmp_diff, attr)[2]
            print "Cannot be merged."
            return -1
    option = raw_input("Choose your merge option: 1-All, 2-Pixel By Pixel: ")
    pixel_merged = {}
    if option == "2":
        for pixel_index, pixel_info in bmp_diff.pixel_diff.iteritems():
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
            for pixel_index, pixel_info in bmp_diff.pixel_diff.iteritems():
                pixel_merged[pixel_index] = pixel_info["after"]
        elif accept == "2":
            for pixel_index, pixel_info in bmp_diff.pixel_diff.iteritems():
                pixel_merged[pixel_index] = pixel_info["before"]
    print pixel_merged


if __name__ == "__main__":
    file_before = sys.argv[1]
    file_after = sys.argv[2]
    merge(file_before, file_after)
