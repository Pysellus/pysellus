import os
import inspect

from doublex import Spy
from expects import expect, have_key, raise_error, be
from doublex_expects import have_been_called_with

from pysellus import loader
from pysellus import integrations
from pysellus import integration_config

with description('the integration_config module'):
    with description('loads integrations from a config file'):
        with it('raises FileNotFoundError if the file doesn\'t exist'):
            expect(lambda: integration_config._load_config_file('/bogus/path')).to(
                raise_error(FileNotFoundError)
            )

            isfile = os.path.isfile
            os.path.isfile = lambda pth: True

            expect(lambda: integration_config._load_config_file('/bogus/path/file.py')).to(
                raise_error(FileNotFoundError)
            )

            os.path.isfile = isfile

        # PermissonError: [Errno 1] Operation not permitted
        with it('exits the program if the file is empty'):
            path = '/tmp/ps' + integration_config.CONFIGURATION_FILE_NAME
            os.mknod(path)

            expect(lambda: integration_config._load_config_file(path)).to(
                raise_error(SystemExit)
            )

            os.remove(path)

    with description('loads integrations from a dict'):
        with context('which has a definition section'):
            with it('returns None if it is missing'):
                expect(integration_config._load_custom_integrations({})).to(be(None))

            with context('each definition contains aliases and configurations'):
                with it('aborts the program if any alias is duplicated'):
                    config_dict = {'custom_integrations': {'duplicated_name': {}}}
                    integrations.integration_classes['duplicated_name'] = {}

                    expect(lambda: integration_config._load_custom_integrations(config_dict)).to(
                        raise_error(SystemExit)
                    )

                    del integrations.integration_classes['duplicated_name']

                with context('each configuration contains a module path and a class name'):
                    with it('aborts the program if the either key is missing'):
                        config_dict = {'some_alias': {}}
                        expect(lambda: integration_config._load_custom_integrations_classes(config_dict)).to(
                            raise_error(SystemExit)
                        )

                    with it('loads the module and finds the class name inside it'):
                        load_modules = loader.load_modules
                        getmembers = inspect.getmembers

                        config_dict = {'some_alias': {
                            'name': 'IntegrationClassName',
                            'path': '/some/filesystem/path'
                        }}

                        name = config_dict['some_alias']['name']
                        path = config_dict['some_alias']['path']

                        classobject = Spy()

                        loader.load_modules = lambda pth: ['sample_returned_module']
                        inspect.getmembers = lambda module, pred: [(name, classobject)]

                        expect(integration_config._get_matching_classobject_from_path(name, path)).to(
                            be(classobject)
                        )

                        integration_config._load_custom_integrations_classes(config_dict)

                        expect(integrations.integration_classes).to(have_key('some_alias'))
                        expect(integration_config.integration_classes['some_alias']).to(be(classobject))

                        del integration_config.integration_classes['some_alias']
                        loader.load_modules = load_modules
                        inspect.getmembers = getmembers

                    with it('aborts the program if the given class name is not in the path module'):
                        integration_config._get_matching_classobject_from_path = lambda a, b: None

                        config_dict = {'some_alias': {'path': '/some/path', 'name': 'some_name'}}
                        expect(lambda: integration_config._load_custom_integrations_classes(config_dict)).to(
                            raise_error(SystemExit)
                        )

        with context('and a notify section'):
            with before.each:
                self.original_integration_instance_creator = integration_config._get_integration_instance
                self.integration_config_spy = Spy()
                integration_config._get_integration_instance = self.integration_config_spy._get_integration_instance

            with it('aborts the program if it is missing'):
                expect(lambda: integration_config._load_defined_integrations({})).to(
                    raise_error(SystemExit)
                )

            with context('when an integration alias is specified'):
                with context('and the integration is configured with one or more parameters'):
                    with it('requests an integration instance and registers that alias'):
                        kwargs_for_integration_constructor = {
                            'some_arg': 'some_value',
                            'another_arg': 35
                        }
                        integrations_configuration = {'notify': {
                            'my-alias': {
                                'an_integration': kwargs_for_integration_constructor
                            }
                        }}

                        integration_config._load_defined_integrations(integrations_configuration)

                        expect(self.integration_config_spy._get_integration_instance).to(
                            have_been_called_with('an_integration', kwargs_for_integration_constructor).once
                        )
                        expect(integrations.loaded_integrations).to(have_key('my-alias'))

                with context('and the integration is configured with no parameters'):
                    with it('requests an integration instance and registers that alias'):
                        kwargs_for_integration_constructor = None
                        integrations_configuration = {'notify': {
                            'my-alias': {
                                'an_integration': kwargs_for_integration_constructor
                            }
                        }}

                        integration_config._load_defined_integrations(integrations_configuration)

                        expect(self.integration_config_spy._get_integration_instance).to(
                            have_been_called_with('an_integration', kwargs_for_integration_constructor).once
                        )
                        expect(integrations.loaded_integrations).to(have_key('my-alias'))

            with context('when an integration alias is not specified'):
                with context('and the integration is configured with one or more parameters'):
                    with it('requests an integration instance and registers the stock name'):
                        kwargs_for_integration_constructor = {
                            'some_arg': 'some_value'
                        }
                        integrations_configuration = {'notify': {
                            'an_integration': kwargs_for_integration_constructor
                        }}

                        integration_config._load_defined_integrations(integrations_configuration)

                        expect(self.integration_config_spy._get_integration_instance).to(
                            have_been_called_with('an_integration', kwargs_for_integration_constructor).once
                        )
                        expect(integrations.loaded_integrations).to(have_key('an_integration'))

                with context('and the integration is configured with no parameters'):
                    with it('requests an integration instance and registers the stock name'):
                        kwargs_for_integration_constructor = None
                        integrations_configuration = {'notify': {
                            'an_integration': kwargs_for_integration_constructor
                        }}

                        integration_config._load_defined_integrations(integrations_configuration)

                        expect(self.integration_config_spy._get_integration_instance).to(
                            have_been_called_with('an_integration', kwargs_for_integration_constructor).once
                        )
                        expect(integrations.loaded_integrations).to(have_key('an_integration'))

            with after.each:
                integration_config._get_integration_instance = self.original_integration_instance_creator
