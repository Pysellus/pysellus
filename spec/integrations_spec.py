import rx

from expects import expect, be, contain_exactly, be_a, raise_error
from doublex import Spy
from doublex_expects import have_been_called

from pysellus import integrations
from pysellus.integrations import on_failure
from pysellus.interfaces import AbstractIntegration


with description('the integrations module'):
    with context('exposes an `on_failure` decorator which'):
        with before.each:
            integrations.integrations = {}

        with after.each:
            integrations.integrations = {}

        with it('returns the decorated function as is'):
            decorated_function = Spy().decorated_function

            expect(on_failure('terminal')(decorated_function)).to(be(decorated_function))

        with it('doesn\'t call the decorated function'):
            decorated_function = Spy().decorated_function

            on_failure('terminal')(decorated_function)

            expect(decorated_function).to_not(have_been_called)

        with it('has the (convenient) side effect of registering the integration name with a subject'):
            decorated_function = Spy().decorated_function

            on_failure('terminal')(decorated_function)

            expect(list(integrations.integrations.keys())).to(contain_exactly(decorated_function.__name__))

            for list_of_associated_subjects in integrations.integrations.values():
                for subject in list_of_associated_subjects:
                    expect(subject).to(be_a(rx.subjects.Subject))

    with context('exposes an abstract `AbstractIntegration` class which'):
        with before.all:
            class WrongIntegration(AbstractIntegration):
                pass

            class GoodIntegration(AbstractIntegration):
                def on_next(self):
                    pass

            self.WrongIntegration = WrongIntegration
            self.GoodIntegration = GoodIntegration

        with it('requires you to implement an `on_next` handler'):
            expect(lambda: self.WrongIntegration()).to(raise_error(
                TypeError,
                'Can\'t instantiate abstract class WrongIntegration with abstract methods on_next'
            ))
            expect(lambda: self.GoodIntegration()).to_not(raise_error(
                TypeError,
                'Can\'t instantiate abstract class GoodIntegration with abstract methods on_next'
            ))

        with it('exposes a `get_subject` method which returns an rx Subject'):
            expect(self.GoodIntegration().get_subject()).to(be_a(rx.subjects.Subject))
