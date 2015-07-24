import os
import sys
from inspect import isfunction
from importlib import import_module


def load(directory):
    functions = []

    for module in _get_modules(directory):
        for name in dir(module):
            value = getattr(module, name)
            if isfunction(value) and not name.startswith('_'):
                functions.append(value)

    return functions


def _get_modules(directory):
    sys.path.insert(0, directory)
    return [
        import_module(filename)
        for filename in _get_python_files(directory)
    ]


def _get_python_files(directory):
    return [
        _remove_file_extension(file)
        for file in os.listdir(directory)
        if not file.startswith('__') and _is_python_file(file)
    ]


def _is_python_file(filename):
    return filename.endswith('.py')


def _remove_file_extension(filename):
    return filename[:-3]
