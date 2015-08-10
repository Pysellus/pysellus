import rx.subjects as subjects

from pysellus.stock_integrations import terminal

""" { test_name: [ registered_integrations ] } """
registered_integrations = {}

""" { integration_name: rx.subjects.Subject } """
integration_to_subject = {}


def on_failure(*integration_names):
    """
    on_failure :: [String] -> (fn -> fn)

    Decorator that maps the given function to the supplied integration names tuple

    Usage:
    @on_failure('integration')
    def foo():
        ...

    Receives a tuple of strings representing an integration (i.e. 'terminal', 'slack'),
    and returns a decorator function.

    This decorator function takes a function, and, for each string in the original tuple,
    creates a Subject object (see _get_integration). It then maps it against the
    given function name, {string: rx.Subject}.

    Finally, returns the original function

    """
    def decorator_of_setup_function(setup_function):
        registered_integrations[setup_function.__name__] = [
            _get_integration(integration_name_)
            for integration_name_ in integration_names
        ]

        return setup_function

    return decorator_of_setup_function


def _get_integration(integration_name):
    """
    _get_integration :: String -> rx.Subject

    Get the Subject object mapped to the given integration name

    If it doesn't exist, create it (see create) and store it in integration_to_subject,
    mapped against the given name {string: rx.Subject}

    """
    if integration_name not in integration_to_subject:
        integration_to_subject[integration_name] = _create(integration_name)

    return integration_to_subject[integration_name]


# TODO: Search for the integration name somewhere and get the functions
def _create(integration_name):
    """
    create :: String -> rx.Subject

    Given an integration name, create a new rx.Subject mapped to it

    In any case, the returned Subject has already been subscribed by all interested functions,
    so one can send a message to it without fear that the message will be lost

    """
    subject = None
    if integration_name == 'terminal':
        subject = terminal.TerminalIntegration().get_subject()

    return subject


def notify_element(test_name, element_payload):
    _notify_integrations(test_name, element_payload)


def notify_error(test_name, element_payload):
    _notify_integrations(test_name, element_payload, error=True)


def _notify_integrations(test_name, message, error=False):
    """
    _notify_integrations :: String -> Any -> Boolean -> IO

    Given a function name, and a Payload object, send the payload to the appropiate subject.

    Check the function name in `registered_integrations` and get all mapped subjects,
    and send the payload to all of them.

    If the error flag is set to true, send the message as an error

    """
    for integration in registered_integrations[test_name]:
        if error:
            integration.on_error(message)
        else:
            integration.on_next(message)
