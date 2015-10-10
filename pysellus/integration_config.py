import os

import yaml

from pysellus.stock_integrations import integration_classes


CONFIGURATION_FILE_NAME = '.ps_integrations.yml'

# {integration_alias: integration_instance}
loaded_integrations = {}


def load_integrations(path):
    """
    load_integrations :: String -> IO

    Given a path, find the config file at it and load it.
    """
    configuration = _load_config_file(path)
    integrations_configuration = configuration['notify']

    _load_integrations_from_configuration(integrations_configuration)


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


def _load_integrations_from_configuration(integrations_configuration):
    for alias, configuration in integrations_configuration.items():
        integration_name = list(configuration.keys())[0]
        integration_configuration = configuration[integration_name]

        instance = _get_integration_instance(integration_name, integration_configuration)
        loaded_integrations[alias] = instance


def _get_integration_instance(name, configuration):
    """
    _get_integration_instance :: {} -> AbstractIntegration

    Given a dictionary containing an integration name,
    and another dictionary of arguments, find the class representing that
    name, and return an instance of it, passing it all the parameters in the
    parameter dictionary.
    """
    try:
        integration_class = integration_classes[name]
    except KeyError:
        print("The '{}' integration does not exist\nAborting...".format(name))
        exit(1)

    kwargs_for_integration_constructor = configuration.values()
    if kwargs_for_integration_constructor:
        return integration_class(**kwargs_for_integration_constructor)
    else:
        return integration_class()
