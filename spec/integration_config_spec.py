import os

from doublex import Spy
from expects import expect, have_key, raise_error, be
from doublex_expects import have_been_called_with

from pysellus import integrations
from pysellus import integration_config

with description('the integration_config module'):
    with description('loads integrations from a config file'):
        with it('raises FileNotFoundError if the file doesn\'t exist'):
            expect(lambda: integration_config._load_config_file('/bogus/path')).to(
                raise_error(FileNotFoundError)
            )

        # PermissonError: [Errno 1] Operation not permitted
        with _it('exits the program if the file is empty'):
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
                        integrations_configuration = {
                            'my-alias': {
                                'an_integration': kwargs_for_integration_constructor
                            }
                        }

                        integration_config._load_integrations_from_configuration(integrations_configuration)

                        expect(self.integration_config_spy._get_integration_instance).to(
                            have_been_called_with('an_integration', kwargs_for_integration_constructor).once
                        )
                        expect(integrations.loaded_integrations).to(have_key('my-alias'))

                with context('and the integration is configured with no parameters'):
                    with it('requests an integration instance and registers that alias'):
                        kwargs_for_integration_constructor = None
                        integrations_configuration = {
                            'my-alias': {
                                'an_integration': kwargs_for_integration_constructor
                            }
                        }

                        integration_config._load_integrations_from_configuration(integrations_configuration)

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
                            integrations_configuration = {
                                'an_integration': kwargs_for_integration_constructor
                            }

                            integration_config._load_integrations_from_configuration(integrations_configuration)

                            expect(self.integration_config_spy._get_integration_instance).to(
                                have_been_called_with('an_integration', kwargs_for_integration_constructor).once
                            )
                            expect(integrations.loaded_integrations).to(have_key('an_integration'))

                with context('and the integration is configured with no parameters'):
                    with it('requests an integration instance and registers the stock name'):
                        kwargs_for_integration_constructor = None
                        integrations_configuration = {
                            'an_integration': kwargs_for_integration_constructor
                        }

                        integration_config._load_integrations_from_configuration(integrations_configuration)

                        expect(self.integration_config_spy._get_integration_instance).to(
                            have_been_called_with('an_integration', kwargs_for_integration_constructor).once
                        )
                        expect(integrations.loaded_integrations).to(have_key('an_integration'))

            with after.each:
                integration_config._get_integration_instance = self.original_integration_instance_creator
