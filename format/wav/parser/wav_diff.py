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
