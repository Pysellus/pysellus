import os
import inspect
import tempfile
import shutil

from doublex import Spy
from expects import expect, have_key, raise_error, be
from doublex_expects import have_been_called_with

from pysellus import loader
from pysellus import integrations
from pysellus import integration_config


with description('the integration_config module'):
    with description('loads integrations from a config file'):
            with context('raises FileNotFoundError if the config file is not present at the given path'):
                with before.each:
                    self.path_to_directory_without_config_file = tempfile.mkdtemp()

                with it('when the path is to a directory'):
                    def attempt_to_read_config_file():
                        integration_config._get_path_to_configuration_file(
                            self.path_to_directory_without_config_file
                        )

                    expect(attempt_to_read_config_file).to(raise_error(FileNotFoundError))

                with it('when the path is to a file (in which case its parent directory is considered)'):
                    path_to_file_whose_parent_directory_doesnt_contain_config_file = os.path.join(
                        self.path_to_directory_without_config_file,
                        'a_file.py'
                    )
                    open(path_to_file_whose_parent_directory_doesnt_contain_config_file, 'w').close()

                    def attempt_to_read_config_file():
                        integration_config._get_path_to_configuration_file(
                            path_to_file_whose_parent_directory_doesnt_contain_config_file
                        )

                    expect(attempt_to_read_config_file).to(raise_error(FileNotFoundError))

                with after.each:
                    shutil.rmtree(self.path_to_directory_without_config_file)


            with it('raises an exception if the config file is empty'):
                expect(lambda: integration_config._load_configuration_from_contents_of_config_file('')).to(
                    raise_error(integration_config.EmptyConfigurationFileError)
                )

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
                    with it('aborts the program if either key is missing'):
                        for malformed_config_dict in [{'some_alias': {}},
                                                      {'some_alias': {'name': 'foo'}},
                                                      {'some_alias': {'path': 'foo'}}]:
                            expect(lambda: integration_config._load_custom_integrations_classes(malformed_config_dict)).to(
                                raise_error(SystemExit)
                            )

                    with it('finds the class name inside the module'):
                        load_modules = loader.load_modules
                        original_class_finder = integration_config._get_classes_in_module

                        an_integration_class_name = 'IntegrationClassName'
                        a_path_to_an_integration_module = '/some/filesystem/path'

                        config_dict = {'some_alias': {
                            'name': an_integration_class_name,
                            'path':a_path_to_an_integration_module
                        }}

                        an_integration_class_object = Spy()

                        loader.load_modules = lambda pth: ['sample_returned_module']
                        integration_config._get_classes_in_module = lambda module: [(an_integration_class_name, an_integration_class_object)]


                        expect(integration_config._get_matching_classobject_from_path(
                            an_integration_class_name,
                            a_path_to_an_integration_module)
                        ).to(be(an_integration_class_object))


                        loader.load_modules = load_modules
                        integration_config._get_classes_in_module = original_class_finder

                    with it('saves the class to the pysellus.integrations.integration_classes dict under the specified alias'):
                        load_modules = loader.load_modules
                        original_class_finder = integration_config._get_classes_in_module

                        an_integration_class_name = 'IntegrationClassName'
                        a_path_to_an_integration_module = '/some/filesystem/path'

                        config_dict = {'some_alias': {
                            'name': an_integration_class_name,
                            'path':a_path_to_an_integration_module
                        }}

                        an_integration_class_object = Spy()

                        loader.load_modules = lambda pth: ['sample_returned_module']
                        integration_config._get_classes_in_module = lambda module: [(an_integration_class_name, an_integration_class_object)]


                        integration_config._load_custom_integrations_classes(config_dict)


                        expect(integrations.integration_classes).to(have_key('some_alias'))
                        expect(integration_config.integration_classes['some_alias']).to(be(an_integration_class_object))

                        del integration_config.integration_classes['some_alias']
                        loader.load_modules = load_modules
                        integration_config._get_classes_in_module = original_class_finder

                    with it('aborts the program if the given class name is not in the module at the specified path'):
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
