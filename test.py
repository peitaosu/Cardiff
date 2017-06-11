from Cardiff import Cardiff
import shutil
import importlib
from PIL import Image

def test_cmd_help():
    cardiff.exec_cmd(["help"])

def test_cmd_init():
    cardiff.exec_cmd(["init", "./test"])

def test_cmd_commit():
    cardiff.exec_cmd(["commit", "file.bmp", "commit no.1"])

def test_cmd_diff():
    cardiff.exec_cmd(["diff", "file.bmp", "1", "2"])

def test_cmd_merge():
    cardiff.exec_cmd(["merge", "file.bmp", "1", "2"])

def test_cmd_log():
    cardiff.exec_cmd(["help", "log"])
    cardiff.exec_cmd(["log"])

def test_cmd_branch():
    cardiff.exec_cmd(["help", "branch"])
    cardiff.exec_cmd(["branch"])

def test_switch_branch():
    cardiff.exec_cmd(["branch", "new_branch"])

def test_cmd_clean():
    cardiff.exec_cmd(["help", "clean"])
    cardiff.exec_cmd(["clean"])

def test_rollback():
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
    print "[TEST] New a Cardiff object..."
    cardiff = Cardiff()

    print "[TEST] Load settings.json from Cardiff root path..."
    settings_path = "./settings.json"
    cardiff.load_settings(settings_path)

    print "[TEST] Command - help"
    test_cmd_help()

    print "[TEST] Command - init"
    test_cmd_init()

    print "[TEST] Command - branch"
    test_cmd_branch()

    print "[TEST] Create Dummy File"
    create_dummy_file("bmp", None)
    create_dummy_bmp()

    print "[TEST] Command - commit"
    test_cmd_commit()

    print "[TEST] Command - diff"
    test_cmd_commit()
    test_cmd_diff()

    print "[TEST] Switch Branch"
    test_switch_branch()

    print "[TEST] Command - merge"
    test_cmd_commit()
    test_cmd_commit()
    test_cmd_merge()

    print "[TEST] Command - log"
    test_cmd_log()

    print "[TEST] Command - clean"
    test_cmd_clean()

    print "[TEST] Rollback Changes"
    test_rollback()
