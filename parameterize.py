import importlib

def parameterize_diff(file_diff, file_ext):
    file_parameterizer = importlib.import_module("format." + file_ext + ".parameterizer")
    file_parameterizer.parameterize(file_diff)
