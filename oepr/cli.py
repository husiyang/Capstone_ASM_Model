#!/usr/bin/env python3
"""
Command line interface.
"""
import argparse
import os.path

import oepr.settings


def get_cli_args():
    parser = argparse.ArgumentParser(__file__)
    parser.add_argument('--config-file',
                        default=oepr.settings.DEFAULT_SETTINGS_FILENAME)

    args = parser.parse_args()

    if not args.config_file:
        parser.exit('no config file specified')

    return args

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
