import queue
from functools import partial

from doublex import Spy, Mock
from expects import expect, be
from doublex_expects import have_been_called

from pysellus import threader

with description('the threader module'):
    with it('should create as many threads as the sum of len(values) of the supplied dict'):
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

    with it('should create a properly initialized thread'):
        stream = Mock()
        observer = Spy()
        target = Spy().target_function

        thread = threader.make_thread(target, stream, observer)

        thread.start()
        thread.join()

        expect(target).to(have_been_called)

    with it('should call the target function with the correct arguments'):
        stream = Mock()
        observer = Spy()
        que = queue.Queue(maxsize=1)

        # Return a list with the stream and the observer fn
        target_function = lambda s, o: [s, o]

        # We can't return from a function running in another thread
        # so we put the value on a queue
        target_wrapper = lambda q, s, o: q.put(target_function(s, o))

        # We define a partial so that we don't have to pass the queue
        # as a parameter to make_thread
        target_partial = partial(target_wrapper, que)

        thread = threader.make_thread(target_partial, stream, observer)

        thread.start()
        thread.join()

        result = que.get()
        # result is [stream, observer]

        expect(result[0]).to(be(stream))
        expect(result[1]).to(be(observer))

    with it('should call `run` on every thread passed to the launch_threads function'):
        a_thread = Spy()
        another_thread = Spy()

        threads = [
            a_thread,
            another_thread
        ]

        threader.launch_threads(threads)

        for thread in threads:
            expect(thread.start).to(have_been_called.once)
