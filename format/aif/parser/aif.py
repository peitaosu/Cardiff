import aifc
import struct
from format.audio import AUDIO

class AIF(AUDIO):
    def __init__(self):
        pass

    def load_from_file(self, aifc_file):
        """read aifc data from file

        args:
            aifc_file (str)
        """
        self.file_path = aifc_file
        self.file = aifc.open(aifc_file, "r")

    def get_markers(self):
        """get aifc markers

        returns:
            self.markers (tuple)
        """
        self.markers = self.file.getmarkers()
        return self.markers

    def create_aifc_file(self, channels_count, sample_width, framerate, frames_count, compress_type, compress_name, data, file_path):
        """creare aifc file

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
        aif_file = aifc.open(file_path, 'w')
        aif_file.setnframes(frames_count)
        aif_file.setparams((channels_count, sample_width, framerate, compress_type, compress_name))
        for value in data:
            aif_file.writeframes(struct.pack('h', value))
        aif_file.close()