from expects import expect, be
from doublex import Spy, Mock

from pysellus import threader

with description('the threader module'):
    with it('should create as many threads as keys * values in the supplied dict'):
        a_stream = Mock()
        another_stream = Mock()

        foo = Spy()
        a_function = Spy()
        another_function = Spy()
        streams_to_observers = {
            a_stream: [a_function],
            another_stream: [a_function, another_function]
        }

        threads = threader.build_threads(streams_to_observers, foo)

        expected_length = sum(
            len(fn_list) for fn_list in streams_to_observers.values()
        )

        expect(len(threads)).to(be(expected_length))
