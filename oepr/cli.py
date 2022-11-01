#!/usr/bin/env python3
"""
Command line interface.
"""
import argparse
import os

import oepr.learn
import oepr.settings
import oepr.sample


def get_cli_args():
    parser = argparse.ArgumentParser(prog='oeprecog')
    parser.add_argument('--config-file',
                        default=oepr.settings.DEFAULT_SETTINGS_FILENAME)

    parser.set_defaults(func=lambda _: getattr(os, 'EX_OK', 0))

    subparsers = parser.add_subparsers()
    oepr.sample.config_parser(subparsers)
    oepr.learn.config_parser(subparsers)

    args = parser.parse_args()

    if not args.config_file:
        parser.exit('no config file specified')

    return args

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
