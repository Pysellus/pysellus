import argparse

from pysellus import loader, registrar, threader


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', type=str,
                        metavar='expanded files directory', help='directory of the expanded files')
    args = parser.parse_args()

    directory = args.directory

    threader.launch_threads(
        threader.build_threads(
            registrar.register(loader.load(directory))
        )
    )
