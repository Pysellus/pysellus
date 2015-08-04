import rx.subjects as subjects

from threading import Thread

def perform_subscribe(s, o):
    s.subscribe(o)

def build_threads(stream_to_observers, fn=perform_subscribe):
    threads = []
    for k, v in stream_to_observers.items():
        subject = subjects.Subject()
        for e in v:
            subject.subscribe(e)
        threads.append(make_thread(fn, k, subject))

    return threads

def make_thread(fn, stream, subject):
    return Thread(target=fn, args=(stream, subject))


def launch_threads(threads):
    for thread in threads:
        thread.start()
