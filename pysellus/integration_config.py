import os
import inspect

import yaml

from pysellus.loader import load_modules
from pysellus.integrations import loaded_integrations, integration_classes

CONFIGURATION_FILE_NAME = '.ps_integrations.yml'


def load_integrations(path):
    """
    load_integrations :: String -> IO

    Given a path, find the config file at it and load it.
    """
    configuration = _load_config_file(path)
    if configuration is None:
        exit("Error while reading {}: file seems to be empty".format(CONFIGURATION_FILE_NAME))

    _load_custom_integrations(configuration)
    _load_defined_integrations(configuration)


def _load_config_file(path):
    """
    _load_config_file :: String -> {}

    Given a directory, loads the configuration file.
    If given a file, it will try to get the configuration from the
    parent directory.

    If no configuration file is found, raise a FileNotFound exception.
    """
    if os.path.isfile(path):
        path = path.rsplit('/', 1)[0]

    config_path = path + '/' + CONFIGURATION_FILE_NAME

    if not os.path.exists(config_path):
        raise FileNotFoundError

    with open(config_path, 'r') as config_file:
        return yaml.load(config_file)


def _load_defined_integrations(configuration):
    try:
        integration_configuration = configuration['notify']
        _load_integrations_from_configuration(integration_configuration)
    except KeyError:
        exit("Malformed configuration file: missing 'notify' section")


def _load_custom_integrations(configuration):
    try:
        custom_integrations_configuration = configuration['custom_integrations']
        _load_custom_integrations_classes(custom_integrations_configuration)
    except KeyError:
        pass  # it's ok for the user to not define custom integrations


def _load_custom_integrations_classes(custom_configuration):
    for alias, configuration in custom_configuration.items():
        if alias in integration_classes.keys():
            exit(
                "Conflicting integration name '{}'. Integration names must be unique\nAborting..."
                .format(alias)
            )

        integration_name = configuration['name']
        integration_path = configuration['path']

        classobject = _get_matching_classobject_from_path(
            integration_name,
            integration_path
        )

        if classobject is None:
            exit(
                "Malformed custom integration '{alias}:\n\t'{klass}' class not found in {module}"
                .format(
                    alias=alias,
                    klass=integration_name,
                    module=integration_path
                )
            )

        integration_classes[alias] = classobject


def _get_matching_classobject_from_path(class_name, path):
    integration_module = load_modules(path)[0]
    module_members = inspect.getmembers(integration_module, inspect.isclass)
    for name, classobject in module_members:
        if name == class_name:
            return classobject


def _load_integrations_from_configuration(integrations_configuration):
    for alias, integration_name, kwargs_for_integration_constructor \
            in _unpack_integration_configuration_data(integrations_configuration):
        loaded_integrations[alias] = _get_integration_instance(
            integration_name,
            kwargs_for_integration_constructor
        )


def _unpack_integration_configuration_data(integrations_configuration):
    for alias, child in integrations_configuration.items():
        if child is None:
            integration_name = alias
            kwargs_for_integration_constructor = None
        elif _has_only_one_key_and_a_dict_as_value(child):
            integration_name = _get_the_only_key_in(child)
            kwargs_for_integration_constructor = child[integration_name]
        elif _has_only_one_key_and_None_as_value(child):
            integration_name = _get_the_only_key_in(child)
            kwargs_for_integration_constructor = None
        else:
            integration_name = alias
            kwargs_for_integration_constructor = child

        yield (alias, integration_name, kwargs_for_integration_constructor)


def _has_only_one_key_and_a_dict_as_value(a_dict):
    return len(a_dict.keys()) == 1 and type(a_dict[_get_the_only_key_in(a_dict)]) is dict


def _get_the_only_key_in(a_dict):
    return list(a_dict.keys())[0]


def _has_only_one_key_and_None_as_value(a_dict):
    return list(a_dict.values()) == [None]


def _get_integration_instance(name, kwargs_for_integration_constructor):
    """
    _get_integration_instance :: {} -> AbstractIntegration

    Given a dictionary containing an integration name,
    and another dictionary of arguments, find the class representing that
    name, and return an instance of it, passing it all the parameters in the
    parameter dictionary.
    """
    try:
        integration_class = integration_classes[name]
        if kwargs_for_integration_constructor is None:
            return integration_class()
        else:
            return integration_class(**kwargs_for_integration_constructor)
    except KeyError:
        exit("On integration '{}': definition missing\nAborting...".format(name))
