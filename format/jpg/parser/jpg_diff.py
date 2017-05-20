import PIL
from format.image_diff import IMAGE_DIFF

class JPG_DIFF(IMAGE_DIFF):
    def __init__(self):
        self.attributes = ["mode", "size", "bits"]
        self.description = ["Color Mode", "Image Size", "Image Bits"]

    def diff_pixel(self, jpg_before, jpg_after):
        """diff jpg file pixels and return the pixel diff

        args:
            jpg_before (PIL.Image)
            jpg_after (PIL.Image)

        returns:
            pixel_diff (dict)
        """
        pixel_data_before = jpg_before.load()
        pixel_data_after = jpg_after.load()
        pixel_index = 1
        pixel_diff = {}
        width, height = jpg_after.size
        for y in xrange(height):
            for x in xrange(width):
                if pixel_data_before[x, y] != pixel_data_after[x, y]:
                    pixel_diff[str(pixel_index)] = {}
                    pixel_diff[str(pixel_index)]["before"] = list(pixel_data_before[x, y])
                    pixel_diff[str(pixel_index)]["after"] = list(pixel_data_after[x, y])
                pixel_index += 1
        return pixel_diff
    
    def diff_exif(self, jpg_before, jpg_after):
        """diff jpg file exif data and return the exif diff

        args:
            jpg_before (PIL.Image)
            jpg_after (PIL.Image)

        returns:
            exif_diff (dict)
        """
        exif_data_before = jpg_before._getexif()
        exif_data_after = jpg_after._getexif()
        exif_diff = {}
        if exif_data_before != None and exif_data_after != None:
            keys = set(exif_data_before.keys() + exif_data_after.keys())
            for key in keys:
                exif_diff[key] = {}
                if key in exif_data_before.keys():
                    exif_diff[key]["before"] = exif_data_before[key]
                else:
                    exif_diff[key]["before"] = None
                if key in exif_data_after.keys():
                    exif_diff[key]["after"] = exif_data_after[key]
                else:
                    exif_diff[key]["after"] = None
            return exif_diff
        return None