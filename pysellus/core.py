#!/usr/bin/env python3

import argparse

from pysellus import loader, registrar, threader, integration_config


def main():
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        '-f', '--file', metavar='test_file', nargs=1, help='test file', required=False
    )

    group.add_argument(
        '-d', '--directory', metavar='test_directory', nargs=1, help='directory of test files'
    )

    args = parser.parse_args()
    user_input = args.directory[0] if args.directory else args.file[0]

    integration_config.load_integrations(user_input)

    threader.launch_threads(
        threader.build_threads(
            registrar.register(loader.load_test_files(user_input))
        )
    )


if __name__ == '__main__':
    main()
