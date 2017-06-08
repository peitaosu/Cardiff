from Cardiff import Cardiff
import shutil

def test_cmd_help():
    cardiff.exec_cmd(["help"])

def test_cmd_init():
    cardiff.exec_cmd(["init", "./test"])

def test_cmd_log():
    cardiff.exec_cmd(["help", "log"])
    cardiff.exec_cmd(["log"])

def test_cmd_branch():
    cardiff.exec_cmd(["help", "branch"])
    cardiff.exec_cmd(["branch"])

def test_cmd_clean():
    cardiff.exec_cmd(["help", "clean"])
    cardiff.exec_cmd(["clean"])

def test_rollback():
    shutil.rmtree("./test")

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

    print "[TEST] Command - log"
    test_cmd_log()

    print "[TEST] Command - branch"
    test_cmd_branch()

    print "[TEST] Command - clean"
    test_cmd_clean()

    print "[TEST] Rollback Changes"
    test_rollback()
