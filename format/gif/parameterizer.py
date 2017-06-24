import os, sys
from PIL import Image
from parser.gif_diff import GIF_DIFF
from format.util import parameterize_image_diff

def parameterize(file_diff):
    """print formatted diff data

    args:
        file_diff (GIF_DIFF)
    """
    parameterize_image_diff(file_diff)

