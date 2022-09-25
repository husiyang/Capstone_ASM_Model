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
import oepr.read
import oepr.cli
import oepr.preprocess


def main():
    """entry point"""
    args = oepr.cli.get_cli_args()

    path_cfg = os.path.join(BASE, args.config_file)

    if not os.path.isfile(path_cfg):
        print('creating config file %s with default settings' %
              args.config_file, file=sys.stderr)
        oepr.settings.create_default_settings(args.config_file)
        return -1

    path_labelled_visits = oepr.settings.get_cfg_field(
        'path_labelled_visits', path_cfg
    )

    if not os.path.isdir(path_labelled_visits):
        print('no such directory as %s' % path_labelled_visits,
               file=sys.stderr)
        return getattr(os, 'EX_NOINPUT', -1)

    for c in oepr.read.get_csvs(path_labelled_visits):
        print(oepr.read.get_info_take(c))

        for d in oepr.preprocess.sample_average_bucketed_centroid_distance(c):
            print(d)

    return getattr(os, 'EX_OK', 0)


if __name__ == '__main__':
    sys.exit(main())

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
