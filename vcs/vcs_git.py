import os, sys
import git

class VCS():
    def __init__(self):
        self.name = "Git"
        self.pypkg = "GitPython"
        self.repo = None
        self.repo_path = None

    def set_repo(self, repo_path):
        """set the git repo

        args:
            repo_path (str)
        """
        self.repo = git.Repo(repo_path)
        self.repo_path = repo_path

    def init(self, path, name, email):
        """init a new git repo

        args:
            path (str)
            name (str)
            email (str)
        """
        self.repo = git.Repo.init(path)
        self.repo.config_writer().set_value("user", "name", name)
        self.repo.config_writer().set_value("user", "email", email)

    def commit(self, file_path, message):
        """commit a file to default branch with message

        args:
            file_path (str)
            message (str)

        returns:
            log (tuple)
        """
        self.repo.index.add([file_path])
        self.repo.index.commit(message)
        return self.log()[-1]

    def checkout(self, file_path, version):
        """checkout file with specific version

        args:
            file_path (str)
            version (str)
        """
        git = self.repo.git
        git.checkout(version, file_path)

    def checkout_as_new(self, file_path, version, new_file_path):
        """checkout file with specific version as new file

        args:
            file_path (str)
            version (str)
            new_file_path (str)
        """
        git = self.repo.git
        os.rename(os.path.join(self.repo_path, file_path), os.path.join(self.repo_path, "saved." + file_path))
        git.checkout(version, file_path)
        os.rename(os.path.join(self.repo_path, file_path), os.path.join(self.repo_path, new_file_path))
        os.rename(os.path.join(self.repo_path, "saved." + file_path), os.path.join(self.repo_path, file_path))

    def log(self):
        """return default branch logs
        """
        head = self.repo.head
        master = head.reference
        log = master.log()
        return log
    
    def create_branch(self, branch_name):
        """create new branch

        args:
            branch_name (str)
        """
        new_branch = self.repo.create_head(branch_name)

    def switch_branch(self, branch):
        """switch to specific branch

        args:
            branch (str)
        """
        self.previous_branch = self.repo.active_branch
        self.repo.head.reference = self.repo.heads[branch]

    def get_branches(self):
        """get branches
        """
        self.branches = {}
        self.branches["current"] = "master"
        self.branches["other"] = []
        for branch in self.repo.heads:
            if branch == self.repo.head.reference:
                self.branches["current"] = branch.name
            else:
                self.branches["other"].append(branch.name)
        return self.branches