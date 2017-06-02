import wave
import struct
from format.audio import AUDIO

class WAV(AUDIO):
    def __init__(self):
        pass

    def load_from_file(self, wave_file):
        """read wave data from file

        args:
            wave_file (str)
        """
        self.file_path = wave_file
        self.file = wave.open(wave_file, "r")

    def create_wave_file(self, channels_count, sample_width, framerate, frames_count, compress_type, compress_name, data, file_path):
        """creare wave file

        args:
            channels_count (int)
            sample_width (int)
            framerate (int)
            frames_count (int)
            compress_type (str)
            compress_name (str)
            data (bin)
            file_path (str)
        """
        wav_file = wave.open(file_path, 'w')
        wav_file.setparams((channels_count, sample_width, framerate, frames_count, compress_type, compress_name))
        for value in data:
            wav_file.writeframes(struct.pack('h', value))
        wav_file.close()