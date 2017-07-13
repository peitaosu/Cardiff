import os, sys, json, time
from util import *
from init import *
from diff import *
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
            "cdiff": self.cmd_cdiff,
            "merge": self.cmd_merge,
            "commit": self.cmd_commit,
            "checkout": self.cmd_checkout,
            "log": self.cmd_log,
            "branch": self.cmd_branch,
            "clean": self.cmd_clean,
            "help": self.cmd_help,
            "info": self.cmd_info
        }

    def load_settings(self, settings_path = None):
        """load settings from file"""
        if settings_path == None:
            self.settings_path = os.path.join(cardiff_path, "settings.json")
        else:
            self.settings_path = settings_path
        with open(self.settings_path) as settings_file:
            self.settings = json.load(settings_file)
        for key in ["user.name", "user.email"]:
            if self.settings[key].startswith("<") and self.settings[key].endswith(">"):
                print "Please set the {} in settings file.".format(key)
                sys.exit(-1)
        if self.settings["repo"].startswith("<") and self.settings["repo"].endswith(">"):
            print "You need to init a repo first time."
        os.environ["VERBOSE_MODE"] = self.settings["verbose"]
        os.environ["SILENT_MODE"] = self.settings["silent"]
        self.temp = os.path.join(cardiff_path, self.settings["temp"])
        self.vcs_db_path = os.path.join(cardiff_path, "vcs", "vcs_db", self.settings["vcs"])
        vprint("Setting Temp Foloder: {}".format(self.temp))
        make_path_exist(self.temp)
        vprint("Setting VCS DB: {}".format(self.vcs_db_path))
        make_path_exist(self.vcs_db_path)
        self.vcs = init_vcs(self.settings["vcs"])
        vprint("Current VCS: {}".format(self.settings["vcs"]))

    def setup_vcs(self):
        """setup VCS"""
        if self.settings["repo"] != "":
            if self.settings["repo"].startswith("<") and self.settings["repo"].endswith(">"):
                print "You need to init a repo first time."
                sys.exit(-1)
            self.vcs.set_repo(self.settings["repo"])
            vprint("Current Repository: {}".format(self.settings["repo"]))
            self.vcs_branches = self.vcs.get_branches()
            self.vcs_current_branch = self.vcs_branches["current"]
            vprint("Current Branch: {}".format(self.vcs_branches["current"]))
            self.vcs_db_log = os.path.join(self.vcs_db_path, os.path.basename(self.settings["repo"]), "log.json")
            with open(self.vcs_db_log) as log_file:
                self.vcs_logs = json.load(log_file)

    def cmd_init(self, init_path):
        """initial new repository"""
        if len(init_path) > 0:
            init_path = init_path[0]
            if os.path.isdir(init_path):
                print "{} is exist.".format(init_path)
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
                print "Initialized Repository:"
                print init_path
        else:
            print "You need to provide a path for repository initialing."

    def cmd_diff(self, file_ver):
        """diff different versions of file"""
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
        new_file_1_path = os.path.join(self.temp, new_file_1)
        self.vcs.checkout_as_new(file_path, ver_1, new_file_1_path)
        new_file_2 = str(time.time()) + file_ext
        new_file_2_path = os.path.join(self.temp, new_file_2)
        self.vcs.checkout_as_new(file_path, ver_2, new_file_2_path)
        diff_result = diff(new_file_1_path, new_file_2_path)
        print "diff {} {} {}".format(file_path, ver_1, ver_2)
        parameterize_diff(diff_result, file_path.split(".")[-1])
        file_output_name = os.path.join(self.temp, file_path.split(".")[0] + "_" + ver_1[:6] + "_" + ver_2[:6])
        file_diffs = diff_file(new_file_1_path, new_file_2_path, file_output_name)
        if os.getenv("SILENT_MODE") == "1":
            print "Diff Result:"
            print_str_or_list(file_diffs)
        else:
            visualize_diff(new_file_1_path, new_file_2_path, file_diffs, file_path.split(".")[-1], file_output_name)
        return file_diffs

    def cmd_cdiff(self, files):
        """diff different versions of file without VCS"""
        file_before = files[0]
        file_after = files[1]
        if len(files) > 2:
            file_output_name = files[2]
        else:
            file_output_name = os.path.join("./", os.path.splitext(os.path.basename(file_before))[0] + os.path.splitext(os.path.basename(file_after))[0])
        file_ext = os.path.splitext(file_before)[1]
        if file_ext != os.path.splitext(file_after)[1]:
            print "{} and {} format different, can not be diffed.".format(file_before, file_after)
            sys.exit(-1)
        diff_result = diff(file_before, file_after)
        print "diff " + file_before + " " + file_after
        parameterize_diff(diff_result, file_before.split(".")[-1])
        file_diffs = diff_file(file_before, file_after, file_output_name)
        if os.getenv("SILENT_MODE") == "1":
            print "Diff Result:"
            print_str_or_list(file_diffs)
        else:
            visualize_diff(file_before, file_after, file_diffs, file_before.split(".")[-1], file_output_name)
        return file_diffs

    def cmd_merge(self, file_ver):
        """merge different versions of file"""
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
        new_file_1_path = os.path.join(self.temp, new_file_1)
        vprint("Checkout Out File: {} (Version: {}) To {}".format(file_path, ver_1, new_file_1_path))
        self.vcs.checkout_as_new(file_path, ver_1, new_file_1_path)
        new_file_2 = str(time.time()) + file_ext
        new_file_2_path = os.path.join(self.temp, new_file_2)
        vprint("Checkout Out File: {} (Version: {}) To {}".format(file_path, ver_2, new_file_2_path))
        self.vcs.checkout_as_new(file_path, ver_2, new_file_2_path)
        print "merge {} {} {}".format(file_path, ver_1, ver_2)
        merged_file = merge_file(new_file_1_path, new_file_2_path, os.path.join(self.vcs.repo_path, file_path))
        print "Merged File: "
        print_str_or_list(merged_file)
        return merge_file

    def cmd_commit(self, commit):
        """commit version of file to VCS"""
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
        print "New Commit:"
        print "{} - {}".format(file_path, commit_message)

    def cmd_checkout(self, file_ver):
        """checkout specific version of file from VCS"""
        self.setup_vcs()
        file_path = file_ver[0]
        ver = self.vcs_logs[self.vcs_current_branch]["#" + file_ver[1]]["hash"]
        self.vcs.checkout(file_path, ver)
        print "Checked Out: {} - {}".format(file_path, ver)

    def cmd_log(self, log_filter):
        """print all logs of VCS"""
        self.setup_vcs()
        logs = self.vcs.log()
        print "Commit History:"
        for log in logs:
            if len(log_filter) > 0:
                if log_filter[0] in log[1] or log_filter[0] in log[4]:
                    for key, value in self.vcs_logs[self.vcs_current_branch].iteritems():
                        if key != "HEAD" and value["hash"] == log[1]:
                            print "{} - {} - {}".format(key, log[1], log[4])
                            break
            else:
                for key, value in self.vcs_logs[self.vcs_current_branch].iteritems():
                    if key != "HEAD" and value["hash"] == log[1]:
                        print "{} - {} - {}".format(key, log[1], log[4])
                        break

    def cmd_branch(self, command):
        """create new branche, switch to branch or print branches information"""
        self.setup_vcs()
        if len(command) == 0:
            print "Local Branches:"
            print "* {}".format(self.vcs_branches["current"])
            if len(self.vcs_branches["other"]) > 0:
                for branch in self.vcs_branches["other"]:
                    print "  {}".format(branch)
        else:
            if command[0] not in self.vcs_logs:
                self.vcs.create_branch(command[0])
                vprint("Created Branch: {}".format(command[0]))
                self.vcs_logs[command[0]] = {"HEAD": "#0"}
                with open(self.vcs_db_log, "w") as log_file:
                    json.dump(self.vcs_logs, log_file, indent=4)
            self.vcs.switch_branch(command[0])
            vprint("Checked Out to Branch: {}".format(command[0]))

    def cmd_clean(self, command):
        """clean all temporary files"""
        if len(command) == 0:
            clean_path(self.temp)
            vprint("Cleaned Temporary Folder: {}".format(self.temp))
            clean_path(cardiff_path, "\.pyc")
            vprint("Cleaned All .pyc Files")
        else:
            for filter in command:
                clean_path(self.temp, filter)

    def cmd_help(self, command):
        """print usage"""
        commands = {
            "init": "init <repo_path>",
            "diff": "diff <file> <version_1> [<version_2>]",
            "cdiff": "cdiff <file1> <file2> [<output>]",
            "merge": "merge <file> <version_1> [<version_2>]",
            "commit": "commit <file> <message>",
            "checkout": "checkout <file> <version>",
            "log": "log [<filter>]",
            "branch": "branch <branch>",
            "clean": "clean [<filter>]",
            "help": "help [<command>]",
            "info": "info [<information>]"
        }
        print "Usage:"
        if len(command) == 1:
            print "  Cardiff.py {}".format(commands[command[0]])
        else:
            for key, value in commands.iteritems():
                print "  Cardiff.py ".format(value)

    def cmd_info(self, command):
        """print information of Cardiff"""
        information = self.settings["information"]
        if len(command) == 1:
            print "{:>12}: {:<8}".format(command[0], information[command[0]])
        else:
            for key, value in information.iteritems():
                print "{:>12}: {:<8}".format(key, value)

    def exec_cmd(self, command):
        """execute command"""
        return self.commands[command[0]](command[1:])

if __name__ == "__main__":
    cardiff = Cardiff()
    settings_path = os.path.join(cardiff_path, "settings.json")
    if sys.argv[1] not in ["cdiff"]:
        cardiff.load_settings(settings_path)
    cardiff.exec_cmd(sys.argv[1:])
