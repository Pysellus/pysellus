import pprint

from pysellus.interfaces import AbstractIntegration


class TerminalIntegration(AbstractIntegration):
    def on_next(self, message):
        print('Assert error: in {0} -> {1}'.format(
            message['test_name'],
            message['expect_function']
        ))
        print('Got:')
        pprint.pprint(message['element'])

    def on_error(self, error_message):
        print('Runtime Error: In {0} -> {1}'.format(
            error_message['test_name'],
            error_message['expect_function']
        ))
        print('Got:')
        pprint.pprint(error_message['error'])

    def on_completed(self):
        print("All tests done.")
