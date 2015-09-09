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

        stream_to_testers = {
            a_stream: [a_tester],
            another_stream: [a_tester, another_tester]
        }

        threads = threader.build_threads(stream_to_testers)

        expect(len(threads)).to(be(len(stream_to_testers)))

    with it('should initialize threads by calling the given target function'):
        a_stream = Mock()
        a_subject = Spy()
        target_function = Spy().target_function

        thread = threader._make_thread(target_function, a_stream, a_subject)

        thread.start()
        thread.join()

        expect(target_function).to(have_been_called.once)

    with it('should call the target function with the correct arguments'):
        a_stream = Mock()
        a_subject = Spy()
        queue = Queue(maxsize=1)

        # Return a list with the stream and the observer fn
        target_function = lambda s, o: [s, o]

        # We can't return from a function running in another thread
        # so we put the value on a queue
        target_wrapper = lambda q, s, o: q.put(target_function(s, o))

        # We define a partial so that we don't have to pass the queue
        # as a parameter to make_thread
        target_partial = partial(target_wrapper, queue)

        thread = threader._make_thread(target_partial, a_stream, a_subject)

        thread.start()
        thread.join()

        result = queue.get()
        # result is [stream, observer]

        expect(result[0]).to(be(a_stream))
        expect(result[1]).to(be(a_subject))

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

    with it('should call `subscribe` on each of the passed streams'):
        a_stream = Spy()
        another_stream = Spy()

        a_tester = Spy().a_tester
        another_tester = Spy().another_tester

        stream_to_testers = {
            a_stream: [a_tester],
            another_stream: [a_tester, another_tester]
        }

        threads = threader.build_threads(stream_to_testers)

        threader.launch_threads(threads)

        for stream in stream_to_testers.keys():
            expect(stream.subscribe).to(have_been_called.once)
