import sys
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
            print "Parameter - " + attr + " not the same: " + getattr(wav_diff, attr)[2]
            print "Cannot be merged."
            return -1

    frame_merged = {}
    for channel in range(len(wav_diff.frame_diff)):
        print "Merging channel: " + str(channel + 1)
        frame_merged[channel] = {}
        option = raw_input("Choose your merge option: 1-All, 2-Frame By Frame: ")
        if option == "2":
            for frame_index, frame_info in wav_diff.frame_diff[channel].iteritems():
                frame_merged[channel][frame_index] = {}
                print "Frame: " + str(frame_index)
                print "Before: " + ", ".join([str(p) for p in frame_info["before"]])
                print "After: " + ", ".join([str(p) for p in frame_info["after"]])
                accept = raw_input(
                    "Choose your merge option: 1-Accept After, 2-Accept Before: ")
                if accept == "1":
                    frame_merged[channel][frame_index] = frame_info["after"]
                elif accept == "2":
                    frame_merged[channel][frame_index] = frame_info["before"]
        elif option == "1":
            accept = raw_input(
                "Choose your merge option: 1-Accept After, 2-Accept Before: ")
            if accept == "1":
                for frame_index, frame_info in wav_diff.frame_diff.iteritems():
                    frame_merged[channel][frame_index] = frame_info["after"]
            elif accept == "2":
                for frame_index, frame_info in wav_diff.frame_diff.iteritems():
                    frame_merged[channel][frame_index] = frame_info["before"]
    return frame_merged


def make_merged(file_before, file_after, file_output_name):
    """merge wav diff and save as file

    args:
        file_before (str)
        file_after (str)
        file_output_name (str)
    """
    merged_wav_out = WAV()
    merged_wav_out.load_from_file(file_after)
    merged_wav_out_data = merged_wav_out.get_frames()
    merged_wav_out_data = numpy.fromstring(merged_wav_out_data, "Int16")
    frame_merged = merge(file_before, file_after)
    for channel in range(len(frame_merged)):
        for frame_index, frame_info in frame_merged[channel]:
            merged_wav_out_data[channel * frame_index] = frame_info
    merged_wav_out_data = merged_wav_out_data.tostring()
    merged_wav_out.create_wave_file(merged_wav_out.channels_count, merged_wav_out.sample_width, merged_wav_out.framerate, merged_wav_out.frames_count, merged_wav_out.compress_type, merged_wav_out.compress_name, merged_wav_out.amp, merged_wav_out_data, file_output_name + ".merged.wav")
    return file_output_name + ".merged.wav"

