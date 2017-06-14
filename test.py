from Cardiff import Cardiff
import shutil
import importlib
from PIL import Image
import json
import pprint
import time

pp = pprint.PrettyPrinter(indent=4)

def test_load_settings():
    print "[TEST] Load settings.json from Cardiff root path..."
    settings_path = "./settings.json"
    with open(settings_path) as settings_file:
        settings = json.load(settings_file)
    settings["user.name"] = "test"
    settings["user.email"] = "test@@cardiff"

    print "Settings Detail:"
    pp.pprint(settings)
    with open(settings_path, "w") as settings_file:
        json.dump(settings, settings_file, indent=4)
    cardiff.load_settings(settings_path)

def test_cmd_help():
    print "[TEST] Command - help"
    cardiff.exec_cmd(["help"])

def test_cmd_init():
    print "[TEST] Command - init"
    cardiff.exec_cmd(["init", "./test"])

def test_cmd_commit():
    print "[TEST] Command - commit"
    print "Create Dummy File: file.bmp"
    create_dummy_bmp()
    cardiff.exec_cmd(["commit", "file.bmp", "commit msg " + str(time.time())])
    cardiff.exec_cmd(["log"])

def test_cmd_diff():
    print "[TEST] Command - diff"
    cardiff.exec_cmd(["diff", "file.bmp", "1", "2"])

def test_cmd_merge():
    print "[TEST] Command - merge"
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
    create_dummy_bmp()
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

def create_dummy_bmp():
    img = Image.new('RGB', (256, 256))
    pixels = img.load()
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            pixels[x, y] = (0, 0, 0)
    img.save("./test/file.bmp")

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

    test_cmd_log()

    test_cmd_clean()

    test_rollback()
