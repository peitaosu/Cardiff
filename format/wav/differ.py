import sys, json
from parser.wav import WAV
from parser.wav_diff import WAV_DIFF

def diff(file_before, file_after):
    wav_before = WAV()
    wav_before.load_from_file(file_before)
    wav_after = WAV()
    wav_after.load_from_file(wav_after)
    wav_diff = WAV_DIFF()
    wav_diff.diff(wav_before, wav_after)
    return wav_diff

def make_diff(file_before, file_after, file_output_name):
    wav_diff = diff(file_before, file_after)
    diff_content = {}
    for attr in wav_diff.attributes:
        diff_content[attr] = {}
        diff_content[attr]["before"] = getattr(wav_diff, attr)[0]
        diff_content[attr]["after"] = getattr(wav_diff, attr)[1]
        if diff_content[attr]["before"] != diff_content[attr]["after"]:
            diff_content[attr]["diff"] = True
    diff_content["frame"] = wav_diff.frame_diff
    with open(file_output_name + "diff.json", "w") as diff_file:
        json.dump(diff_content, diff_file, indent=4)
    return file_output_name + ".diff.json"
