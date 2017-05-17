import os, sys
from parser.bmp import BMP
from parser.bmp_diff import BMP_DIFF

def parameterize(file_diff):
    """print formatted diff data

    args:
        file_diff (BMP_DIFF)
    """
    print "{:>48} : {:>8} <---> {:<8}".format("============ Parameters ============", "before", "after")
    for i in range(len(file_diff.attributes)):
        print "{:>48} : {:>8} <---> {:<8}".format(file_diff.description[i], getattr(file_diff, file_diff.attributes[i])[0], getattr(file_diff, file_diff.attributes[i])[1])
    print "{:>48} : {:>12}".format("Pixel Changed", str(len(file_diff.pixel_diff)))
