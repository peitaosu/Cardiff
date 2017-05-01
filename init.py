import os, sys, importlib

def init_vcs(vcs_name):
    vcs_module = importlib.import_module("vcs.vcs_" + vcs_name)
    vcs_class = getattr(vcs_module, 'VCS')
    vcs_instance = vcs_class()
    return vcs_instance
