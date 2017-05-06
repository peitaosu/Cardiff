import os, sys, time
from differ import diff
from parser.bmp import BMP
from parser.bmp_diff import *


def visualize(file_diff, file_output_name = None):
    bmp_data = []
    bmp_data += chr(66) + chr(77)
    bmp_data += int_to_bytes(file_diff.bfSize[0], 4)
    bmp_data += chr(0) * 4
    bmp_data += int_to_bytes(file_diff.bfOffBits[0], 4)
    bmp_data += int_to_bytes(file_diff.biSize[0], 4)
    bmp_data += int_to_bytes(file_diff.biWidth[0], 4)
    bmp_data += int_to_bytes(file_diff.biHeight[0], 4)
    bmp_data += chr(1) + chr(0)
    bmp_data += int_to_bytes(file_diff.biBitCount[0], 2)
    bmp_data += int_to_bytes(file_diff.biCompression[0], 4)
    bmp_data += int_to_bytes(file_diff.biSizeImage[0], 4)
    bmp_data += int_to_bytes(file_diff.biXPelsPerMeter[0], 4)
    bmp_data += int_to_bytes(file_diff.biYPelsPerMeter[0], 4)
    bmp_data += int_to_bytes(file_diff.biClrUsed[0], 4)
    bmp_data += int_to_bytes(file_diff.biClrImportant[0], 4)
    bmp_data += "BGRs"
    bmp_data += chr(0) * (file_diff.bfOffBits[0] - 58)
    for i in range(file_diff.biSizeImage[0]):
        if str(i + 1) in file_diff.pixel_diff:
            bmp_data += chr(255) * 3
        else:
            bmp_data += chr(0) * 3
    if file_output_name == None:
        file_output_name = str(time.time())
    with open(file_output_name + ".diff.bmp", "wb") as diff_file:
        diff_file.write(bytearray(bmp_data))
    os.system("open " + file_output_name + ".diff.bmp")

if __name__ == "__main__":
    bmp_before = BMP()
    bmp_after = BMP()
    bmp_before.load_bmp_from_file(sys.argv[1])
    bmp_after.load_bmp_from_file(sys.argv[2])
    bmp_diff = BMP_DIFF()
    bmp_diff.diff(bmp_before, bmp_after)
    try:
        file_output_name = sys.argv[3]
        visualize(bmp_diff, file_output_name)
    except:
        visualize(bmp_diff)
