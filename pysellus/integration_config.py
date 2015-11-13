import os
import inspect

import yaml

from pysellus import loader
from pysellus.integrations import loaded_integrations, integration_classes


CONFIGURATION_FILE_NAME = '.ps_integrations.yml'


def load_integrations(path):
    """
    load_integrations :: String -> IO

    Given a path, find the config file at it and load it.
    """
    configuration = _load_config_file(path)
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
    path_to_configuration_file = _get_path_to_configuration_file(path)

    with open(path_to_configuration_file, 'r') as config_file:
        try:
            configuration = _load_configuration_from_contents_of_config_file(config_file)
        except EmptyConfigurationFileError as error:
            exit("Error while reading {path}: {reason}".format(
                path=path_to_configuration_file,
                reason=error.message
                )
            )

        return configuration


def _get_path_to_configuration_file(path):
    directory_containing_configuration_file = _get_parent_directory_of_path(path)
    path_to_configuration_file = os.path.join(
        directory_containing_configuration_file,
        CONFIGURATION_FILE_NAME
        )

    if not os.path.exists(path_to_configuration_file):
        raise FileNotFoundError

    return path_to_configuration_file

def _get_parent_directory_of_path(path):
    if os.path.isdir(path):
        return path

    return os.path.dirname(path)

def _load_configuration_from_contents_of_config_file(contents_of_config_file):
    loaded_configuration = yaml.load(contents_of_config_file)

    if loaded_configuration is None:
        raise EmptyConfigurationFileError()

    return loaded_configuration


def _load_custom_integrations(configuration):
    """
    _load_custom_integrations :: {} -> IO

    Given an integration configuration dict, get their definitions and import them,
    then add them to the integrations#loaded_integrations dict.

    If the definition is missing, pass.
    """
    if 'custom_integrations' not in configuration:
        return

    custom_integrations_configuration = configuration['custom_integrations']
    _load_custom_integrations_classes(custom_integrations_configuration)


def _load_custom_integrations_classes(custom_configuration):
    """
    _load_custom_integrations_classes :: {} -> IO

    Given a map of configuration definitions, find the integration module, import it,
    and then load the appropiate class object into the integration_classes dict.

    Fails if it can't find the class object inside the module, or if the integration
    name is a duplicate.
    """
    for alias, configuration in custom_configuration.items():
        if alias in integration_classes.keys():
            exit(
                "Conflicting integration name '{}'. Integration names must be unique\nAborting..."
                .format(alias)
            )

        integration_name = configuration.pop('name', None)
        integration_path = configuration.pop('path', None)

        if not all((integration_name, integration_path)):
            exit("Malformed integration '{}': missing class name and/or module path".format(alias))

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
    """
    _get_matching_classobject_from_path :: String -> String -> python.ClassObject | None

    Given a class name, and a module path, search for the given class inside it and return the
    first match.

    If no match is found, return None.
    """
    integration_module = loader.load_modules(path)[0]
    module_members = inspect.getmembers(integration_module, inspect.isclass)
    for name, classobject in module_members:
        if name == class_name:
            return classobject


def _load_defined_integrations(configuration):
    """
    _load_defined_integrations :: {} -> IO

    Given an integration configuration dict, get their constructors and import them,
    then add them to the integrations#loaded_integrations dict.

    Fails if the constructor section is missing.
    """
    try:
        integration_configuration = configuration['notify']
        _load_integrations_from_configuration(integration_configuration)
    except KeyError:
        exit("Malformed configuration file: missing 'notify' section")


def _load_integrations_from_configuration(integrations_configuration):
    """
    _load_integrations_from_configuration :: {} -> IO

    Given a map of integration constructors, gather the attributes and build an instance
    of the integration. Then map their aliases with their instances inside the
    loaded_integrations dict
    """
    for alias, integration_name, kwargs_for_integration_constructor \
            in _unpack_integration_configuration_data(integrations_configuration):
        loaded_integrations[alias] = _get_integration_instance(
            integration_name,
            kwargs_for_integration_constructor
        )


def _unpack_integration_configuration_data(integrations_configuration):
    """
    _unpack_integration_configuration_data :: {} -> (String, String, {} | None)

    Given a map of integration constructors, gather the attributes into an alias, the integration
    name and a map of constructor parameters.

    Yields a tuple on every call.
    """
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


class EmptyConfigurationFileError(Exception):
    def __init__(self, message="configuration file is empty"):
        super(EmptyConfigurationFileError, self).__init__(message)

        self.message = message
