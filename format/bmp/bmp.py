import sys

class BMP():
    def __init__(self):
        self.FORMAT_FILE_HEADER = {
            "bfType": {"start": 0, "length": 2},
            "bfSize": {"start": 2, "length": 4},
            "bfReserved1": {"start": 6, "length": 2},
            "bfReserved2": {"start": 8, "length": 2},
            "bfOffBits": {"start": 10, "length": 4}
        }
        self.FORMAT_IMAGE_HEADER = {
            "biSize": {"start": 14, "length": 4},
            "biWidth": {"start": 18, "length": 4},
            "biHeight": {"start": 22, "length": 4},
            "biPlanes": {"start": 26, "length": 2},
            "biBitCount": {"start": 28, "length": 2},
            "biCompression": {"start": 30, "length": 4},
            "biSizeImage": {"start": 34, "length": 4},
            "biXPelsPerMeter": {"start": 38, "length": 4},
            "biYPelsPerMeter": {"start": 42, "length": 4},
            "biClrUsed": {"start": 46, "length": 4},
            "biClrImportant": {"start": 50, "length": 4}
        }
        self.FORMAT_COLOR_TABLE = {}
        self.FORMAT_PIXEL_DATA = {}
        self.data = []
    
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
        return self.bmp_data[chunk["start"]: chunk["start"] + chunk["length"]]
    
    def get_bmp_color_table(self):
        bmp_bfOffBits = self.get_spec_data("bfOffBits")
        self.FORMAT_COLOR_TABLE["start"] = 54
        self.FORMAT_COLOR_TABLE["length"] = ord(bmp_bfOffBits[0]) - 54
        return self.bmp_data[54: ord(bmp_bfOffBits[0])-1]
    
    def get_bmp_pixel_data(self):
        bmp_bfOffBits = self.get_spec_data("bfOffBits")
        self.FORMAT_PIXEL_DATA["start"] = ord(bmp_bfOffBits[0])
        self.FORMAT_PIXEL_DATA["length"] = len(self.bmp_data) - ord(bmp_bfOffBits[0])
        return self.bmp_data[ord(bmp_bfOffBits[0]): ]

if __name__ == "__main__":
    bmp = BMP()
    bmp.load_bmp_from_file(sys.argv[1])
    for byte in bmp.get_bmp_pixel_data():
        print "{:02x}".format(ord(byte)),

