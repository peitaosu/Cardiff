import os, sys
from parser.bmp import BMP
from parser.bmp_diff import BMP_DIFF


def merge(file_before, file_after):
    """merge bmp diff

    args:
        file_before (str)
        file_after (str)

    returns:
        pixel_merged (dict)
    """
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
    if "AUTO_MERGE" not in os.environ:
        option = raw_input("Choose your merge option: 1-All, 2-Pixel By Pixel: ")
    else:
        option = os.getenv("AUTO_MERGE")
    pixel_merged = {}
    if option == "2":
        for pixel_index, pixel_info in bmp_diff.pixel_diff.iteritems():
            pixel_merged[pixel_index] = {}
            print "Pixel: " + pixel_index
            print "Before: " + ", ".join([str(p) for p in pixel_info["before"]])
            print "After: " + ", ".join([str(p) for p in pixel_info["after"]])
            if "AUTO_ACCEPT" not in os.environ:
                accept = raw_input(
                    "Choose your merge option: 1-Accept After, 2-Accept Before: ")
            else:
                accept = os.getenv("AUTO_ACCEPT")
            if accept == "1":
                pixel_merged[pixel_index] = pixel_info["after"]
            elif accept == "2":
                pixel_merged[pixel_index] = pixel_info["before"]
    elif option == "1":
        if "AUTO_ACCEPT" not in os.environ:
            accept = raw_input(
                "Choose your merge option: 1-Accept After, 2-Accept Before: ")
        else:
            accept = os.getenv("AUTO_ACCEPT")
        if accept == "1":
            for pixel_index, pixel_info in bmp_diff.pixel_diff.iteritems():
                pixel_merged[pixel_index] = pixel_info["after"]
        elif accept == "2":
            for pixel_index, pixel_info in bmp_diff.pixel_diff.iteritems():
                pixel_merged[pixel_index] = pixel_info["before"]
    return pixel_merged


def make_merged(file_before, file_after, file_output_name):
    """merge bmp diff and save as file

    args:
        file_before (str)
        file_after (str)
        file_output_name (str)
    """
    merged_bmp_out = BMP()
    merged_bmp_out.load_bmp_from_file(file_after)
    merged_bmp_out.get_bmp_pixel_data()
    pixel_start = merged_bmp_out.FORMAT_PIXEL_DATA[0]
    pixel_length = merged_bmp_out.FORMAT_PIXEL_DATA[1]
    merged_bmp_out_data = merged_bmp_out.bmp_data[:pixel_start]
    pixel_merged = merge(file_before, file_after)
    for i in range(pixel_length / 3):
        if str(i + 1) in pixel_merged:
            merged_bmp_out_data = merged_bmp_out_data + \
                chr(pixel_merged[str(i + 1)][2]) + chr(pixel_merged[str(i + 1)][1]) + chr(pixel_merged[str(i + 1)][0])
        else:
            merged_bmp_out_data = merged_bmp_out_data + \
                merged_bmp_out.bmp_data[pixel_start + i * 3 + 0 : pixel_start + i * 3 + 3]
    with open(file_output_name + ".merged.bmp", "wb") as merged_file:
        merged_file.write(merged_bmp_out_data)

