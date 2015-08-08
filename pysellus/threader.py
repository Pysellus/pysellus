from rx.subjects import Subject

from threading import Thread


def _perform_subscribe(stream, observer):
    stream.subscribe(observer)


def build_threads(stream_to_testers, thread_target=_perform_subscribe):
    threads = []

    for stream, testers in stream_to_testers.items():
        subject = Subject()
        for tester in testers:
            subject.subscribe(tester)

        threads.append(_make_thread(thread_target, stream, subject))

    return threads


def _make_thread(thread_target, stream, subject):
    return Thread(target=thread_target, args=(stream, subject))


def launch_threads(threads):
    for thread in threads:
        thread.start()
