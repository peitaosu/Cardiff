import os, sys
import git

class VCS():
    def __init__(self):
        self.name = "Git"
        self.pypkg = "GitPython"
        self.repo = None

    def set_repo(self, repo_path):
        self.repo = git.Repo(repo_path)

    def init(self, path, name, email):
        self.repo = git.Repo.init(path)
        self.repo.config_writer().set_value("user", "name", name)
        self.repo.config_writer().set_value("user", "email", email)

    def commit(self, file_path, message):
        self.repo.index.add([file_path])
        self.repo.index.commit(message)

    def checkout(self, file_path, version):
        git = self.repo.git
        git.checkout(version, file_path)

    def log(self):
        head = self.repo.head
        master = head.reference
        log = master.log()
        return log
