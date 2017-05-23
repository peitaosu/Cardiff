import matplotlib.pyplot
import numpy
import wave

def visualize_wave_file(file_path):
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

visualize_wave_file("/Users/tony/Desktop/test.wav")