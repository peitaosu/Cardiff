from PIL import Image

def create_diff_image(image_mode, image_size, pixel_changes, output_file):
    diff_image_before = Image.new("RGBA", image_size)
    diff_image_after = Image.new("RGBA", image_size)
    width, height = image_size
    pixel_index = 1
    for y in xrange(height):
        for x in xrange(width):
            if str(pixel_index) in pixel_changes:
                if image_mode == "RGB":
                    diff_image_before.load()[x, y] = tuple(pixel_changes[str(pixel_index)]["before"]) + (255,)
                    diff_image_after.load()[x, y] = tuple(pixel_changes[str(pixel_index)]["after"]) + (255,)
                else:
                    diff_image_before.load()[x, y] = tuple(pixel_changes[str(pixel_index)]["before"])
                    diff_image_after.load()[x, y] = tuple(pixel_changes[str(pixel_index)]["after"])
            else:
                diff_image_before.load()[x, y] = diff_image_after.load()[x, y] = (0, 0, 0, 0)
            pixel_index += 1
    diff_image_before.save(output_file + "before.diff.png", "PNG")
    diff_image_after.save(output_file + "after.diff.png", "PNG")
    return [output_file + ".before.diff.png", output_file + ".after.diff.png"]
