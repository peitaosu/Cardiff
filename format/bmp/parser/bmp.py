# https://en.wikipedia.org/wiki/BMP_file_format

import sys


class BMP():
    def __init__(self):
        self.FORMAT_FILE_HEADER = {
            "bfType": [0, 2],
            "bfSize": [2, 4],
            "bfReserved1": [6, 2],
            "bfReserved2": [8, 2],
            "bfOffBits": [10, 4]
        }
        self.FORMAT_IMAGE_HEADER = {
            "biSize": [14, 4],
            "biWidth": [18, 4],
            "biHeight": [22, 4],
            "biPlanes": [26, 2],
            "biBitCount": [28, 2],
            "biCompression": [30, 4],
            "biSizeImage": [34, 4],
            "biXPelsPerMeter": [38, 4],
            "biYPelsPerMeter": [42, 4],
            "biClrUsed": [46, 4],
            "biClrImportant": [50, 4]
        }
        self.FORMAT_COLOR_TABLE = {}
        self.FORMAT_PIXEL_DATA = {}

    def load_bmp_from_file(self, file_path):
        with open(file_path, "rb") as bmp_file:
            self.bmp_data = bmp_file.read()

    def print_bmp_data(self):
        for byte in self.bmp_data:
            print "{:02x}".format(ord(byte)),

    def get_spec_data(self, field):
        if field in self.FORMAT_FILE_HEADER:
            chunk = self.FORMAT_FILE_HEADER[field]
        elif field in self.FORMAT_IMAGE_HEADER:
            chunk = self.FORMAT_IMAGE_HEADER[field]
        else:
            return False
        return self.bmp_data[chunk[0]: chunk[0] + chunk[1]]

    def get_bmp_color_table(self):
        bmp_bfOffBits = self.get_spec_data("bfOffBits")
        self.FORMAT_COLOR_TABLE[0] = 54
        self.FORMAT_COLOR_TABLE[1] = ord(bmp_bfOffBits[0]) - 54
        return self.bmp_data[54: ord(bmp_bfOffBits[0]) - 1]

    def get_bmp_pixel_data(self):
        bmp_bfOffBits = self.get_spec_data("bfOffBits")
        self.FORMAT_PIXEL_DATA[0] = ord(bmp_bfOffBits[0])
        self.FORMAT_PIXEL_DATA[1] = len(self.bmp_data) - ord(bmp_bfOffBits[0])
        return self.bmp_data[ord(bmp_bfOffBits[0]):]


if __name__ == "__main__":
    bmp = BMP()
    bmp.load_bmp_from_file(sys.argv[1])
    for byte in bmp.get_bmp_pixel_data():
        print "{:02x}".format(ord(byte)),
