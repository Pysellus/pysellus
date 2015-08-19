import rx

from expects import expect, be, contain_exactly, be_a
from doublex import Spy, Mock
from doublex_expects import have_been_called

from pysellus import integrations
from pysellus import integration_config
from pysellus.integrations import on_failure


with description('the integrations module'):
    with context('exposes an `on_failure` decorator which'):
        with before.each:
            integrations.registered_integrations = {}

            with Mock() as some_integration_instance:
                some_integration_instance.get_subject().returns(rx.subjects.Subject())

                integration_config.loaded_integrations = {
                    'some_integration': some_integration_instance
                }

        with after.each:
            integrations.registered_integrations = {}
            integration_config.loaded_integrations = {}

        with it('returns the decorated function as is'):
            decorated_function = Spy().decorated_function

            expect(on_failure('some_integration')(decorated_function)).to(be(decorated_function))

        with it('doesn\'t call the decorated function'):
            decorated_function = Spy().decorated_function

            on_failure('some_integration')(decorated_function)

            expect(decorated_function).to_not(have_been_called)

        with it('has the (convenient) side effect of registering the integration name with a subject'):
            decorated_function = Spy().decorated_function

            on_failure('some_integration')(decorated_function)

            expect(list(integrations.registered_integrations.keys())).to(contain_exactly(decorated_function.__name__))

            for setup_function in integrations.registered_integrations:
                for subject in integrations.registered_integrations[setup_function]['integrations']:
                    expect(subject).to(be_a(rx.subjects.Subject))

