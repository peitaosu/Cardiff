import os, sys
from parser.bmp import BMP
from parser.bmp_diff import BMP_DIFF
from format.util import parameterize_image_diff

def parameterize(file_diff):
    """print formatted diff data

    args:
        file_diff (BMP_DIFF)
    """
    parameterize_image_diff(file_diff)
