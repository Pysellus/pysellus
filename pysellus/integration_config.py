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
    integrations_configuration = _load_integration_config_file(path)

    declared_integrations = integrations_configuration['notify']

    for alias, configuration in declared_integrations.items():
        instance = _get_integration_instance(configuration)
        loaded_integrations[alias] = instance


def _load_integration_config_file(path):
    """
    _load_integration_config_file :: String -> {}

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


def _get_integration_instance(integration_configuration):
    """
    _get_integration_instance :: {} -> AbstractIntegration

    Given a dictionary containing an integration name,
    and another dictionary of arguments, find the class representing that
    name, and return an instance of it, passing it all the parameters in the
    parameter dictionary.
    """
    integration_name = list(integration_configuration.keys())[0]
    try:
        integration_class = integration_classes[integration_name]
    except KeyError as e:
        print("The integration {} does not exist\nAborting...".format(e))
        exit(1)

    kwargs_for_integration_constructor = integration_configuration.values()
    if kwargs_for_integration_constructor:
        return integration_class(**kwargs_for_integration_constructor)
    else:
        return integration_class()
