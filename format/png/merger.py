import os, sys
from PIL import Image
from parser.png_diff import PNG_DIFF


def merge(file_before, file_after):
    """merge png diff

    args:
        file_before (str)
        file_after (str)

    returns:
        pixel_merged (dict)
    """
    png_before = Image.open(file_before)
    png_after = Image.open(file_after)
    png_diff = PNG_DIFF()
    png_diff.diff(png_before, png_after)
    for attr in png_diff.attributes:
        if getattr(png_diff, attr)[0] != getattr(png_diff, attr)[1]:
            print "Parameter - " + attr + " not the same: " + getattr(png_diff, attr)[2]
            print "Cannot be merged."
            return -1
    if "AUTO_MERGE" not in os.environ:
        option = raw_input("Choose your merge option: 1-All, 2-Pixel By Pixel: ")
    else:
        option = os.getenv("AUTO_MERGE")
    pixel_merged = {}
    if option == "2":
        for pixel_index, pixel_info in png_diff.pixel_diff.iteritems():
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
            for pixel_index, pixel_info in png_diff.pixel_diff.iteritems():
                pixel_merged[pixel_index] = pixel_info["after"]
        elif accept == "2":
            for pixel_index, pixel_info in png_diff.pixel_diff.iteritems():
                pixel_merged[pixel_index] = pixel_info["before"]
    return pixel_merged


def make_merged(file_before, file_after, file_output_name):
    """merge png diff and save as file

    args:
        file_before (str)
        file_after (str)
        file_output_name (str)

    returns:
        merged_file (str)
    """
    merged_png_out = Image.open(file_after)
    merged_png_out_data = merged_png_out.load()
    pixel_merged = merge(file_before, file_after)
    width, height = merged_png_out.size
    pixel_index = 1
    for y in xrange(height):
        for x in xrange(width):
            if str(pixel_index) in pixel_merged:
                print pixel_merged[str(pixel_index)]
                merged_png_out_data[x, y] = tuple(pixel_merged[str(pixel_index)])
            pixel_index += 1
    merged_png_out.save(file_output_name + ".merged.png", "PNG")
    return file_output_name + ".merged.png"

