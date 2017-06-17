import sys, json, os
from PIL import Image
from parser.psd import PSD
from parser.psd_diff import PSD_DIFF

def diff(file_before, file_after):
    psd_before = PSD()
    psd_after = PSD()
    psd_before.load_psd_from_file(file_before)
    psd_after.load_psd_from_file(file_after)
    psd_diff = PSD_DIFF()
    psd_diff.diff(psd_before, psd_after)
    return psd_diff

def make_diff(file_before, file_after, file_output_name):
    os.mkdir(file_output_name)
    psd_diff = diff(file_before, file_after)
    diff_content = {}
    for attr in ["header", "layer"]:
        diff_content[attr] = getattr(psd_diff, attr)
    with open(os.path.join(file_output_name, "diff.json"), "w") as diff_file:
        json.dump(diff_content, diff_file, indent=4)
    for layer_id in psd_diff.layer.keys():
        if len(psd_diff.layer_image[layer_id]) > 1:
            output_image = os.path.join(file_output_name, layer_id)
            psd_diff.layer_image[layer_id]["before"].save(output_image + ".before.png")
            psd_diff.layer_image[layer_id]["after"].save(output_image + ".after.png")
            diff_image_before = Image.new("RGBA", psd_diff.layer_image[layer_id]["before"].size)
            diff_image_before_data = diff_image_before.load()
            diff_image_after = Image.new("RGBA", psd_diff.layer_image[layer_id]["after"].size)
            diff_image_after_data = diff_image_after.load()
            width, height = diff_image_before.size
            pixel_index = 1
            for y in xrange(height):
                for x in xrange(width):
                    if str(pixel_index) in diff_content["layer"][layer_id]["pixel"]:
                        diff_image_before_data[x, y] = tuple(diff_content["layer"][layer_id]["pixel"][str(pixel_index)]["before"])
                        diff_image_after_data[x, y] = tuple(diff_content["layer"][layer_id]["pixel"][str(pixel_index)]["after"])
                    else:
                        diff_image_before_data[x, y] = (0, 0, 0, 0)
                        diff_image_after_data[x, y] = (0, 0, 0, 0)
                    pixel_index += 1
            diff_image_before.save(output_image + ".before.diff.png", "PNG")
            diff_image_after.save(output_image + ".after.diff.png", "PNG")
