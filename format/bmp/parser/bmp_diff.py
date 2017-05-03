import sys

class BMP_DIFF():
    def __init__(self):
        self.attributes = ["bfSize", "biSize", "biWidth", "biHeight", "biBitCount", "biCompression", "biSizeImage", "biXPelsPerMeter", "biYPelsPerMeter", "biClrUsed", "biClrImportant"]

    def diff_spec(self, field, bmp_before, bmp_after):
        setattr(self, field,[])
        getattr(self, field).append(ord(bmp_before.get_spec_data(field)[0]))
        getattr(self, field).append(ord(bmp_after.get_spec_data(field)[0]))
        getattr(self, field).append(str(getattr(self, field)[0]) + " <---> " + str(getattr(self, field)[1]))

    def diff(self, bmp_before, bmp_after):
        for attr in self.attributes:
            self.diff_spec(attr, bmp_before, bmp_after)
