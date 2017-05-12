import sys
from PIL import Image
from parser.png_diff import PNG_DIFF

def diff(file_before, file_after):
    png_before = Image.open(file_before)
    png_after = Image.open(file_after)
    png_diff = PNG_DIFF()
    png_diff.diff(png_before, png_after)
    print png_diff.pixel_diff

if __name__ == "__main__":
    file_before = sys.argv[1]
    file_after = sys.argv[2]
    diff(file_before, file_after)
