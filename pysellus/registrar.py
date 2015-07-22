stream_to_observers = {}


def register(function_list):
    for fn in function_list:
        fn()
    return stream_to_observers


def expect(stream):
    def tests_registrar(*testers):
        if stream in stream_to_observers.keys():
            stream_to_observers[stream] += list(testers)
        else:
            stream_to_observers[stream] = list(testers)

    return tests_registrar
