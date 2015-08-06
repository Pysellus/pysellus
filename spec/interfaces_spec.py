import rx

from expects import expect, raise_error, be_a

from pysellus.interfaces import AbstractIntegration

with description('the interfaces module'):
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
