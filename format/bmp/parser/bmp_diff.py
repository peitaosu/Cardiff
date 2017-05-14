import sys, struct
from format.image_diff import IMAGE_DIFF

def bytes_to_int(bytes):
    result = ord(bytes[0])
    for b in bytes[1:]:
        result = result + ord(b) * 256
    return result

def int_to_bytes(value, length):
    result = []
    for i in range(0, length):
        result.append(value >> (i * 8) & 0xff)
    return result

class BMP_DIFF(IMAGE_DIFF):
    def __init__(self):
        self.attributes = ["bfSize", "bfOffBits", "biSize", "biWidth", "biHeight", "biBitCount", "biCompression",
                           "biSizeImage", "biXPelsPerMeter", "biYPelsPerMeter", "biClrUsed", "biClrImportant"]
        self.description = ["The size of the file in bytes", "Offset to start of Pixel Data", "Header Size", "Image width in pixels", "Image height in pixels", "Bits per pixel", "Compression typ", "Image Size",
                            "Preferred resolution in pixels per meter", "Preferred resolution in pixels per meter", "Number Color Map entries that are actually used", "Number of significant colors"]

    def diff_spec(self, field, bmp_before, bmp_after):
        """diff bmp file parameters and set the attributes

        args:
            field (str)
            bmp_before (BMP)
            bmp_after (BMP)
        """
        setattr(self, field, [])
        getattr(self, field).append(bytes_to_int(bmp_before.get_spec_data(field)))
        getattr(self, field).append(bytes_to_int(bmp_after.get_spec_data(field)))
        getattr(self, field).append(str(getattr(self, field)[
            0]) + " <---> " + str(getattr(self, field)[1]))

    def diff_pixel(self, bmp_before, bmp_after):
        """diff bmp file pixels and return the pixel diff

        args:
            bmp_before (BMP)
            bmp_after (BMP)

        returns:
            pixel_diff (dict)
        """
        pixel_data_before = bmp_before.get_bmp_pixel_data()
        pixel_data_after = bmp_after.get_bmp_pixel_data()
        index = 0
        pixel_diff = {}
        while index < len(pixel_data_before):
            if pixel_data_before[index] == pixel_data_after[index]:
                if pixel_data_before[index + 1] == pixel_data_after[index + 1]:
                    if pixel_data_before[index + 2] == pixel_data_after[index + 2]:
                        index += 3
                        continue
            pixel_index = index / 3 + 1
            pixel_diff[str(pixel_index)] = {}
            pixel_rgb_before = []
            pixel_rgb_after = []
            for i in range(3):
                pixel_rgb_before.append(ord(pixel_data_before[index + 2 - i]))
                pixel_rgb_after.append(ord(pixel_data_after[index + 2 - i]))
            pixel_diff[str(pixel_index)]["before"] = pixel_rgb_before
            pixel_diff[str(pixel_index)]["after"] = pixel_rgb_after
            index += 3
        return pixel_diff
