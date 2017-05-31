import matplotlib.pyplot
import numpy
import aifc
import time

def visualize_aifc_file(file_path):
    """visualize the aifc file, show as plot

    args:
        file_path (str)
    """
    aif_file = aifc.open(file_path, "r")

    signal = aif_file.readframes(-1)
    signal = numpy.fromstring(signal, "Int16")

    channels = [[] for channel in range(aif_file.getnchannels())]
    for index, datum in enumerate(signal):
        channels[index % len(channels)].append(datum)

    fs = aif_file.getframerate()
    Time = numpy.linspace(0, len(signal) / len(channels) /
                        fs, num=len(signal) / len(channels))

    matplotlib.pyplot.figure(1)
    matplotlib.pyplot.title(file_path)
    for channel in channels:
        matplotlib.pyplot.plot(Time, channel)
    matplotlib.pyplot.show()

def visualize_as_png(file_path, file_output_name = None):
    """visualize the aifc file, save as plot png file

    args:
        file_path (str)
        file_output_name (str)
    
    returns:
        png_file (str)
    """
    aif_file = aifc.open(file_path, "r")

    signal = aif_file.readframes(-1)
    signal = numpy.fromstring(signal, "Int16")

    channels = [[] for channel in range(aif_file.getnchannels())]
    for index, datum in enumerate(signal):
        channels[index % len(channels)].append(datum)

    fs = aif_file.getframerate()
    Time = numpy.linspace(0, len(signal) / len(channels) /
                        fs, num=len(signal) / len(channels))

    matplotlib.pyplot.figure(1)
    matplotlib.pyplot.title(file_path)
    for channel in channels:
        matplotlib.pyplot.plot(Time, channel)

    matplotlib.pyplot.savefig(file_output_name + ".png")
    return file_output_name + ".png"

def visualize_file_diff(file_diff, file_base):
    """visualize the aifc diff, open with plot

    args:
        file_diff (str)
        file_base (str)
    """
    aif_file = aifc.open(file_base, "r")
    signal = aif_file.readframes(-1)
    signal = numpy.fromstring(signal, "Int16")
    channel_count = len(file_diff.frame_diff)
    for index in range(len(signal)):
        if str(index / channel_count) in file_diff.frame_diff[str(index % channel_count)].keys():
            continue
        else:
            signal[index] = 0
    channels = [[] for channel in range(channel_count)]
    for index, datum in enumerate(signal):
        channels[index % len(channels)].append(datum)

    fs = aif_file.getframerate()
    Time = numpy.linspace(0, len(signal) / len(channels) /
                        fs, num=len(signal) / len(channels))

    matplotlib.pyplot.figure(1)
    matplotlib.pyplot.title("Aifc Diff")
    for channel in channels:
        matplotlib.pyplot.plot(Time, channel)
    matplotlib.pyplot.show()


def visualize(file_diff, file_after, file_output_name = None):
    """visualize the aifc diff, open with plot window

    args:
        file_diff (AIF_DIFF)
        file_after (str)
        file_output_name (str)
    """
    if file_output_name == None:
        file_output_name = str(time.time())
    visualize_file_diff(file_diff, file_after)
    