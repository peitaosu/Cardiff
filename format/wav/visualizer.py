import matplotlib.pyplot
import numpy
import wave

def visualize_wave_file(file_path):
    """visualize the wave file, show as plot

    args:
        file_path (str)
    """
    wav_file = wave.open(file_path, "r")

    signal = wav_file.readframes(-1)
    signal = numpy.fromstring(signal, "Int16")

    channels = [[] for channel in range(wav_file.getnchannels())]
    for index, datum in enumerate(signal):
        channels[index % len(channels)].append(datum)

    fs = wav_file.getframerate()
    Time = numpy.linspace(0, len(signal) / len(channels) /
                        fs, num=len(signal) / len(channels))

    matplotlib.pyplot.figure(1)
    matplotlib.pyplot.title(file_path)
    for channel in channels:
        matplotlib.pyplot.plot(Time, channel)
    matplotlib.pyplot.show()

def visualize_as_png(file_path, file_output_name = None):
    """visualize the wave file, save as plot png file

    args:
        file_path (str)
        file_output_name (str)
    
    returns:
        png_file (str)
    """
    wav_file = wave.open(file_path, "r")

    signal = wav_file.readframes(-1)
    signal = numpy.fromstring(signal, "Int16")

    channels = [[] for channel in range(wav_file.getnchannels())]
    for index, datum in enumerate(signal):
        channels[index % len(channels)].append(datum)

    fs = wav_file.getframerate()
    Time = numpy.linspace(0, len(signal) / len(channels) /
                        fs, num=len(signal) / len(channels))

    matplotlib.pyplot.figure(1)
    matplotlib.pyplot.title(file_path)
    for channel in channels:
        matplotlib.pyplot.plot(Time, channel)

    matplotlib.pyplot.savefig(file_output_name + ".png")
    return file_output_name + ".png"
