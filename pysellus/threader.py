from threading import Thread


def build_threads(stream_to_observers, fn):
    threads = []
    for k, v in stream_to_observers.items():
        for e in v:
            threads.append(make_thread(fn, k, e))

    return threads


def make_thread(fn, stream, observer):
    return Thread(target=fn, args=(stream, observer))


def launch_threads(threads):
    for thread in threads:
        thread.start()
