#!/usr/bin/env python3
"""
Sample.
"""
import csv
import functools
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
    parse.set_defaults(func=main)
    grp = parse.add_mutually_exclusive_group()
    grp.add_argument('--read', action='store_true',
                     help='read samples to stdout')
    grp.add_argument('--convert', action='store_true',
                     help='convert shelf files to csv')
    return parse


def key(name_take):
    return name_take.replace(' ', '_')


def read(path_cfg):
    for s in oepr.db.kv_read_all(path_cfg, 'sample'):
        print(s)

    return getattr(os, 'EX_OK', 0)


def convert(path_cfg):
    path_samples = oepr.settings.get_cfg_field('path_samples', path_cfg)

    titlerow = functools.reduce(
        lambda a, b: a + b,
        ('X.{0} Y.{0} Z.{0}'.format(k).split() for k in range(1, 89)),
        ['X', 'Y', 'Z']
    )

    def frame_to_row(frame):
        return functools.reduce(lambda a, b: a + list(b), frame['points'], [])

    for s in oepr.db.kv_read_all(path_cfg, 'sample'):
        metadata = s.pop('metadata')
        sample = s.pop('sample')

        path = os.path.join(path_samples, '%s.csv' % key(metadata['Take Name']))

        with open(path, 'w', newline='') as hdl:
            w = csv.writer(hdl, delimiter=',')

            w.writerow(titlerow)
            for frame in sample:
                w.writerow(frame_to_row(frame))

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
    elif args.convert:
        return convert(path_cfg)

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
