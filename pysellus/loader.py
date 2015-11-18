import os
import sys
from inspect import isfunction
from importlib import import_module


def load_test_files(path):
    """
    load_test_files :: String -> [(a -> b)]

    Given a filesystem path, import all modules under that path, then import all setup_functions
    inside those modules.

    See load_modules, _get_setup_functions_from_module
    """
    modules = load_modules(path)

    functions = []
    for module in modules:
        functions += _get_setup_functions_from_module(module)

    return functions


def load_modules(path):
    """
    load_modules :: String -> [python.Module]

    Given a filesystem path, import all modules under that path.

    If the path is a file, import that file. If it's a directory, import all python files inside
    that folder, in a non-recursive manner.
    """
    if _is_python_file(path):
        sys.path.insert(0, os.path.dirname(path))
        module = import_module(_get_module_name_from_path(path))
        return [module]

    return _get_modules(path)


def _get_module_name_from_path(path):
    return _remove_extension(path.split('/')[-1])


def _get_setup_functions_from_module(module):
    """
    Gets all setup functions from the given module.
    All setup functions have the 'is_setup_function' attribute

    See integrations#on_failure
    """
    functions = []
    for entry in dir(module):
        value = getattr(module, entry)
        if isfunction(value) and hasattr(value, 'is_setup_function'):
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
