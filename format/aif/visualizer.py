import matplotlib.pyplot
import numpy
import aifc
import time
from parser.aif import AIF
from parser.aif_diff import AIF_DIFF

def visualize_aifc_file(file_path):
    """visualize the aifc file, show as plot

    args:
        file_path (str)
    """
    # there is a aifc module issue, need to pass file object, not name
    file_obj = open(file_path, "r")
    aif_file = aifc.open(file_obj)

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
    # there is a aifc module issue, need to pass file object, not name
    file_obj = open(file_path, "r")
    aif_file = aifc.open(file_obj)

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

def visualize_file_diff(file_before, file_diff, file_after):
    """visualize the aifc diff, open with plot

    args:
        file_before (str)
        file_diff (str)
        file_after (str)
    """
    # there is a aifc module issue, need to pass file object, not name
    file_obj = open(file_after, "r")
    aif_file = aifc.open(file_obj)
    signal = aif_file.readframes(-1)
    signal = numpy.fromstring(signal, "Int16")
    aif_before = AIF()
    aif_before.load_from_file(file_before)
    aif_after = AIF()
    aif_after.load_from_file(file_after)
    aif_diff = AIF_DIFF()
    aif_diff.diff(aif_before, aif_after)
    channel_count = len(aif_diff.frame_diff)
    for index in range(len(signal)):
        if str(index / channel_count) in aif_diff.frame_diff[str(index % channel_count)].keys():
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


def visualize(file_before, file_diff, file_after, file_output_name = None):
    """visualize the aifc diff, open with plot window

    args:
        file_before (str)
        file_diff (str)
        file_after (str)
        file_output_name (str)
    """
    if file_output_name == None:
        file_output_name = str(time.time())
    visualize_file_diff(file_before, file_diff, file_after)
    