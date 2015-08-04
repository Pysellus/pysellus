from rx.subjects import Subject

from threading import Thread


def perform_subscribe(stream, observer):
    stream.subscribe(observer)


def build_threads(stream_to_observers, thread_target=perform_subscribe):
    threads = []

    for stream, observers in stream_to_observers.items():
        subject = Subject()
        for observer in observers:
            subject.subscribe(observer)

        threads.append(make_thread(thread_target, stream, subject))

    return threads


def make_thread(thread_target, stream, subject):
    return Thread(target=thread_target, args=(stream, subject))


def launch_threads(threads):
    for thread in threads:
        thread.start()
