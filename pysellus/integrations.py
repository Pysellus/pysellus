import rx.subjects as subjects

integrations = {}
integrations_subject = {}


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
        integrations[setup_function.__name__] = [
            _get_integration(integration_name_)
            for integration_name_ in integration_names
        ]

        return setup_function

    return decorator_of_setup_function


def _get_integration(integration_name):
    """
    _get_integration :: String -> rx.Subject

    Get the Subject object mapped to the given integration name

    If it doesn't exist, create it (see create) and store it in integrations_subject,
    mapped against the given name {string: rx.Subject}

    """
    if integration_name not in integrations_subject.keys():
        integrations_subject[integration_name] = _create(integration_name)

    return integrations_subject[integration_name]


def register_function_to_subject(subject, *functions):
    """
    register_function_to_subject :: rx.Subject -> [fn] -> IO

    Given a subject, and a tuple of functions, subscribe all functions to the subject.

    """
    for fn in functions:
        subject.subscribe(fn)


def notify_element(test_name, element_payload):
    _notify_integration(test_name, element_payload)


def notify_error(test_name, element_payload):
    _notify_integration(test_name, element_payload, error=True)


def _notify_integration(test_name, message, error=False):
    """
    _notify_integration :: String -> Any -> Boolean -> IO

    Given a function name, and a Payload object, send the payload to the appropiate subject.

    Check the function name in integrations and get all mapped subjects, and send the payload to
    all of them.

    If the error flag is set to true, send the message as an error

    """
    for integration in integrations[test_name]:
        if error:
            integration.on_error(message)
        else:
            integration.on_next(message)


# TODO: Search for the integration name somewhere and get the functions
def _create(integration_name):
    """
    create :: String -> rx.Subject

    Given an integration name, create a new rx.Subject mapped to it

    If a mapped subject already exists, return it.

    In any case, the returned Subject has already been subscribed by all interested functions,
    so one can send a message to it without fear that the message will be lost

    """
    if integration_name == 'terminal':
        if integration_name not in integrations_subject:
            integration_subject = subjects.Subject()
            register_function_to_subject(integration_subject, print)
            integrations_subject[integration_name] = integration_subject

        return integrations_subject[integration_name]
