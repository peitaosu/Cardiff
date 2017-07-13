import os, sys
import numpy
from parser.wav import WAV
from parser.wav_diff import WAV_DIFF

def merge(file_before, file_after):
    """merge wav diff

    args:
        file_before (str)
        file_after (str)

    returns:
        frame_merged (dict)
    """
    wav_before = WAV()
    wav_before.load_from_file(file_before)
    wav_after = WAV()
    wav_after.load_from_file(file_after)
    wav_diff = WAV_DIFF()
    wav_diff.diff(wav_before, wav_after)
    for attr in wav_diff.attributes:
        if getattr(wav_diff, attr)[0] != getattr(wav_diff, attr)[1]:
            print "Parameter - {} not the same: {}".format(attr, getattr(wav_diff, attr)[2])

    frame_merged = {}
    for channel in range(len(wav_diff.frame_diff)):
        if len(wav_diff.frame_diff[str(channel)]) == 0:
            print "Channel {} nothing to merge.".format(str(channel))
            continue
        print "Merging channel: {}".format(str(channel + 1))
        frame_merged[str(channel)] = {}
        if "AUTO_MERGE" not in os.environ:
            option = raw_input("Choose your merge option: 1-All, 2-Frame By Frame: ")
        else:
            option = os.getenv("AUTO_MERGE")
        if option == "2":
            for frame_index, frame_info in wav_diff.frame_diff[str(channel)].iteritems():
                frame_merged[str(channel)][frame_index] = {}
                print "Frame: {}".format(frame_index)
                print "Before: {}".format(frame_info["before"])
                print "After: {}".format(frame_info["after"])
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
                for frame_index, frame_info in wav_diff.frame_diff[str(channel)].iteritems():
                    frame_merged[str(channel)][frame_index] = frame_info["after"]
            elif accept == "2":
                for frame_index, frame_info in wav_diff.frame_diff[str(channel)].iteritems():
                    frame_merged[str(channel)][frame_index] = frame_info["before"]
    return frame_merged


def make_merged(file_before, file_after, file_output_name):
    """merge wav diff and save as file

    args:
        file_before (str)
        file_after (str)
        file_output_name (str)

    returns:
        merged_file (str)
    """
    merged_wav_out = WAV()
    merged_wav_out.load_from_file(file_after)
    merged_wav_out_data = merged_wav_out.get_frames()
    merged_wav_out_data = numpy.fromstring(merged_wav_out_data, "Int16")
    frame_merged = merge(file_before, file_after)
    for channel in range(len(frame_merged)):
        for frame_index, frame_info in frame_merged[str(channel)].iteritems():
            merged_wav_out_data[channel * int(frame_index)] = frame_info
    merged_wav_out.create_wave_file(merged_wav_out.get_channels_count(), merged_wav_out.get_sample_width(), merged_wav_out.get_framerate(), merged_wav_out.get_frames_count(), merged_wav_out.get_compress_type(), merged_wav_out.get_compress_name(), merged_wav_out_data, file_output_name + ".merged.wav")
    return file_output_name + ".merged.wav"

