import os, sys, json
from init import init_vcs

cardiff_path = os.path.dirname(os.path.realpath(__file__))

class Cardiff():
    def __init__(self):
        self.settings = {}
        self.settings_path = os.path.join(cardiff_path, "settings.json")
        self.vcs = None
        self.commands = {
            "init": self.cmd_init,
            "diff": self.cmd_diff,
            "merge": self.cmd_merge,
            "commit": self.cmd_commit,
            "checkout": self.cmd_checkout,
            "log": self.cmd_log
        }

    def load_settings(self, settings_path = None):
        if settings_path is not None:
            self.settings_path = settings_path
        with open(self.settings_path) as settings_file:
            self.settings = json.load(settings_file)

    def setup_vcs(self):
        self.vcs = init_vcs(self.settings["vcs"])

    def cmd_init(self, init_path):
        if len(init_path) > 0:
            init_path = init_path[0]
            if os.path.isdir(init_path):
                print init_path + " is exist."
            else:
                os.mkdir(init_path)
                user_name = self.settings["user.name"]
                user_email = self.settings["user.email"]
                self.vcs.init(init_path, user_name, user_email)
                self.settings["repo"] = init_path
                with open(self.settings_path, "w") as settings_file:
                    json.dump(self.settings, settings_file, indent=4)
                print "[Initialized Repository]:"
                print init_path
        else:
            print "You need to provide a path for repository initialing."

    def cmd_diff(self, file_ver):
        file_path = file_ver[0]
        if len(file_ver) > 2:
            ver_1 = file_ver[1]
            ver_2 = file_ver[2]
        else:
            ver_1 = "HEAD"
            ver_2 = file_ver[1]
        # TODO: compare file between versions, create diff
        print "diff " + file_path + " " + ver_1 + " " + ver_2

    def cmd_merge(self, file_ver):
        file_path = file_ver[0]
        if len(file_ver) > 2:
            ver_1 = file_ver[1]
            ver_2 = file_ver[2]
        else:
            ver_1 = "HEAD"
            ver_2 = file_ver[1]
        # TODO: merge file between versions and save as new version
        print "merge " + file_path + " " + ver_1 + " " + ver_2

    def cmd_commit(self, commit):
        file_path = commit[0]
        commit_message = commit[1]
        self.vcs.set_repo(self.settings["repo"])
        self.vcs.commit(file_path, commit_message)
        print "[New Commit]:"
        print file_path + " - " + commit_message

    def cmd_checkout(self, file_ver):
        file_path = file_ver[0]
        ver = file_ver[1]
        # TODO: rollback file to specified version
        print "checkout " + file_path + " from " + ver

    def cmd_log(self, log_filter):
        self.vcs.set_repo(self.settings["repo"])
        logs = self.vcs.log()
        print "[Commit History]:"
        if len(log_filter) > 0:
            for log in logs:
                if log_filter[0] in log[1] or log_filter[0] in log[4]:
                    print log[1] + " - " + log[4]
        else:
            for log in logs:
                print log[1] + " - " + log[4]

if __name__ == "__main__":
    cardiff = Cardiff()
    settings_path = os.path.join(cardiff_path, "settings.json")
    cardiff.load_settings(settings_path)
    cardiff.setup_vcs()
    cardiff.commands[sys.argv[1]](sys.argv[2:])
