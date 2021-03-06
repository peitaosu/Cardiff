import os, sys, json, time, logging, logging.config
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
            "conf": self.cmd_conf,
            "init": self.cmd_init,
            "diff": self.cmd_diff,
            "cdiff": self.cmd_cdiff,
            "merge": self.cmd_merge,
            "commit": self.cmd_commit,
            "checkout": self.cmd_checkout,
            "log": self.cmd_log,
            "branch": self.cmd_branch,
            "repo": self.cmd_repo,
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
        if self.settings["repo"]["current"].startswith("<") and self.settings["repo"]["current"].endswith(">"):
            print "You need to init a repo first time."
        os.environ["CARDIFF_VERBOSE_MODE"] = self.settings["verbose"]
        os.environ["CARDIFF_SILENT_MODE"] = self.settings["silent"]
        self.temp = os.path.join(cardiff_path, self.settings["temp"])
        self.vcs_db_path = os.path.join(cardiff_path, "vcs", "vcs_db", self.settings["vcs"])
        vprint("Setting Temporary Foloder: {}".format(self.temp))
        make_path_exist(self.temp)
        vprint("Setting VCS DB: {}".format(self.vcs_db_path))
        make_path_exist(self.vcs_db_path)
        self.vcs = init_vcs(self.settings["vcs"])
        vprint("Current VCS: {}".format(self.settings["vcs"]))
        log_config_path = os.path.join(cardiff_path, "logconf.json")
        if not os.path.isfile(log_config_path):
            self.log_config = None
        else:
            with open(log_config_path, "r") as log_config_file:
                self.log_config = json.load(log_config_file)
        self.setup_logging()
    
    def save_settings(self, settings_path = None):
        """save settings to file"""
        if settings_path == None:
            settings_path = self.settings_path
        with open(settings_path, "w") as settings_file:
            json.dump(self.settings, settings_file, indent=4)

    def setup_logging(self, default_level=logging.INFO):
        if self.log_config is not None:
            info_file_folder = os.path.dirname(self.log_config["handlers"]["info_file_handler"]["filename"])
            error_file_folder = os.path.dirname(self.log_config["handlers"]["error_file_handler"]["filename"])
            if "log" in self.settings:
                info_file_folder = error_file_folder = os.path.join(cardiff_path, self.settings["log"])
                self.log_config["handlers"]["info_file_handler"]["filename"] = os.path.join(info_file_folder, "info.log")
                self.log_config["handlers"]["error_file_handler"]["filename"] = os.path.join(error_file_folder, "errors.log")
            make_path_exist(info_file_folder)
            make_path_exist(error_file_folder)
            logging.config.dictConfig(self.log_config)
        else:
            log_folder = os.path.join(cardiff_path, "log")
            if not os.path.isdir(log_folder):
                os.mkdir(log_folder)
            logging.basicConfig(filename="log/info.log", level=default_level)

    def setup_vcs(self):
        """setup VCS"""
        if self.settings["repo"]["current"] != "":
            if self.settings["repo"]["current"].startswith("<") and self.settings["repo"]["current"].endswith(">"):
                print "You need to init a repo first time."
                sys.exit(-1)
            self.vcs.set_repo(self.settings["repo"]["current"])
            vprint("Current Repository: {}".format(self.settings["repo"]["current"]))
            self.vcs_branches = self.vcs.get_branches()
            self.vcs_current_branch = self.vcs_branches["current"]
            vprint("Current Branch: {}".format(self.vcs_branches["current"]))
            self.vcs_commits = self.vcs.get_commits()
            self.vcs_db_log = os.path.join(self.vcs_db_path, os.path.basename(self.settings["repo"]["current"]), "log.json")
            with open(self.vcs_db_log) as log_file:
                self.vcs_logs = json.load(log_file)
            if self.vcs_current_branch not in self.vcs_logs:
                self.vcs_logs[self.vcs_current_branch] = {"HEAD": "#0"}
                for commit in self.vcs_commits:
                    log_flag = "#" + str(len(self.vcs_logs[self.vcs_current_branch].keys()))
                    log = {}
                    log["hash"] = commit[0]
                    log["message"] = commit[1]
                    self.vcs_logs[self.vcs_current_branch][log_flag] = log
                    self.vcs_logs[self.vcs_current_branch]["HEAD"] = log_flag
                with open(self.vcs_db_log, "w") as log_file:
                    json.dump(self.vcs_logs, log_file, indent=4)

    def cmd_conf(self, command):
        """show or change settings through command"""
        if len(command) == 0:
            return
        key = command[0]
        if key not in self.settings:
            print "{} not in settings.json".format(key)
            return
        if len(command) == 1:
            print "{} value is {}".format(key, self.settings[key])
            return self.settings[key]
        else:
            new_value = command[1]
            self.settings[key] = new_value
            self.save_settings()
            self.load_settings(self.settings_path)
            print "{} have been set to {}".format(key, new_value)
            return new_value

    def cmd_init(self, init_repo):
        """initial new repository"""
        if len(init_repo) > 0:
            init_path = os.path.join(cardiff_path, self.settings["repos"], init_repo[0])
            if os.path.isdir(init_path):
                print "Repository {} is exist.".format(init_repo[0])
            else:
                make_path_exist(init_path)
                make_path_exist(os.path.join(self.vcs_db_path, os.path.basename(init_path)))
                init_vcs_log(self.vcs_db_path, os.path.basename(init_path))
                user_name = self.settings["user.name"]
                user_email = self.settings["user.email"]
                self.vcs.init(init_path, user_name, user_email)
                if not self.settings["repo"]["current"].startswith("<") and not self.settings["repo"]["current"].endswith(">"):
                    if self.settings["repo"]["current"] not in self.settings["repo"]["others"]:
                        self.settings["repo"]["others"].append(self.settings["repo"]["current"])
                self.settings["repo"]["current"] = init_path
                with open(self.settings_path, "w") as settings_file:
                    json.dump(self.settings, settings_file, indent=4)
                print "Initialized Repository:"
                print init_path
                return init_path
        else:
            print "You need to provide a repository name for initialization."
            return False

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
        if os.getenv("CARDIFF_SILENT_MODE") == "1":
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
        if os.getenv("CARDIFF_SILENT_MODE") == "1":
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
        commit_content = self.vcs.commit(file_path, commit_message)
        log_flag = "#" + str(len(self.vcs_logs[self.vcs_current_branch].keys()))
        log = {}
        log["hash"] = commit_content[0]
        log["message"] = commit_content[1]
        self.vcs_logs[self.vcs_current_branch][log_flag] = log
        self.vcs_logs[self.vcs_current_branch]["HEAD"] = log_flag
        with open(self.vcs_db_log, "w") as log_file:
            json.dump(self.vcs_logs, log_file, indent=4)
        print "New Commit:"
        print "{} - {}".format(file_path, commit_message)
        return (file_path, commit_message)

    def cmd_checkout(self, file_ver):
        """checkout specific version of file from VCS"""
        self.setup_vcs()
        file_path = file_ver[0]
        ver = self.vcs_logs[self.vcs_current_branch]["#" + file_ver[1]]["hash"]
        self.vcs.checkout(file_path, ver)
        print "Checked Out: {} - {}".format(file_path, ver)
        return (file_path, ver)

    def cmd_log(self, log_filter):
        """print all logs of VCS"""
        self.setup_vcs()
        log_str = "Commit History:\n"
        iter_count = 0
        for commit in reversed(self.vcs_commits):
            iter_count = iter_count + 1
            if len(log_filter) > 0:
                if log_filter[0] in commit[0] or log_filter[0] in commit[1]:
                    log_str = log_str + "#{} - {} - {}".format(iter_count, commit[0], commit[1]) + "\n"
            else:
                log_str = log_str + "#{} - {} - {}".format(iter_count, commit[0], commit[1]) + "\n"
        print log_str
        return log_str

    def cmd_branch(self, command):
        """create new branche, switch to branch or print branches information"""
        self.setup_vcs()
        branch_str = ""
        if len(command) == 0:
            branch_str = "Local Branches:" + "\n"
            branch_str = branch_str + "* {}".format(self.vcs_branches["current"]) + "\n"
            if len(self.vcs_branches["other"]) > 0:
                for branch in self.vcs_branches["other"]:
                    branch_str = branch_str + "  {}".format(branch) + "\n"
            print branch_str
            return branch_str
        else:
            if command[0] not in self.vcs_logs:
                self.vcs.create_branch(command[0])
                vprint("Created Branch: {}".format(command[0]))
            self.vcs.switch_branch(command[0])
            self.setup_vcs()
            vprint("Checked Out to Branch: {}".format(command[0]))
            return command[0]

    def cmd_repo(self, command):
        """switch to repository or print repositories information"""
        if len(command) == 0:
            repo_str = "Local Repositories:" + "\n"
            repo_str = repo_str + "* {}".format(self.settings["repo"]["current"]) + "\n"
            if len(self.settings["repo"]["others"]) > 0:
                for repo in self.settings["repo"]["others"]:
                    repo_str = repo_str + "  {}".format(repo) + "\n"
            print repo_str
            return repo_str
        else:
            if command[0] in self.settings["repo"]["others"]:
                self.settings["repo"]["others"].remove(command[0])
                self.settings["repo"]["others"].append(self.settings["repo"]["current"])
                self.settings["repo"]["current"] = command[0]
                vprint("Switch to Repository: {}".format(command[0]))
                self.save_settings()
                return command[0]

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
            "conf": "conf <config_name> [<config_value>]",
            "init": "init <repo_name>",
            "diff": "diff <file> <version_1> [<version_2>]",
            "cdiff": "cdiff <file1> <file2> [<output>]",
            "merge": "merge <file> <version_1> [<version_2>]",
            "commit": "commit <file> <message>",
            "checkout": "checkout <file> <version>",
            "log": "log [<filter>]",
            "branch": "branch <branch>",
            "repo": "repo <repo>",
            "clean": "clean [<filter>]",
            "help": "help [<command>]",
            "info": "info [<information>]"
        }
        help_str = "Usage:" + "\n"
        if len(command) == 1:
            help_str = help_str + "  Cardiff.py {}".format(commands[command[0]]) + "\n"
        else:
            for key, value in commands.iteritems():
                help_str = help_str + "  Cardiff.py {}".format(value) + "\n"
        print help_str
        return help_str

    def cmd_info(self, command):
        """print information of Cardiff"""
        information = self.settings["information"]
        info_str = ""
        if len(command) == 1:
            info_str = info_str + "{:>12}: {:<8}".format(command[0], information[command[0]]) + "\n"
        else:
            for key, value in information.iteritems():
                info_str = info_str + "{:>12}: {:<8}".format(key, value) + "\n"
        print info_str
        return info_str

    def exec_cmd(self, command):
        """execute command"""
        return self.commands[command[0]](command[1:])

if __name__ == "__main__":
    cardiff = Cardiff()
    settings_path = os.path.join(cardiff_path, "settings.json")
    if sys.argv[1] not in ["cdiff"]:
        cardiff.load_settings(settings_path)
    cardiff.exec_cmd(sys.argv[1:])
    cardiff.save_settings()
