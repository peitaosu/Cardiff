import wave

class WAV():
    def __init__(self):
        pass

    def load_from_file(self, wave_file):
        self.file_path = wave_file
        self.file = wave.open(wave_file, "r")

    def get_frames_count(self):
        self.frames_count = self.file.getnframes()
        return self.frames_count
    
    def get_frames(self):
        self.frames = self.file.readframes(self.file.getnframes())
        return self.frames

    def get_nframes(self, number_of_frames=None):
        if number_of_frames is not None:
            return self.file.readframes(number_of_frames)
        else:
            return self.file.readframes(self.file.getnframes())

    def get_rate(self):
        self.rate = self.file.getframerate()
        return self.rate

    def get_duration(self):
        self.duration = self.get_frames_count() / float(self.get_rate())
        return self.duration

    def get_channels_count(self):
        self.channels_count = self.file.getnchannels()
        return self.channels_count

    def get_sample_width(self):
        self.sample_width = self.file.getsampwidth()
        return self.sample_width

    def get_framerate(self):
        self.framerate = self.file.getframerate()
        return self.framerate

    def get_comptype(self):
        self.comptype = self.file.getcomptype()
        return self.comptype

    def get_compname(self):
        self.compname = self.file.getcompname()
        return self.compname

    def get_params(self):
        self.params = self.file.getparams()
        return self.params
