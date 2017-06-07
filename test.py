from Cardiff import Cardiff

def test_cmd_help():
    cardiff.exec_cmd(["help"])
    cardiff.exec_cmd(["help", "log"])

def test_cmd_log():
    cardiff.exec_cmd(["log"])

def test_cmd_branch():
    cardiff.exec_cmd(["branch"])

if __name__ == "__main__":
    print "[TEST] New a Cardiff object..."
    cardiff = Cardiff()
    
    print "[TEST] Load settings.json from Cardiff root path..."
    settings_path = "./settings.json"
    cardiff.load_settings(settings_path)

    print "[TEST] Test help command..."
    test_cmd_help()

    print "[TEST] Test log command..."
    test_cmd_log()

    print "[TEST] Test branch command..."
    test_cmd_branch()
