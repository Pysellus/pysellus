from queue import Queue
from functools import partial

from doublex import Spy, Mock
from expects import expect, be
from doublex_expects import have_been_called

from pysellus import threader

with description('the threader module'):
    with it('should create as many threads as streams in the supplied dict'):
        a_stream = Mock()
        another_stream = Mock()

        a_tester = Spy().a_tester
        another_tester = Spy().another_tester

        streams_to_observers = {
            a_stream: [a_tester],
            another_stream: [a_tester, another_tester]
        }

        threads = threader.build_threads(streams_to_observers)

        expect(len(threads)).to(be(len(streams_to_observers)))

    with it('should initialize threads by calling the given target function'):
        stream = Mock()
        subject = Spy()
        target_function = Spy().target_function

        thread = threader.make_thread(target_function, stream, subject)

        thread.start()
        thread.join()

        expect(target_function).to(have_been_called.once)

    with it('should call the target function with the correct arguments'):
        stream = Mock()
        subject = Spy()
        queue = Queue(maxsize=1)

        # Return a list with the stream and the observer fn
        target_function = lambda s, o: [s, o]

        # We can't return from a function running in another thread
        # so we put the value on a queue
        target_wrapper = lambda q, s, o: q.put(target_function(s, o))

        # We define a partial so that we don't have to pass the queue
        # as a parameter to make_thread
        target_partial = partial(target_wrapper, queue)

        thread = threader.make_thread(target_partial, stream, subject)

        thread.start()
        thread.join()

        result = queue.get()
        # result is [stream, observer]

        expect(result[0]).to(be(stream))
        expect(result[1]).to(be(subject))

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
