import os, sys
from PIL import Image
from parser.psd import PSD
from parser.psd_diff import PSD_DIFF


def merge(file_before, file_after):
    psd_before = PSD()
    psd_after = PSD()
    psd_before.load_psd_from_file(file_before)
    psd_after.load_psd_from_file(file_after)
    psd_diff = PSD_DIFF()
    psd_diff.diff(psd_before, psd_after)
    for param in psd_diff.header:
        if psd_diff.header[param]["before"] != psd_diff.header[param]["after"]:
            print "Header - {} not the same. Before: {} After: {}".format(param, psd_diff.header[param]["before"], psd_diff.header[param]["after"])
            print "Cannot be merged."
            return -1
    if "AUTO_MERGE" not in os.environ:
        option = raw_input("Choose your merge option: 1-All, 2-Pixel By Pixel: ")
    else:
        option = os.getenv("AUTO_MERGE")
    layer_merged = {}
    for layer_id in psd_diff.layer:
        for param in psd_diff.layer[layer_id]["parameter"]:
            if psd_diff.layer[layer_id]["parameter"][param]["before"] != psd_diff.layer[layer_id]["parameter"][param]["after"]:
                print "Layer {} Parameter - {} not the same. Before: {} After: {}".format(layer_id, param, psd_diff.layer[layer_id]["parameter"][param]["before"], psd_diff.layer[layer_id]["parameter"][param]["after"])
                print "Cannot be merged."
                return -1
        if psd_diff.layer[layer_id]["pixel"] != "Empty Layer." and len(psd_diff.layer[layer_id]["pixel"]) > 0:
            layer_merged[layer_id] = {}
            print "Layer " + layer_id + " changed. Need merge."
            if option == "1":
                if "AUTO_ACCEPT" not in os.environ:
                    accept = raw_input(
                        "Choose your merge option: 1-Accept After, 2-Accept Before: ")
                else:
                    accept = os.getenv("AUTO_ACCEPT")
                for pixel_index in psd_diff.layer[layer_id]["pixel"]:
                    if accept == "1":
                        layer_merged[layer_id][pixel_index] = psd_diff.layer[layer_id]["pixel"][pixel_index]["after"]
                    elif accept == "2":
                        layer_merged[layer_id][pixel_index] = psd_diff.layer[layer_id]["pixel"][pixel_index]["before"]
            elif option == "2":
                for pixel_index in psd_diff.layer[layer_id]["pixel"]:
                    print "Pixel: " + pixel_index
                    print "Before: " + psd_diff.layer[layer_id]["pixel"][pixel_index]["before"]
                    print "After: " + psd_diff.layer[layer_id]["pixel"][pixel_index]["after"]
                    if "AUTO_ACCEPT" not in os.environ:
                        accept = raw_input(
                            "Choose your merge option: 1-Accept After, 2-Accept Before: ")
                    else:
                        accept = os.getenv("AUTO_ACCEPT")
                    if accept == "1":
                        layer_merged[layer_id][pixel_index] = psd_diff.layer[layer_id]["pixel"][pixel_index]["after"]
                    elif accept == "2":
                        layer_merged[layer_id][pixel_index] = psd_diff.layer[layer_id]["pixel"][pixel_index]["before"]
    return layer_merged

def make_merged(file_before, file_after, file_output_name):
    pass