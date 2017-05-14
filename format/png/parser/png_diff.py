import PIL
from format.image_diff import IMAGE_DIFF

class PNG_DIFF(IMAGE_DIFF):
    def __init__(self):
        self.attributes = ["mode", "size"]
        self.description = ["Color Mode", "Image Size"]

    def diff_pixel(self, png_before, png_after):
        """diff png file pixels and return the pixel diff

        args:
            png_before (PIL.Image)
            png_after (PIL.Image)

        returns:
            pixel_diff (dict)
        """
        pixel_data_before = png_before.convert("RGBA").load()
        pixel_data_after = png_after.convert("RGBA").load()
        pixel_index = 1
        pixel_diff = {}
        width, height = png_after.size
        for y in xrange(height):
            for x in xrange(width):
                if pixel_data_before[x, y] != pixel_data_after[x, y]:
                    pixel_diff[str(pixel_index)] = {}
                    pixel_diff[str(pixel_index)]["before"] = list(pixel_data_before[x, y])
                    pixel_diff[str(pixel_index)]["after"] = list(pixel_data_after[x, y])
                pixel_index += 1
        return pixel_diff
