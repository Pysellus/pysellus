import os
import sys
from inspect import isfunction
from importlib import import_module


def load(path):
    if _is_python_file(path):
        sys.path.insert(0, os.path.dirname(path))
        module = import_module(_get_module_name_from_path(path))
        return _get_setup_functions_from_module(module)

    functions = []
    for module in _get_modules(path):
        functions += _get_setup_functions_from_module(module)

    return functions


def _get_module_name_from_path(path):
    return _remove_extension(path.split('/')[-1])


def _get_setup_functions_from_module(module):
    """
    Gets all setup functions from the given module.
    Setup functions are required to start with 'pscheck_'
    """
    functions = []
    for name in dir(module):
        value = getattr(module, name)
        if isfunction(value) and name.startswith('pscheck_'):
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
        _remove_extension(filename)
        for filename in os.listdir(directory)
        if not filename.startswith('__') and _is_python_file(filename)
    ]


def _is_python_file(filename):
    return filename.endswith('.py')


def _remove_extension(filename):
    return filename[:-3]
