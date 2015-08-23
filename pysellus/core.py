#!/usr/bin/env python3

import argparse

from pysellus import loader, registrar, threader, integration_config

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', type=str,
                        metavar='expanded files directory', help='directory of the expanded files')
    args = parser.parse_args()

    directory = args.directory
    integration_config.load_integrations(directory)

    threader.launch_threads(
        threader.build_threads(
            registrar.register(loader.load(directory))
        )
    )


if __name__ == '__main__':
    main()
