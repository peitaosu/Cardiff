import PIL

class PNG_DIFF():
    def __init__(self):
        self.attributes = ["mode", "size"]
        self.description = ["Color Mode", "Image Size"]

    def diff_spec(self, field, png_before, png_after):
        """diff png file parameters and set the attributes

        args:
            field (str)
            png_before (PIL.Image)
            png_after (PIL.Image)
        """
        setattr(self, field, [])
        getattr(self, field).append(getattr(png_before, field))
        getattr(self, field).append(getattr(png_after, field))
        getattr(self, field).append(str(getattr(self, field)[
            0]) + " <---> " + str(getattr(self, field)[1]))

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

    def diff(self, png_before, png_after):
        """diff png file parameters and pixels

        args:
            png_before (PIL.Image)
            png_after (PIL.Image)
        """
        for attr in self.attributes:
            self.diff_spec(attr, png_before, png_after)
        self.pixel_diff = self.diff_pixel(png_before, png_after)