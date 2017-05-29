class AUDIO_DIFF():
    def __init__(self):
        self.attributes = []
        self.description = []

    def diff_spec(self, field, audio_before, audio_after):
        setattr(self, field, [])
        getattr(self, field).append(getattr(audio_before, "get_" + field)())
        getattr(self, field).append(getattr(audio_after, "get_" + field)())
        getattr(self, field).append(str(getattr(self, field)[
            0]) + " <---> " + str(getattr(self, field)[1]))

    def diff_frame(self, audio_before, audio_after):
        pass

    def diff(self, audio_before, audio_after):
        for attr in self.attributes:
            self.diff_spec(attr, audio_before, audio_after)
        self.frame_diff = self.diff_frame(audio_before, audio_after)
        self.frame_diff_count = sum(len(v) for v in self.frame_diff.itervalues())
