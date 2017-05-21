import importlib

def parameterize_diff(file_diff, file_ext):
    """parameterize the file diff

    args:
        file_diff (object)
        file_ext (str)
    """
    file_parameterizer = importlib.import_module("format." + file_ext + ".parameterizer")
    file_parameterizer.parameterize(file_diff)
