import sys, json
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
    psd_diff = diff(file_before, file_after)
    diff_content = {}
    for attr in ["header", "layer"]:
        diff_content[attr] = getattr(psd_diff, attr)
    with open(file_output_name + "diff.json", "w") as diff_file:
        json.dump(diff_content, diff_file, indent=4)
