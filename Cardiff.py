import os, sys, json, time
from common import *
from init import *
from diff import diff
from visualize import visualize_diff
from parameterize import parameterize_diff
from merge import merge_file

cardiff_path = os.path.dirname(os.path.realpath(__file__))

class Cardiff():
    def __init__(self):
        self.settings = {}
        self.vcs = None
        self.commands = {
            "init": self.cmd_init,
            "diff": self.cmd_diff,
            "merge": self.cmd_merge,
            "commit": self.cmd_commit,
            "checkout": self.cmd_checkout,
            "log": self.cmd_log,
            "branch": self.cmd_branch,
            "clean": self.cmd_clean,
            "help": self.cmd_help
        }

    def load_settings(self, settings_path = None):
        if settings_path == None:
            self.settings_path = os.path.join(cardiff_path, "settings.json")
        else:
            self.settings_path = settings_path
        with open(self.settings_path) as settings_file:
            self.settings = json.load(settings_file)
        for key in ["user.name", "user.email"]:
            if self.settings[key].startswith("<") and self.settings[key].endswith(">"):
                print "Please set the " + key + " in settings file."
                sys.exit(-1)
        if self.settings["repo"].startswith("<") and self.settings["repo"].endswith(">"):
            print "You need to init a repo first time."
        self.temp = os.path.join(cardiff_path, self.settings["temp"])
        self.vcs_db_path = os.path.join(cardiff_path, "vcs", "vcs_db", self.settings["vcs"])
        make_path_exist(self.temp)
        make_path_exist(self.vcs_db_path)
        self.vcs = init_vcs(self.settings["vcs"])

    def setup_vcs(self):
        if self.settings["repo"] != "":
            if self.settings["repo"].startswith("<") and self.settings["repo"].endswith(">"):
                print "You need to init a repo first time."
                sys.exit(-1)
            self.vcs.set_repo(self.settings["repo"])
            self.vcs_branches = self.vcs.get_branches()
            self.vcs_current_branch = self.vcs_branches["current"]
            self.vcs_db_log = os.path.join(self.vcs_db_path, os.path.basename(self.settings["repo"]), "log.json")
            with open(self.vcs_db_log) as log_file:
                self.vcs_logs = json.load(log_file)

    def cmd_init(self, init_path):
        if len(init_path) > 0:
            init_path = init_path[0]
            if os.path.isdir(init_path):
                print init_path + " is exist."
            else:
                make_path_exist(init_path)
                make_path_exist(os.path.join(self.vcs_db_path, os.path.basename(init_path)))
                init_vcs_log(self.vcs_db_path, os.path.basename(init_path))
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
        self.setup_vcs()
        file_path = file_ver[0]
        if len(file_ver) > 2:
            ver_1 = self.vcs_logs[self.vcs_current_branch]["#" + file_ver[1]]["hash"]
            ver_2 = self.vcs_logs[self.vcs_current_branch]["#" + file_ver[2]]["hash"]
        else:
            ver_1 = self.vcs_logs[self.vcs_current_branch][self.vcs_logs[self.vcs_current_branch]["HEAD"]]["hash"]
            ver_2 = self.vcs_logs[self.vcs_current_branch]["#" + file_ver[1]]["hash"]
        file_ext = os.path.splitext(file_path)[1]
        new_file_1 = str(time.time()) + file_ext
        self.vcs.checkout_as_new(file_path, ver_1, os.path.join(self.temp, new_file_1))
        new_file_2 = str(time.time()) + file_ext
        self.vcs.checkout_as_new(file_path, ver_2, os.path.join(self.temp, new_file_2))
        diff_result = diff(os.path.join(self.temp, new_file_1), os.path.join(self.temp, new_file_2))
        print "diff " + file_path + " " + ver_1 + " " + ver_2
        parameterize_diff(diff_result, file_path.split(".")[-1])
        visualize_diff(diff_result, os.path.join(self.temp, new_file_2), file_path.split(".")[-1], os.path.join(self.temp, file_path.split(".")[0] + "_" + ver_1[:6] + "_" + ver_2[:6]))

    def cmd_merge(self, file_ver):
        self.setup_vcs()
        file_path = file_ver[0]
        if len(file_ver) > 2:
            ver_1 = self.vcs_logs[self.vcs_current_branch]["#" + file_ver[1]]["hash"]
            ver_2 = self.vcs_logs[self.vcs_current_branch]["#" + file_ver[2]]["hash"]
        else:
            ver_1 = self.vcs_logs[self.vcs_current_branch][self.vcs_logs[self.vcs_current_branch]["HEAD"]]["hash"]
            ver_2 = self.vcs_logs[self.vcs_current_branch]["#" + file_ver[1]]["hash"]
        file_ext = os.path.splitext(file_path)[1]
        new_file_1 = str(time.time()) + file_ext
        self.vcs.checkout_as_new(file_path, ver_1, os.path.join(self.temp, new_file_1))
        new_file_2 = str(time.time()) + file_ext
        self.vcs.checkout_as_new(file_path, ver_2, os.path.join(self.temp, new_file_2))
        merged_file = merge_file(os.path.join(self.temp, new_file_1), os.path.join(self.temp, new_file_2), os.path.join(self.vcs.repo_path, file_path))
        print "merge " + file_path + " " + ver_1 + " " + ver_2

    def cmd_commit(self, commit):
        self.setup_vcs()
        file_path = commit[0]
        commit_message = commit[1]
        log_content = self.vcs.commit(file_path, commit_message)
        log_flag = "#" + str(int(self.vcs_logs[self.vcs_current_branch]["HEAD"][1:]) + 1)
        log = {}
        log["hash"] = log_content[1]
        log["message"] = log_content[4]
        self.vcs_logs[self.vcs_current_branch][log_flag] = log
        self.vcs_logs[self.vcs_current_branch]["HEAD"] = log_flag
        with open(self.vcs_db_log, "w") as log_file:
            json.dump(self.vcs_logs, log_file, indent=4)
        print "[New Commit]:"
        print file_path + " - " + commit_message

    def cmd_checkout(self, file_ver):
        self.setup_vcs()
        file_path = file_ver[0]
        ver = self.vcs_logs[self.vcs_current_branch]["#" + file_ver[1]]["hash"]
        self.vcs.checkout(file_path, ver)
        print "checkout " + file_path + " from " + ver

    def cmd_log(self, log_filter):
        self.setup_vcs()
        logs = self.vcs.log()
        print "[Commit History]:"
        for log in logs:
            if len(log_filter) > 0:
                if log_filter[0] in log[1] or log_filter[0] in log[4]:
                    for key, value in self.vcs_logs[self.vcs_current_branch].iteritems():
                        if key != "HEAD" and value["hash"] == log[1]:
                            print key + " - " + log[1] + " - " + log[4]
                            break
            else:
                for key, value in self.vcs_logs[self.vcs_current_branch].iteritems():
                    if key != "HEAD" and value["hash"] == log[1]:
                        print key + " - " + log[1] + " - " + log[4]
                        break

    def cmd_branch(self, command):
        self.setup_vcs()
        if len(command) == 0:
            print "[Local Branches]:"
            print "* " + self.vcs_branches["current"]
            if len(self.vcs_branches["other"]) > 0:
                for branch in self.vcs_branches["other"]:
                    print "  " + branch
        else:
            if command[0] not in self.vcs_logs:
                self.vcs.create_branch(command[0])
                self.vcs_logs[command[0]] = {"HEAD": "#0"}
                with open(self.vcs_db_log, "w") as log_file:
                    json.dump(self.vcs_logs, log_file, indent=4)
            self.vcs.switch_branch(command[0])

    def cmd_clean(self, command):
        if len(command) == 0:
            clean_path(self.temp)
            clean_path(cardiff_path, "\.pyc")
        else:
            for filter in command:
                clean_path(self.temp, filter)

    def cmd_help(self, command):
        commands = {
            "init": "init <repo_path>",
            "diff": "diff <file> <version_1> [<version_2>]",
            "merge": "merge <file> <version_1> [<version_2>]",
            "commit": "commit <file> <message>",
            "checkout": "checkout <file> <version>",
            "log": "log [filter]",
            "branch": "branch <branch>",
            "clean": "clean [filter]",
            "help": "help [command]"
        }
        print "Usage:"
        if len(command) == 1:
            print "  Cardiff.py " + commands[command[0]]
        else:
            for key, value in commands.iteritems():
                print "  Cardiff.py " + value

    def exec_cmd(self, command):
        self.commands[command[0]](command[1:])

if __name__ == "__main__":
    cardiff = Cardiff()
    settings_path = os.path.join(cardiff_path, "settings.json")
    cardiff.load_settings(settings_path)
    cardiff.exec_cmd(sys.argv[1:])
