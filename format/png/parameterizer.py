import os, sys
from PIL import Image
from parser.png_diff import PNG_DIFF

def parameterize(file_diff):
    """print formatted diff data

    args:
        file_diff (PNG_DIFF)
    """
    print "{:>48} : {:>8} <---> {:<8}".format("============ Parameters ============", "before", "after")
    for i in range(len(file_diff.attributes)):
        print "{:>48} : {:>8} <---> {:<8}".format(file_diff.description[i], getattr(file_diff, file_diff.attributes[i])[0], getattr(file_diff, file_diff.attributes[i])[1])
    print "{:>48} : {:>12}".format("Pixel Changed", str(len(file_diff.pixel_diff)))

if __name__ == "__main__":
    png_before = Image.open(sys.argv[1])
    png_after = Image.open(sys.argv[2])
    png_diff = PNG_DIFF()
    png_diff.diff(png_before, png_after)
    parameterize(png_diff)
