from Cardiff import Cardiff
import shutil
import importlib
from PIL import Image
import json
import pprint
import time
import os
from util import *

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
    os.environ["CARDIFF_VERBOSE_MODE"] = "1"

def test_cmd_help():
    print "[TEST] Command - help"
    cardiff.exec_cmd(["help"])

def test_cmd_info():
    print "[TEST] Command - info"
    cardiff.exec_cmd(["info"])
    cardiff.exec_cmd(["info", "version"])
    cardiff.exec_cmd(["info", "contributor"])

def test_cmd_init():
    print "[TEST] Command - init"
    cardiff.exec_cmd(["init", "test"])
    print_settings()
    cardiff.save_settings()

def test_cmd_commit():
    print "[TEST] Command - commit"
    print "Create Dummy Files"
    for image_format in ["bmp", "jpg", "png", "gif"]:
        time.sleep(1)
        create_dummy_image(image_format)
        cardiff.exec_cmd(["commit", "file." + image_format, "commit msg " + str(time.time())])
        time.sleep(1)
        cardiff.exec_cmd(["commit", "file." + image_format, "commit msg " + str(time.time())])
    for audio_format in ["wav", "aif"]:
        time.sleep(1)
        create_dummy_audio(audio_format)
        cardiff.exec_cmd(["commit", "file." + audio_format, "commit msg " + str(time.time())])
        time.sleep(1)
        cardiff.exec_cmd(["commit", "file." + audio_format, "commit msg " + str(time.time())])
    cardiff.exec_cmd(["log"])

def test_cmd_diff():
    print "[TEST] Command - diff"
    os.environ["CARDIFF_SILENT_MODE"] = "1"
    result = cardiff.exec_cmd(["diff", "file.bmp", "2", "3"])
    print_file_content(result[2])
    result = cardiff.exec_cmd(["diff", "file.jpg", "4", "5"])
    print_file_content(result[2])
    result = cardiff.exec_cmd(["diff", "file.png", "6", "7"])
    print_file_content(result[2])
    result = cardiff.exec_cmd(["diff", "file.gif", "8", "9"])
    print_file_content(result[2])
    cardiff.exec_cmd(["diff", "file.wav", "10", "11"])
    cardiff.exec_cmd(["diff", "file.aif", "12", "13"])

def test_cmd_merge():
    print "[TEST] Command - merge"
    os.environ["AUTO_MERGE"] = "1"
    os.environ["AUTO_ACCEPT"] = "1"
    cardiff.exec_cmd(["merge", "file.bmp", "2", "3"])
    cardiff.exec_cmd(["merge", "file.jpg", "4", "5"])
    cardiff.exec_cmd(["merge", "file.png", "6", "7"])
    cardiff.exec_cmd(["merge", "file.gif", "8", "9"])
    cardiff.exec_cmd(["merge", "file.wav", "10", "11"])
    cardiff.exec_cmd(["merge", "file.aif", "12", "13"])

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

def test_cmd_repo():
    print "[TEST] Command - repo"
    cardiff.exec_cmd(["help", "repo"])
    cardiff.exec_cmd(["repo"])
    cardiff.exec_cmd(["repo", "test"])

def test_cmd_clean():
    print "[TEST] Command - clean"
    cardiff.exec_cmd(["help", "clean"])
    cardiff.exec_cmd(["clean"])

def test_rollback():
    print "Rollback Changes"
    shutil.rmtree("./repos/test")
    shutil.rmtree("./vcs/vcs_db/git/test")

def create_dummy_image(format):
    if format in ["bmp", "jpg"]:
        img = Image.new("RGB", (256, 256))
        for x in range(256):
            for y in range(256):
                img.load()[x, y] = (x, y, 180)
        img.save("./repos/test/file." + format)
    elif format in ["png", "gif"]:
        img = Image.new("RGBA", (256, 256))
        for x in range(256):
            for y in range(256):
                img.load()[x, y] = (x, y, 180, 180)
        img.save("./repos/test/file." + format)


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
        audio_file = aifc.open("./repos/test/file." + format, 'w')
    elif format == "wav":
        audio_file = wave.open("./repos/test/file." + format, 'w')
    audio_file.setparams(
        (nchannels, sampwidth, framerate, nframes, comptype, compname))
    for values in data:
        for v in values:
            audio_file.writeframes(struct.pack('h', int(v * amp / 2)))

if __name__ == "__main__":

    print "[TEST] Testing for Cardiff..."
    cardiff = Cardiff()

    test_load_settings()

    test_cmd_help()

    test_cmd_info()

    test_cmd_init()

    test_cmd_repo()

    test_cmd_branch()

    test_cmd_commit()

    test_cmd_diff()

    test_cmd_merge()

    test_cmd_log()

    test_cmd_clean()

    test_rollback()
