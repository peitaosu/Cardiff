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
