import sys, json
from parser.aif import AIF
from parser.aif_diff import AIF_DIFF

def diff(file_before, file_after):
    """diff aifc file

    args:
        file_before (str)
        file_after (str)

    returns:
        aif_diff (AIF_DIFF)
    """
    aif_before = AIF()
    aif_before.load_from_file(file_before)
    aif_after = AIF()
    aif_after.load_from_file(file_after)
    aif_diff = AIF_DIFF()
    aif_diff.diff(aif_before, aif_after)
    return aif_diff

def make_diff(file_before, file_after, file_output_name):
    """diff aifc file and save as file

    args:
        file_before (str)
        file_after (str)
        file_output_name (str)

    returns:
        saved_file (str)
    """
    aif_diff = diff(file_before, file_after)
    diff_content = {}
    for attr in aif_diff.attributes:
        diff_content[attr] = {}
        diff_content[attr]["before"] = getattr(aif_diff, attr)[0]
        diff_content[attr]["after"] = getattr(aif_diff, attr)[1]
        if diff_content[attr]["before"] != diff_content[attr]["after"]:
            diff_content[attr]["diff"] = True
    diff_content["frame"] = aif_diff.frame_diff
    with open(file_output_name + "diff.json", "w") as diff_file:
        json.dump(diff_content, diff_file, indent=4)
    return file_output_name + ".diff.json"
