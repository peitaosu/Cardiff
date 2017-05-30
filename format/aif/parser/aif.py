import aifc
import struct

class AIF():
    def __init__(self):
        pass

    def load_from_file(self, aifc_file):
        """read aifc data from file

        args:
            aifc_file (str)
        """
        self.file_path = aifc_file
        self.file = aifc.open(aifc_file, "r")

    def get_frames_count(self):
        """get aifc frames count
        
        returns:
            self.frames_count (int)
        """
        self.frames_count = self.file.getnframes()
        return self.frames_count
    
    def get_frames(self):
        """get all the frames data

        returns:
            self.frames (bin)
        """
        self.frames = self.file.readframes(self.file.getnframes())
        return self.frames

    def get_nframes(self, number_of_frames=None):
        """get all or number of frames

        args:
            number_of_frames (int)
        
        returns:
            frames (bin)
        """
        if number_of_frames is not None:
            return self.file.readframes(number_of_frames)
        else:
            return self.file.readframes(self.file.getnframes())

    def get_framerate(self):
        """get aifc framerate

        returns:
            self.framerate (int)
        """
        self.framerate = self.file.getframerate()
        return self.framerate

    def get_duration(self):
        """get aifc duration

        returns:
            self.duration (float)
        """
        self.duration = self.get_frames_count() / float(self.get_framerate())
        return self.duration

    def get_channels_count(self):
        """get aifc channels count

        returns:
            self.channels_count (int)
        """
        self.channels_count = self.file.getnchannels()
        return self.channels_count

    def get_sample_width(self):
        """get aifc sample width

        returns:
            self.sample_width (int)
        """
        self.sample_width = self.file.getsampwidth()
        return self.sample_width

    def get_compress_type(self):
        """get aifc compress type

        returns:
            self.compress_type (str)
        """
        self.compress_type = self.file.getcomptype()
        return self.compress_type

    def get_compress_name(self):
        """get aifc compress name

        returns:
            self.compress_name (str)
        """
        self.compress_name = self.file.getcompname()
        return self.compress_name

    def get_params(self):
        """get aifc parameters

        returns:
            self.params (tuple)
        """
        self.params = self.file.getparams()
        return self.params

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