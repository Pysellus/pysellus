from expects.matchers import Matcher


class contain_exactly_function_called(Matcher):
    """
    Assert that the names of all functions in a
    list of functions are exactly the given names.
    """

    def __init__(self, *expected_function_names):
        self._expected_function_names = expected_function_names

    def _match(self, a_list_of_functions):
        self._function_names = list(map(
            lambda function: function.__name__,
            a_list_of_functions
        ))

        if len(a_list_of_functions) != len(self._expected_function_names):
            return False

        for expected_name in self._expected_function_names:
            if expected_name not in self._function_names:
                return False

        return True

    def _failure_message(self, a_list_of_functions):
        return 'Expected function names {} to be exactly {}'.format(
            self._function_names,
            self._expected_function_names
        )
