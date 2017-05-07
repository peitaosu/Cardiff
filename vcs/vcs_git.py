import os, sys
import git

class VCS():
    def __init__(self):
        self.name = "Git"
        self.pypkg = "GitPython"
        self.repo = None
        self.repo_path = None

    def set_repo(self, repo_path):
        self.repo = git.Repo(repo_path)
        self.repo_path = repo_path

    def init(self, path, name, email):
        self.repo = git.Repo.init(path)
        self.repo.config_writer().set_value("user", "name", name)
        self.repo.config_writer().set_value("user", "email", email)

    def commit(self, file_path, message):
        self.repo.index.add([file_path])
        self.repo.index.commit(message)
        return self.log()[-1]

    def checkout(self, file_path, version):
        git = self.repo.git
        git.checkout(version, file_path)

    def checkout_as_new(self, file_path, version, new_file_path):
        git = self.repo.git
        os.rename(os.path.join(self.repo_path, file_path), os.path.join(self.repo_path, "saved." + file_path))
        git.checkout(version, file_path)
        os.rename(os.path.join(self.repo_path, file_path), os.path.join(self.repo_path, new_file_path))
        os.rename(os.path.join(self.repo_path, "saved." + file_path), os.path.join(self.repo_path, file_path))

    def log(self):
        head = self.repo.head
        master = head.reference
        log = master.log()
        return log
