#!/usr/bin/env python3
"""
Sample.
"""
import os.path
import pathlib
import sys

import oepr.db
import oepr.settings
import oepr.read
import oepr.preprocess

SAMPLE_FUNCTION = oepr.preprocess.sample_average_bucketed_centroid_distance

def config_parser(subp):
    parse = subp.add_parser('sample')
    parse.set_defaults(func=oepr.sample.main)
    parse.add_argument('--read', action='store_true',
                          help='read samples to stdout')
    return parse

def key(name_take):
    return name_take.replace(' ', '_')


def read(path_cfg):
    for s in oepr.db.kv_read_all(path_cfg, 'sample'):
        print(s)

    return getattr(os, 'EX_OK', 0)


def main(args):
    """main function for module"""
    path_cfg = args.config_file

    path_labelled_visits = oepr.settings.get_cfg_field(
        'path_labelled_visits', path_cfg
    )
    path_samples = oepr.settings.get_cfg_field('path_samples', path_cfg)

    if not os.path.isdir(path_labelled_visits):
        print('no such directory as %s' % path_labelled_visits,
               file=sys.stderr)
        return getattr(os, 'EX_NOINPUT', -1)

    if not os.path.isdir(path_samples):
        os.mkdir(path_samples)

    if args.read:
        return read(path_cfg)

    for c in oepr.read.get_csvs(path_labelled_visits):
        try:
            metadata = oepr.read.get_info_take(c)
            sample = list(SAMPLE_FUNCTION(c))
        except Exception as _:
            error = os.path.join(
                path_samples,
                metadata['Take Name'].replace(' ', '_') + '_error.txt'
            )
            pathlib.Path(error).touch()
        else:
            pass
            k = key(metadata['Take Name'])
            value = {'metadata': metadata, 'sample': sample}
            oepr.db.kv_write(path_cfg, 'sample', k, value)

    return getattr(os, 'EX_OK', 0)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
