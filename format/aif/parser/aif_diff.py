import numpy
from format.audio_diff import AUDIO_DIFF

class AIF_DIFF(AUDIO_DIFF):
    def __init__(self):
        self.attributes = ["frames_count", "framerate", "duration", "channels_count", "sample_width", "compress_type", "compress_name"]
        self.description = ["Numbers of Frames", "Sampling Frequency", "Duration", "Numbers of Channels", "Sample Width", "Compression Type", "Compression Name"]

    def diff_frame(self, aif_before, aif_after):
        """diff aif file frames and return the frame diff

        args:
            aif_before (AIF)
            aif_after (AIF)

        returns:
            frame_diff (dict)
        """
        signal_before = aif_before.get_frames()
        signal_after = aif_after.get_frames()

        signal_before = numpy.fromstring(signal_before, "Int16")
        signal_after = numpy.fromstring(signal_after, "Int16")

        channels_before = [[] for channel in range(aif_before.get_channels_count())]
        for index, datum in enumerate(signal_before):
            channels_before[index % len(channels_before)].append(datum)
        channels_after = [[] for channel in range(aif_after.get_channels_count())]
        for index, datum in enumerate(signal_after):
            channels_after[index % len(channels_after)].append(datum)

        frame_diff = {}
        if len(channels_before) == len(channels_after):
            for channel in range(len(channels_before)):
                frame_diff[str(channel)] = {}
                if len(channels_before[channel]) == len(channels_after[channel]):
                    if channels_before[channel] != channels_after[channel]:
                        for index in range(len(channels_before[0])):
                            if channels_before[channel][index] != channels_after[channel][index]:
                                frame_diff[str(channel)][str(index)] = {}
                                frame_diff[str(channel)][str(index)]["before"] = str(channels_before[channel][index])
                                frame_diff[str(channel)][str(index)]["after"] = str(channels_after[channel][index])
                else:
                    #TODO: add the diff for different length
                    pass
        else:
            #TODO: add the diff for different count of channels
            pass
        return frame_diff
