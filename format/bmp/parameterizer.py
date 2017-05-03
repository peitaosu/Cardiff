import os, sys
from parser.bmp import BMP
from parser.bmp_diff import BMP_DIFF

def parameterize(file_diff):
    print "{:>48}".format("============ Parameters ============") + " : " + "{:>8}".format("before") + " <---> " + "{:<8}".format("after")
    for i in range(len(file_diff.attributes)):
        print "{:>48}".format(file_diff.description[i]) + " : " + "{:>8}".format(getattr(file_diff, file_diff.attributes[i])[0]) + " <---> " + "{:<8}".format(getattr(file_diff, file_diff.attributes[i])[1])


if __name__ == "__main__":
    bmp_before = BMP()
    bmp_after = BMP()
    bmp_before.load_bmp_from_file(sys.argv[1])
    bmp_after.load_bmp_from_file(sys.argv[2])
    bmp_diff = BMP_DIFF()
    bmp_diff.diff(bmp_before, bmp_after)
    parameterize(bmp_diff)

