from abc import ABCMeta, abstractmethod

from rx.subjects import Subject


class AbstractIntegration(metaclass=ABCMeta):
    def __init__(self):
        self._subject = Subject()

    def get_subject(self):
        self._subject.subscribe(
            self.on_next,
            self.on_error,
            self.on_completed
        )

        return self._subject

    @abstractmethod
    def on_next(self, element):
        pass

    def on_error(self, element):
        pass

    def on_completed(self):
        pass

