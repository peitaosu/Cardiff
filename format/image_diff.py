class IMAGE_DIFF():
    def __init__(self):
        self.attributes = []
        self.description = []

    def diff_spec(self, field, image_before, image_after):
        setattr(self, field, [])
        getattr(self, field).append(getattr(image_before, field))
        getattr(self, field).append(getattr(image_after, field))
        getattr(self, field).append(str(getattr(self, field)[
            0]) + " <---> " + str(getattr(self, field)[1]))

    def diff_pixel(self, image_before, image_after):
        pass

    def diff(self, image_before, image_after):
        for attr in self.attributes:
            self.diff_spec(attr, image_before, image_after)
        self.pixel_diff = self.diff_pixel(image_before, image_after)