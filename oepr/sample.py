#!/usr/bin/env python3
"""
Sample.
"""
import csv
import functools
import os.path
import pathlib
import shelve
import sys
import threading

import oepr.db
import oepr.settings
import oepr.read
import oepr.normalise
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
    grp.add_argument('--train-and-test', action='store_true',
                     help='produce train and test data in csv form')
    grp.add_argument('--normalise', action='store_true',
                     help='produce train, test data and do all normalisation')
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


def convert_shelf(path_shelf):
    titlerow = functools.reduce(
        lambda a, b: a + b,
        ('X.{0} Y.{0} Z.{0}'.format(k).split() for k in range(1, 89)),
        ['X', 'Y', 'Z']
    )

    def frame_to_row(frame):
        return functools.reduce(lambda a, b: a + list(b), frame['points'], [])

    with shelve.open(path_shelf) as hdl:
        data = dict(hdl)

    metadata = data.pop('metadata')
    sample = data.pop('sample')

    path = os.path.join(os.path.dirname(path_shelf), '%s.csv' % key(metadata['Take Name']))

    with open(path, 'w', newline='') as hdl:
        w = csv.writer(hdl, delimiter=',')

        w.writerow(titlerow)
        for frame in sample:
            w.writerow(frame_to_row(frame))

    return path


def sample_csv(path_csv, path_out, path_cfg, path_samples, path_normalise, normalise=False):
    """sample and optionally normalise a single csv file"""
    k = sample(path_csv, path_cfg, path_samples)

    if not k:
        return

    path_shelf = os.path.join(path_samples, k + '_shelf')
    path_sampled_csv = convert_shelf(path_shelf)

    os.rename(path_sampled_csv, path_out)
    os.unlink('%s.db' % path_shelf)

    if normalise:
        oepr.normalise.normalise(path_out, path_out.replace(path_samples, path_normalise))


def sample_to_subdir(subdir, path_cfg, path_samples, path_labelled_visits,
                     normalise=False):
    args_list = []
    threads = []
    p_subdir = os.path.join(path_samples, subdir)

    path_normalise = oepr.settings.get_cfg_field('path_normalise', path_cfg)
    normalise_subdir = os.path.join(path_normalise, subdir)

    max_threads = oepr.settings.get_cfg_field('max_threads', path_cfg, converter=int)

    if not os.path.isdir(p_subdir):
        os.makedirs(p_subdir)

    if normalise and not os.path.isdir(normalise_subdir):
        os.makedirs(normalise_subdir)

    for index, c in enumerate(oepr.read.get_csvs(path_labelled_visits)):
        path_out = os.path.join(p_subdir, '%d.csv' % (index + 1))
        args = (c, path_out, path_cfg, path_samples, path_normalise, normalise)
        args_list.append(args)

    while args_list:
        if len(threads) < max_threads:
            threads.append(threading.Thread(target=sample_csv, args=args_list.pop()))
            threads[-1].start()

        for index, t in enumerate(threads):
            if not t.is_alive():
                t.join()
            threads.pop(index)

    for t in threads:
        t.join()


def sample(csv_, path_cfg, path_samples):
    try:
        metadata = oepr.read.get_info_take(csv_)
        sample = list(SAMPLE_FUNCTION(csv_))
    except Exception as _:
        error = os.path.join(
            path_samples,
            metadata['Take Name'].replace(' ', '_') + '_error.txt'
        )
        pathlib.Path(error).touch()
    else:
        k = key(metadata['Take Name'])
        value = {'metadata': metadata, 'sample': sample}
        oepr.db.kv_write(path_cfg, 'sample', k, value)

        return k


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
    elif args.train_and_test:
        sample_to_subdir('train', path_cfg, path_samples, path_labelled_visits)
        sample_to_subdir('test', path_cfg, path_samples, path_labelled_visits)
    elif args.normalise:
        sample_to_subdir('train', path_cfg, path_samples, path_labelled_visits,
                normalise=True)
        sample_to_subdir('test', path_cfg, path_samples, path_labelled_visits,
                normalise=True)
    else:
        for c in oepr.read.get_csvs(path_labelled_visits):
            sample(c, path_cfg, path_samples)

    return getattr(os, 'EX_OK', 0)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
