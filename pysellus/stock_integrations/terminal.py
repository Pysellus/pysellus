from pysellus.interfaces import AbstractIntegration


class TerminalIntegration(AbstractIntegration):
    def on_next(self, element):
        print("Received => {}".format(element))

    def on_error(self, error):
        print("Error! On: {}".format(error))

    def on_completed(self):
        print("Stream completed!")
