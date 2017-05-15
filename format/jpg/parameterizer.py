import os, sys
from PIL import Image
from parser.jpg_diff import JPG_DIFF

def parameterize(file_diff):
    """print formatted diff data

    args:
        file_diff (JPG_DIFF)
    """
    print "{:>48} : {:>8} <---> {:<8}".format("============ Parameters ============", "before", "after")
    for i in range(len(file_diff.attributes)):
        print "{:>48} : {:>8} <---> {:<8}".format(file_diff.description[i], getattr(file_diff, file_diff.attributes[i])[0], getattr(file_diff, file_diff.attributes[i])[1])
    print "{:>48} : {:>12}".format("Pixel Changed", str(len(file_diff.pixel_diff)))

if __name__ == "__main__":
    jpg_before = Image.open(sys.argv[1])
    jpg_after = Image.open(sys.argv[2])
    jpg_diff = JPG_DIFF()
    jpg_diff.diff(jpg_before, jpg_after)
    parameterize(jpg_diff)
