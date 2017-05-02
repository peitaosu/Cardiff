import sys
from parser.bmp import BMP

def diff(file_before, file_after):
    bmp_before = BMP()
    bmp_after = BMP()
    bmp_before.load_bmp_from_file(file_before)
    bmp_after.load_bmp_from_file(file_after)
    #TODO: create diff file which can be visualized and parameterized

if __name__ == "__main__":
    file_before = sys.argv[1]
    file_after = sys.argv[2]
    diff(file_before, file_after)
