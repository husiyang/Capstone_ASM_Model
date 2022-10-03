#!/usr/bin/env python3
"""
Command line interface.
"""
import argparse
import os

import oepr.settings
import oepr.sample


def get_cli_args():
    parser = argparse.ArgumentParser(__file__)
    parser.add_argument('--config-file',
                        default=oepr.settings.DEFAULT_SETTINGS_FILENAME)

    parser.set_defaults(func=lambda _: getattr(os, 'EX_OK', 0))

    subparsers = parser.add_subparsers()

    p_sample = subparsers.add_parser('sample')
    p_sample.set_defaults(func=oepr.sample.main)

    args = parser.parse_args()

    if not args.config_file:
        parser.exit('no config file specified')

    return args

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
