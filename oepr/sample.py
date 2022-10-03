#!/usr/bin/env python3
"""
Sample.
"""
import os.path
import pathlib
import shelve
import sys

import oepr.settings
import oepr.read
import oepr.preprocess

SAMPLE_FUNCTION = oepr.preprocess.sample_average_bucketed_centroid_distance


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

    for c in oepr.read.get_csvs(path_labelled_visits):
        try:
            metadata = oepr.read.get_info_take(c)
            samples = list(SAMPLE_FUNCTION(c))
        except Exception as _:
            error = os.path.join(
                path_samples,
                metadata['Take Name'].replace(' ', '_') + '_error.txt'
            )
            pathlib.Path(error).touch()
        else:
            shelf = os.path.join(
                path_samples, metadata['Take Name'].replace(' ', '_') + '_shelf'
            )

            with shelve.open(shelf) as hdl:
                hdl['metadata'] = metadata
                hdl['samples'] = samples

            print(metadata)
            print(samples)

    return getattr(os, 'EX_OK', 0)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
