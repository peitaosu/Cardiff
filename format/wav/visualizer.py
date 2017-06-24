import matplotlib.pyplot
import numpy
import wave
import time
from parser.wav import WAV
from parser.wav_diff import WAV_DIFF

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

def visualize_file_diff(file_before, file_diff, file_after):
    """visualize the wave diff, open with plot

    args:
        file_before (str)
        file_diff (str)
        file_after (str)
    """
    wav_file = wave.open(file_after, "r")
    signal = wav_file.readframes(-1)
    signal = numpy.fromstring(signal, "Int16")

    wav_before = WAV()
    wav_before.load_from_file(file_before)
    wav_after = WAV()
    wav_after.load_from_file(file_after)
    wav_diff = WAV_DIFF()
    wav_diff.diff(wav_before, wav_after)
    channel_count = len(wav_diff.frame_diff)
    for index in range(len(signal)):
        if str(index / channel_count) in wav_diff.frame_diff[str(index % channel_count)].keys():
            continue
        else:
            signal[index] = 0
    channels = [[] for channel in range(channel_count)]
    for index, datum in enumerate(signal):
        channels[index % len(channels)].append(datum)

    fs = wav_file.getframerate()
    Time = numpy.linspace(0, len(signal) / len(channels) /
                        fs, num=len(signal) / len(channels))

    matplotlib.pyplot.figure(1)
    matplotlib.pyplot.title("Wave Diff")
    for channel in channels:
        matplotlib.pyplot.plot(Time, channel)
    matplotlib.pyplot.show()


def visualize(file_before, file_diff, file_after, file_output_name = None):
    """visualize the wave diff, open with plot window

    args:
        file_before (str)
        file_diff (str)
        file_after (str)
        file_output_name (str)
    """
    if file_output_name == None:
        file_output_name = str(time.time())
    visualize_file_diff(file_before, file_diff, file_after)
    