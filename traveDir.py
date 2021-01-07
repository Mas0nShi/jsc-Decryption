import os

_files = []
_exts = [".jsc"]

def deep_iterate_dir(rootDir):
    for lists in os.listdir(rootDir):
        path = os.path.join(rootDir, lists)
        if os.path.isdir(path):
            deep_iterate_dir(path)
        elif os.path.isfile(path):
            ext = os.path.splitext(path)[1]
            if ext in _exts:
                _files.append(path)


def getfileslist():
    return _files


