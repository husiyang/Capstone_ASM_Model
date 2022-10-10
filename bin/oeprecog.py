#!/usr/bin/env python3
"""
OEP Recognise.
"""
import argparse
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

import oepr.settings
import oepr.cli


def main():
    """entry point"""
    args = oepr.cli.get_cli_args()

    path_cfg = os.path.join(BASE, args.config_file)

    if not os.path.isfile(path_cfg):
        print('creating config file %s with default settings' %
              args.config_file, file=sys.stderr)
        oepr.settings.create_default_settings(args.config_file)
        return -1

    args.config_file = path_cfg

    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
