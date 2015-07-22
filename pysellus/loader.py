import os
from importlib import import_module
from inspect import isfunction


def load(directory):
    functions = []

    for filename in _get_python_files(directory):
        module = import_module(_path_to_module(directory, filename))
        for name in dir(module):
            value = getattr(module, name)
            if isfunction(value):
                functions.append(value)

    return functions


def _get_python_files(directory):
    return [file for file in os.listdir(directory) if not file.startswith('__')]


def _path_to_module(path, filename):
    return os.path.join(
        os.path.dirname(path),
        _remove_file_extension(filename)
    ).replace('/', '.')


def _remove_file_extension(filename):
    return filename[:-3]
