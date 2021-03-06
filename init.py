import os, sys, importlib

def init_vcs(vcs_name):
    """initialize the VCS

    args:
        vcs_name (str)
    
    returns:
        vcs_instance (object)
    """
    vcs_module = importlib.import_module("vcs.vcs_" + vcs_name)
    vcs_class = getattr(vcs_module, 'VCS')
    vcs_instance = vcs_class()
    return vcs_instance

def init_vcs_log(vcs_db_path, repo_name):
    """initialize the VCS log file

    args:
        vcs_db_path (str)
        repo_name (str)
    """
    with open(os.path.join(vcs_db_path, repo_name, "log.json"), "w") as vcs_log_file:
        vcs_log_file.write("{\"master\":{\"HEAD\": \"#0\"}}")