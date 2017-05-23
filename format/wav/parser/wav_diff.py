import numpy

class WAV_DIFF():
    def __init__(self):
        self.attributes = ["frames_count", "framerate", "duration", "channels_count", "sample_width", "compress_type", "compress_name"]
        self.description = ["Numbers of Frames", "Sampling Frequency", "Duration", "Numbers of Channels", "Sample Width", "Compression Type", "Compression Name"]

    def diff_spec(self, field, wav_before, wav_after):
        setattr(self, field, [])
        getattr(self, field).append(getattr(wav_before, "get_" + field)())
        getattr(self, field).append(getattr(wav_after, "get_" + field)())
        getattr(self, field).append(str(getattr(self, field)[
            0]) + " <---> " + str(getattr(self, field)[1]))

    def diff_frame(self, wav_before, wav_after):
        signal_before = wav_before.get_frames()
        signal_after = wav_after.get_frames()

        signal_before = numpy.fromstring(signal_before, "Int16")
        signal_after = numpy.fromstring(signal_after, "Int16")

        channels_before = [[] for channel in range(wav_before.get_channels_count())]
        for index, datum in enumerate(signal_before):
            channels_before[index % len(channels_before)].append(datum)
        channels_after = [[] for channel in range(wav_after.get_channels_count())]
        for index, datum in enumerate(signal_after):
            channels_after[index % len(channels_after)].append(datum)

        frame_diff = {}
        print len(channels_before[0])
        for channel in range(len(channels_before)):
            frame_diff[channel] = {}
            if channels_before[channel] != channels_after[channel]:
                frame_diff[channel][index] = {}
                for index in range(len(channels_before[0])):
                    if channels_before[channel][index] != channels_after[channel][index]:
                        frame_diff[channel][index]["before"] = channels_before[channel][index]
                        frame_diff[channel][index]["after"] = channels_after[channel][index]
        return frame_diff
