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
    for layer_id in psd_diff.layer:
        for param in psd_diff.layer[layer_id]["parameter"]:
            if psd_diff.layer[layer_id]["parameter"][param]["before"] != psd_diff.layer[layer_id]["parameter"][param]["after"]:
                print "Layer {} Parameter - {} not the same. Before: {} After: {}".format(layer_id, param, psd_diff.layer[layer_id]["parameter"][param]["before"], psd_diff.layer[layer_id]["parameter"][param]["after"])
                print "Cannot be merged."
                return -1
    pass

def make_merged(file_before, file_after, file_output_name):
    pass