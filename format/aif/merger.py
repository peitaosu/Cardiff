import os, sys
import numpy
from parser.aif import AIF
from parser.aif_diff import AIF_DIFF

def merge(file_before, file_after):
    """merge aif diff

    args:
        file_before (str)
        file_after (str)

    returns:
        frame_merged (dict)
    """
    aif_before = AIF()
    aif_before.load_from_file(file_before)
    aif_after = AIF()
    aif_after.load_from_file(file_after)
    aif_diff = AIF_DIFF()
    aif_diff.diff(aif_before, aif_after)
    for attr in aif_diff.attributes:
        if getattr(aif_diff, attr)[0] != getattr(aif_diff, attr)[1]:
            print "Parameter - " + attr + " not the same: " + getattr(aif_diff, attr)[2]
            print "Cannot be merged."
            return -1

    frame_merged = {}
    for channel in range(len(aif_diff.frame_diff)):
        if len(aif_diff.frame_diff[str(channel)]) == 0:
            print "Channel " + str(channel) + " nothing to merge."
            continue
        print "Merging channel: " + str(channel + 1)
        frame_merged[str(channel)] = {}
        if "AUTO_MERGE" not in os.environ:
            option = raw_input("Choose your merge option: 1-All, 2-Frame By Frame: ")
        else:
            option = os.getenv("AUTO_MERGE")
        if option == "2":
            for frame_index, frame_info in aif_diff.frame_diff[str(channel)].iteritems():
                frame_merged[str(channel)][frame_index] = {}
                print "Frame: " + frame_index
                print "Before: " + frame_info["before"]
                print "After: " + frame_info["after"]
                if "AUTO_ACCEPT" not in os.environ:
                    accept = raw_input(
                        "Choose your merge option: 1-Accept After, 2-Accept Before: ")
                else:
                    accept = os.getenv("AUTO_ACCEPT")
                if accept == "1":
                    frame_merged[str(channel)][frame_index] = frame_info["after"]
                elif accept == "2":
                    frame_merged[str(channel)][frame_index] = frame_info["before"]
        elif option == "1":
            if "AUTO_ACCEPT" not in os.environ:
                accept = raw_input(
                    "Choose your merge option: 1-Accept After, 2-Accept Before: ")
            else:
                accept = os.getenv("AUTO_ACCEPT")
            if accept == "1":
                for frame_index, frame_info in aif_diff.frame_diff[str(channel)].iteritems():
                    frame_merged[str(channel)][frame_index] = frame_info["after"]
            elif accept == "2":
                for frame_index, frame_info in aif_diff.frame_diff[str(channel)].iteritems():
                    frame_merged[str(channel)][frame_index] = frame_info["before"]
    return frame_merged


def make_merged(file_before, file_after, file_output_name):
    """merge aif diff and save as file

    args:
        file_before (str)
        file_after (str)
        file_output_name (str)
    """
    merged_aif_out = AIF()
    merged_aif_out.load_from_file(file_after)
    merged_aif_out_data = merged_aif_out.get_frames()
    merged_aif_out_data = numpy.fromstring(merged_aif_out_data, "Int16")
    frame_merged = merge(file_before, file_after)
    for channel in range(len(frame_merged)):
        for frame_index, frame_info in frame_merged[str(channel)].iteritems():
            merged_aif_out_data[channel * int(frame_index)] = frame_info
    merged_aif_out.create_aifc_file(merged_aif_out.get_channels_count(), merged_aif_out.get_sample_width(), merged_aif_out.get_framerate(), merged_aif_out.get_frames_count(), merged_aif_out.get_compress_type(), merged_aif_out.get_compress_name(), merged_aif_out_data, file_output_name + ".merged.aif")
    return file_output_name + ".merged.aif"

