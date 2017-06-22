from Cardiff import Cardiff
import shutil
import importlib
from PIL import Image
import json
import pprint
import time
import os

pp = pprint.PrettyPrinter(indent=4)
settings_path = "./settings.json"

def print_settings():
    print "Current Settings"
    with open(settings_path) as settings_file:
        current_settings = json.load(settings_file)
    pp.pprint(current_settings)

def test_load_settings():
    print "[TEST] Load settings.json from Cardiff root path..."

    with open(settings_path) as settings_file:
        settings = json.load(settings_file)
    settings["user.name"] = "test"
    settings["user.email"] = "test@@cardiff"
    with open(settings_path, "w") as settings_file:
        json.dump(settings, settings_file, indent=4)

    print_settings()
    cardiff.load_settings(settings_path)

def test_cmd_help():
    print "[TEST] Command - help"
    cardiff.exec_cmd(["help"])

def test_cmd_init():
    print "[TEST] Command - init"
    cardiff.exec_cmd(["init", "./test"])
    print_settings()

def test_cmd_commit():
    print "[TEST] Command - commit"
    print "Create Dummy File: file.bmp"
    create_dummy_image("bmp")
    cardiff.exec_cmd(["commit", "file.bmp", "commit msg " + str(time.time())])
    cardiff.exec_cmd(["log"])
    cardiff.exec_cmd(["commit", "file.bmp", "commit msg " + str(time.time())])
    cardiff.exec_cmd(["log"])

def test_cmd_diff():
    print "[TEST] Command - diff"
    cardiff.exec_cmd(["diff", "file.bmp", "1", "2"])

def test_cmd_merge():
    print "[TEST] Command - merge"
    os.environ["AUTO_MERGE"] = "1"
    os.environ["AUTO_ACCEPT"] = "1"
    cardiff.exec_cmd(["merge", "file.bmp", "1", "2"])

def test_cmd_log():
    print "[TEST] Command - log"
    cardiff.exec_cmd(["help", "log"])
    cardiff.exec_cmd(["log"])

def test_cmd_branch():
    print "[TEST] Command - branch"
    cardiff.exec_cmd(["help", "branch"])
    cardiff.exec_cmd(["branch"])
    print "Commit to branch: file.bmp"
    create_dummy_image("bmp")
    cardiff.exec_cmd(["commit", "file.bmp", "commit msg " + str(time.time())])
    cardiff.exec_cmd(["log"])
    print "Create New Branch: new_branch"
    cardiff.exec_cmd(["branch", "new_branch"])
    cardiff.exec_cmd(["branch"])

def test_cmd_clean():
    print "[TEST] Command - clean"
    cardiff.exec_cmd(["help", "clean"])
    cardiff.exec_cmd(["clean"])

def test_rollback():
    print "Rollback Changes"
    shutil.rmtree("./test")

def create_dummy_image(format):
    if format in ["bmp", "jpg"]:
        img = Image.new("RGB", (256, 256))
        for x in range(256):
            for y in range(256):
                img.load()[x, y] = (x, y, 180)
        img.save("./test/file." + format)
    elif format in ["png", "gif"]:
        img = Image.new("RGBA", (256, 256))
        for x in range(256):
            for y in range(256):
                img.load()[x, y] = (x, y, 180, 180)
        img.save("./test/file." + format)


def create_dummy_audio(format):
    import aifc
    import wave
    import math
    import struct
    freq = 440.0
    data_size = 40000
    frate = 1000.0
    amp = 64000.0
    nchannels = 2
    sampwidth = 2
    framerate = int(frate)
    nframes = data_size
    comptype = "NONE"
    compname = "not compressed"
    data = [(math.sin(2 * math.pi * freq * (x / frate)),
             math.cos(2 * math.pi * freq * (x / frate))) for x in range(data_size)]

    if format == "aif":
        audio_file = aifc.open("./test/file." + format, 'w')
    elif format == "wav":
        audio_file = wave.open("./test/file." + format, 'w')
    audio_file.setparams(
        (nchannels, sampwidth, framerate, nframes, comptype, compname))
    for values in data:
        for v in values:
            audio_file.writeframes(struct.pack('h', int(v * amp / 2)))

def create_dummy_file(ext, content):
    file_module = importlib.import_module("format." + ext + ".parser." + ext)
    file_class = getattr(file_module, ext.upper())
    #TODO: create file with method of class

if __name__ == "__main__":

    print "[TEST] Testing for Cardiff..."
    cardiff = Cardiff()

    test_load_settings()

    test_cmd_help()

    test_cmd_init()

    test_cmd_branch()

    test_cmd_commit()

    test_cmd_merge()

    test_cmd_log()

    test_cmd_clean()

    test_rollback()
