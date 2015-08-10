#!/usr/bin/env python3

import os

import yaml

from pysellus.stock_integrations import integration_classes


_config_file = '.ps_integrations.yml'

# {integration_user_name: integration_instance}
loaded_integrations = {}


def load_integrations(folder):
    """
    load_integrations :: String -> IO

    Given a filesystem folder, find the config file in it, load it,
    and...

    """
    config_dict = _load_integration_config(folder)

    declarations = config_dict['notify']

    for integration_alias, integration_dict in declarations.items():
        instance = _get_integration_instance(integration_dict)
        loaded_integrations[integration_alias] = instance

    print(loaded_integrations)


def _load_integration_config(folder):
    """
    _load_integration_config :: String -> {}

    Given a directory, loads the configuration file.
    If given a file, it will try to get the configuration from the
    parent directory.

    If no configuation file is found, raise a FileNotFound exception

    """
    if os.path.isfile(folder):
        folder = folder.rsplit('/', 1)[0]

    config_path = folder + '/' + _config_file

    if not os.path.exists(config_path):
        raise FileNotFoundError

    with open(config_path, 'r') as config:
        return yaml.load(config)


def _get_integration_instance(integration_dict):
    """
    _get_integration_instance :: {} -> AbstractIntegration

    Given a dictionary containing an integration name,
    and another dictionary of argum©®ents, find the class representing that
    name, and return an instance of it, passing it all the parameters in the
    parameter dictionary

    """
    integration_name = list(integration_dict.keys())[0]
    try:
        integration_class = integration_classes[integration_name]
    except KeyError as e:
        print("The integration {} does not exist\nAborting...".format(e))
        exit(1)

    kwargs = integration_dict[integration_name]
    if kwargs:
        return integration_class(**kwargs)
    else:
        return integration_class()
