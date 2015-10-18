from doublex import Spy
from expects import expect, have_key
from doublex_expects import have_been_called_with

from pysellus import integration_config

with description('the integration_config module'):
    with description('loads integrations from a dict'):
        with before.each:
            self.original_integration_instance_creator = integration_config._get_integration_instance
            self.integration_config_spy = Spy()
            integration_config._get_integration_instance = self.integration_config_spy._get_integration_instance

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
                    expect(integration_config.loaded_integrations).to(have_key('my-alias'))

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
                    expect(integration_config.loaded_integrations).to(have_key('my-alias'))

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
                    expect(integration_config.loaded_integrations).to(have_key('an_integration'))

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
                    expect(integration_config.loaded_integrations).to(have_key('an_integration'))

        with after.each:
            integration_config._get_integration_instance = self.original_integration_instance_creator
