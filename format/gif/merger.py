import sys
from PIL import Image
from parser.gif_diff import GIF_DIFF


def merge(file_before, file_after, default_option="0", default_accept="0"):
    """merge gif diff

    args:
        file_before (str)
        file_after (str)

    returns:
        pixel_merged (dict)
    """
    gif_before = Image.open(file_before)
    gif_after = Image.open(file_after)
    gif_diff = GIF_DIFF()
    gif_diff.diff(gif_before, gif_after)
    for attr in gif_diff.attributes:
        if getattr(gif_diff, attr)[0] != getattr(gif_diff, attr)[1]:
            print "Parameter - " + attr + " not the same: " + getattr(gif_diff, attr)[2]
            print "Cannot be merged."
            return -1
    if default_option == "0":
        option = raw_input("Choose your merge option: 1-All, 2-Pixel By Pixel: ")
    else:
        option = default_option
    pixel_merged = {}
    if option == "2":
        for pixel_index, pixel_info in gif_diff.pixel_diff.iteritems():
            pixel_merged[pixel_index] = {}
            print "Pixel: " + pixel_index
            print "Before: " + ", ".join([str(p) for p in pixel_info["before"]])
            print "After: " + ", ".join([str(p) for p in pixel_info["after"]])
            if default_accept == "0":
                accept = raw_input(
                    "Choose your merge option: 1-Accept After, 2-Accept Before: ")
            else:
                accept = default_accept
            if accept == "1":
                pixel_merged[pixel_index] = pixel_info["after"]
            elif accept == "2":
                pixel_merged[pixel_index] = pixel_info["before"]
    elif option == "1":
        if default_accept == "0":
            accept = raw_input(
                "Choose your merge option: 1-Accept After, 2-Accept Before: ")
        else:
            accept = default_accept
        if accept == "1":
            for pixel_index, pixel_info in gif_diff.pixel_diff.iteritems():
                pixel_merged[pixel_index] = pixel_info["after"]
        elif accept == "2":
            for pixel_index, pixel_info in gif_diff.pixel_diff.iteritems():
                pixel_merged[pixel_index] = pixel_info["before"]
    return pixel_merged


def make_merged(file_before, file_after, file_output_name):
    """merge gif diff and save as file

    args:
        file_before (str)
        file_after (str)
        file_output_name (str)
    """
    merged_gif_out = Image.open(file_after)
    merged_gif_out = merged_gif_out.convert("RGBA")
    merged_gif_out_data = merged_gif_out.load()
    pixel_merged = merge(file_before, file_after)
    width, height = merged_gif_out.size
    pixel_index = 1
    for y in xrange(height):
        for x in xrange(width):
            if str(pixel_index) in pixel_merged:
                merged_gif_out_data[x, y] = tuple(pixel_merged[str(pixel_index)])
            pixel_index += 1
    merged_gif_out.save(file_output_name + ".merged.gif", "GIF")
    return file_output_name + ".merged.gif"

